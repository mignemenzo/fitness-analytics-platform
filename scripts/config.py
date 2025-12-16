"""
Health & Fitness Analytics Platform - Configuration
Author: [Your Name]
Date: December 2025

Configuration settings for ETL pipeline and Snowflake connection.
"""

import os
from pathlib import Path

# Project directory structure
PROJECT_ROOT = Path("/home/ubuntu/fitness_analytics_platform")
DATA_DIR = PROJECT_ROOT / "data"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
SQL_DIR = PROJECT_ROOT / "sql"
LOGS_DIR = PROJECT_ROOT / "logs"

# Create logs directory if it doesn't exist
LOGS_DIR.mkdir(exist_ok=True)

# Snowflake connection configuration
# Update these with your actual Snowflake credentials
SNOWFLAKE_CONFIG = {
    "account": os.getenv("SNOWFLAKE_ACCOUNT", "YOUR_ACCOUNT"),
    "user": os.getenv("SNOWFLAKE_USER", "YOUR_USERNAME"),
    "password": os.getenv("SNOWFLAKE_PASSWORD", "YOUR_PASSWORD"),
    "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
    "role": os.getenv("SNOWFLAKE_ROLE", "SYSADMIN"),
    "database": "RAW_FITNESS_DB",
    "schema": "STAGING"
}

# Three-layer data warehouse configuration
RAW_LAYER = {
    "database": "RAW_FITNESS_DB",
    "schema": "STAGING"
}

CURATED_LAYER = {
    "database": "CURATED_FITNESS_DB",
    "schema": "FITNESS_DATA"
}

ANALYTICS_LAYER = {
    "database": "ANALYTICS_FITNESS_DB",
    "dimensions_schema": "DIMENSIONS",
    "facts_schema": "FACTS",
    "aggregates_schema": "AGGREGATES"
}

# ETL pipeline settings
ETL_CONFIG = {
    "batch_size": 1000,
    "max_retries": 3,
    "retry_delay_seconds": 5,
    "enable_data_quality_checks": True,
    "enable_logging": True,
    "log_level": "INFO"
}

# CSV file locations for sample data
DATA_FILES = {
    "exercises": DATA_DIR / "exercises_sample.csv",
    "nutrition": DATA_DIR / "nutrition_sample.csv",
    "members": DATA_DIR / "members_sample.csv",
    "workout_logs": DATA_DIR / "workout_logs_sample.csv",
    "nutrition_logs": DATA_DIR / "nutrition_logs_sample.csv",
    "member_engagement": DATA_DIR / "member_engagement_sample.csv"
}

# Map data sources to Snowflake table names
RAW_TABLES = {
    "exercises": "RAW_EXERCISES",
    "nutrition": "RAW_NUTRITION",
    "members": "RAW_MEMBERS",
    "workout_logs": "RAW_WORKOUT_LOGS",
    "nutrition_logs": "RAW_NUTRITION_LOGS",
    "member_engagement": "RAW_MEMBER_ENGAGEMENT"
}

# Quality check thresholds for data validation
DATA_QUALITY_THRESHOLDS = {
    "null_percentage_threshold": 10.0,  # Max % of nulls allowed
    "duplicate_percentage_threshold": 5.0,  # Max % of duplicates allowed
    "min_record_count": 10  # Minimum records required
}

# API Ninjas configuration for REST API integration
API_CONFIG = {
    "api_ninjas_base_url": "https://api.api-ninjas.com/v1",
    "api_key": "CEnxh3qaoT7+lNu0rlQifA==sl6jfXXCXDTK5mK9",
    "rate_limit_per_minute": 50,
    "timeout_seconds": 30
}

# Logging setup for pipeline monitoring
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "standard",
            "stream": "ext://sys.stdout"
        },
        "file": {
            "class": "logging.FileHandler",
            "level": "DEBUG",
            "formatter": "detailed",
            "filename": str(LOGS_DIR / "etl_pipeline.log"),
            "mode": "a"
        }
    },
    "loggers": {
        "": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False
        }
    }
}
