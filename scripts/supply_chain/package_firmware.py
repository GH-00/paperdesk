#!/usr/bin/env python3
"""Create a deterministic, checksummed firmware release package."""

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path
from typing import Any


FLASH_METADATA_FILE = "flasher_args.json"
METADATA_FILES = (
    "flasher_args.json",
    "flash_args",
    "project_description.json",
    "firmware-sbom.cdx.json",
)
ARTIFACT_METADATA_FILE = "ARTIFACT_METADATA.json"
CHECKSUMS_FILE = "SHA256SUMS"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Package firmware flash artifacts with metadata and checksums."
    )
    parser.add_argument("--build-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--source-sha", required=True)
    return parser.parse_args()


def load_json(path: Path) -> dict[str, Any]:
    try:
        with path.open(encoding="utf-8") as file:
            value = json.load(file)
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"could not read JSON file {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise ValueError(f"JSON file {path} must contain an object")
    return value


def ensure_file(path: Path, description: str) -> None:
    if not path.is_file():
        raise ValueError(f"required {description} is missing: {path}")


def resolve_flash_file(build_dir: Path, relative_name: str) -> Path:
    if not isinstance(relative_name, str) or not relative_name:
        raise ValueError("flash_files entries must be non-empty strings")

    candidate = (build_dir / relative_name).resolve()
    try:
        candidate.relative_to(build_dir)
    except ValueError as exc:
        raise ValueError(
            f"flash file escapes build directory: {relative_name}"
        ) from exc
    ensure_file(candidate, f"flash binary ({relative_name})")
    return candidate


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_artifact_metadata(
    output_dir: Path,
    source_sha: str,
    flasher_args: dict[str, Any],
) -> None:
    flash_settings = flasher_args.get("flash_settings")
    flash_files = flasher_args.get("flash_files")
    extra_esptool_args = flasher_args.get("extra_esptool_args")
    if not isinstance(flash_settings, dict):
        raise ValueError("flasher_args.json flash_settings must be an object")
    if not isinstance(flash_files, dict):
        raise ValueError("flasher_args.json flash_files must be an object")
    if not isinstance(extra_esptool_args, dict):
        raise ValueError(
            "flasher_args.json extra_esptool_args must be an object"
        )
    chip = extra_esptool_args.get("chip")
    if not isinstance(chip, str) or not chip:
        raise ValueError("flasher_args.json extra_esptool_args.chip is required")

    metadata = {
        "project": "paperdesk",
        "source_sha": source_sha,
        "chip": chip,
        "flash_settings": flash_settings,
        "flash_files": flash_files,
    }
    path = output_dir / ARTIFACT_METADATA_FILE
    path.write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def write_checksums(output_dir: Path, filenames: list[str]) -> None:
    ordered_filenames = sorted(filenames)
    lines = [
        f"{sha256(output_dir / filename)}  {filename}"
        for filename in ordered_filenames
    ]
    (output_dir / CHECKSUMS_FILE).write_text(
        "\n".join(lines) + "\n",
        encoding="utf-8",
    )


def package_firmware(
    build_dir: Path,
    output_dir: Path,
    source_sha: str,
) -> None:
    source_sha = source_sha.strip()
    if not source_sha:
        raise ValueError("--source-sha must not be empty")

    build_dir = build_dir.resolve()
    output_dir = output_dir.resolve()
    if not build_dir.is_dir():
        raise ValueError(f"build directory is missing: {build_dir}")
    if output_dir.exists():
        if not output_dir.is_dir():
            raise ValueError(f"output path is not a directory: {output_dir}")
        if any(output_dir.iterdir()):
            raise ValueError(
                f"output directory must be empty: {output_dir}"
            )

    flasher_args_path = build_dir / FLASH_METADATA_FILE
    flasher_args = load_json(flasher_args_path)
    flash_files = flasher_args.get("flash_files")
    if not isinstance(flash_files, dict) or not flash_files:
        raise ValueError(
            "flasher_args.json flash_files must be a non-empty object"
        )

    flash_sources: list[tuple[str, Path]] = []
    output_names: set[str] = set()
    for source_name in flash_files.values():
        source = resolve_flash_file(build_dir, source_name)
        output_name = source.name
        if output_name in output_names:
            raise ValueError(
                f"flash binary basename collision in output: {output_name}"
            )
        output_names.add(output_name)
        flash_sources.append((output_name, source))

    metadata_sources = []
    for filename in METADATA_FILES:
        source = build_dir / filename
        ensure_file(source, "firmware metadata")
        if filename in output_names:
            raise ValueError(f"output filename collision: {filename}")
        output_names.add(filename)
        metadata_sources.append((filename, source))

    output_dir.mkdir(parents=True, exist_ok=True)
    for filename, source in flash_sources + metadata_sources:
        shutil.copy2(source, output_dir / filename)

    write_artifact_metadata(output_dir, source_sha, flasher_args)
    checksum_names = [
        *[filename for filename, _ in flash_sources],
        *[filename for filename, _ in metadata_sources],
        ARTIFACT_METADATA_FILE,
    ]
    write_checksums(output_dir, checksum_names)


def main() -> int:
    args = parse_args()
    try:
        package_firmware(args.build_dir, args.output_dir, args.source_sha)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())