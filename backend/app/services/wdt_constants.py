"""WDT constant configuration."""
WDT_CONFIG = {
    "test": {
        "sid": "haijun",
        "appkey": "appkey_market_test",
        "appsecret": "***",  # Replace with actual test credentials
        "base_url": "https://openapitest.huice.com/openapi/",
    },
    "prod": {
        "sid": "",
        "appkey": "",
        "appsecret": "",
        "base_url": "https://openapi.huice.com/openapi/",
    },
}
