"""
Configuration management for Reactive Hub API

This module handles all application configuration using Pydantic Settings.
It automatically loads environment variables from .env file and provides
type-safe configuration access throughout the application.
"""

from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings(BaseSettings):
    """
    Application settings class
    
    Automatically loads configuration from environment variables
    with type validation and default values.
    """
    
    # Application configuration
    project_name: str = "Reactive Hub API"
    debug: bool = True
    environment: str = "development"
    
    # Server configuration
    port: int = 3001
    
    # API configuration
    api_v1_str: str = "/api/v1"
    
    # CORS configuration
    frontend_url: str = "http://localhost:3000"
    
    # Database configuration (individual parameters)
    database_host: str = "localhost"
    database_port: int = 5432
    database_user: str = "user"
    database_password: str = "password"
    database_name: str = "myapidb"
    
    @property
    def database_url(self) -> str:
        """
        Generate complete database URL from individual parameters
        
        Returns:
            str: Complete PostgreSQL connection URL
        """
        return (
            f"postgresql://{self.database_user}:{self.database_password}"
            f"@{self.database_host}:{self.database_port}/{self.database_name}"
        )
    
    class Config:
        """Pydantic configuration"""
        env_file = ".env"
        env_file_encoding = "utf-8"


# Create global settings instance
# This will be imported and used throughout the application
settings = Settings() 