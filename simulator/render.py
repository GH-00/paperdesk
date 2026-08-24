import argparse

from simulator.api_client import fetch_dashboard
from simulator.config import OUTPUT_DIR
from simulator.pages import (
    calendar_page,
    home_page,
    schedule_page,
)


PAGE_RENDERERS = {
    "calendar": calendar_page.render,
    "schedule": schedule_page.render,
    "home": home_page.render,
}


def parse_args():
    parser = argparse.ArgumentParser(
        description=(
            "Paperdesk 400x300 "
            "RLCD simulator"
        )
    )

    parser.add_argument(
        "--page",
        choices=[
            "calendar",
            "schedule",
            "home",
            "all",
        ],
        default="calendar",
        help="Page to render",
    )

    return parser.parse_args()


def render_single_page(
    data,
    page_name,
):
    renderer = (
        PAGE_RENDERERS[
            page_name
        ]
    )

    image = renderer(data)

    output_file = (
        OUTPUT_DIR
        / f"{page_name}.png"
    )

    image.save(
        output_file
    )

    print(
        f"Rendered: {output_file}"
    )


def main():
    args = parse_args()

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    data = fetch_dashboard()

    if args.page == "all":
        for page_name in (
            PAGE_RENDERERS.keys()
        ):
            render_single_page(
                data,
                page_name,
            )

        return

    render_single_page(
        data,
        args.page,
    )


if __name__ == "__main__":
    main()
