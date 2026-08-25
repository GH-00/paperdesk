idf_component_register(
    SRCS
        "app_main.cpp"
        "api/dashboard_client.cpp"
        "api/dashboard_parser.cpp"
        "network/wifi_manager.cpp"
        "storage/dashboard_cache.cpp"

    INCLUDE_DIRS
        "."
        "api"
        "models"
        "network"
        "pages"
        "storage"

    REQUIRES
        esp_event
        esp_http_client
        esp_netif
        spiffs
        esp_wifi
        json
        nvs_flash
)
