idf_component_register(
    SRCS
        "app_main.cpp"
        "api/dashboard_client.cpp"
        "api/dashboard_parser.cpp"
        "storage/dashboard_cache.cpp"

    INCLUDE_DIRS
        "."
        "api"
        "models"
        "network"
        "pages"
        "storage"

    REQUIRES
        esp_http_client
        json
)
