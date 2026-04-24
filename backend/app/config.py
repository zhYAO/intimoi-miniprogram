"""应用配置，从环境变量读取。"""
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # WDT 旺店通配置
    wdt_appkey: str = "test_appkey"
    wdt_appsecret: str = "test_secret"
    wdt_sid: str = "test_sid"
    wdt_base_url: str = "https://openapitest.huice.com/openapi/"

    # Redis 配置
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: str = ""

    # JWT 配置
    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 10080  # 7 days

    # 服务配置
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
