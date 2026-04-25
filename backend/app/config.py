"""Application configuration."""
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    # Database
    database_url: str = "mysql+pymysql://root:password@localhost:3306/intimoi"
    
    # JWT
    jwt_secret: str = "your-super-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24 * 7  # 7 days
    
    # WeChat
    wechat_appid: str = "your-wechat-appid"
    wechat_secret: str = "your-wechat-secret"
    
    # WDT
    wdt_test_base_url: str = "https://openapitest.huice.com/openapi/"
    wdt_prod_base_url: str = "https://openapi.huice.com/openapi/"
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000


@lru_cache()
def get_settings() -> Settings:
    return Settings()
