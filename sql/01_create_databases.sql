/*
================================================================================
Health & Fitness Analytics Platform - Database Setup
================================================================================
Author: Miguel Nemenzo
Date: December 2025
Purpose: Create three-layer database architecture for fitness analytics

Architecture Layers:
1. RAW Layer: Staging tables for API data ingestion
2. CURATED Layer: Cleaned and validated data
3. ANALYTICS Layer: Star schema optimized for reporting

Usage:
- Run this script in Snowflake worksheet as ACCOUNTADMIN or SYSADMIN
- Ensure you have CREATE DATABASE privileges
================================================================================
*/

-- Set context
USE ROLE SYSADMIN;
USE WAREHOUSE COMPUTE_WH;

-- ============================================================================
-- RAW LAYER: Staging tables for initial data ingestion
-- ============================================================================

CREATE DATABASE IF NOT EXISTS RAW_FITNESS_DB
    COMMENT = 'Raw layer for staging fitness and health data from APIs';

CREATE SCHEMA IF NOT EXISTS RAW_FITNESS_DB.STAGING
    COMMENT = 'Staging schema for raw API data';

USE SCHEMA RAW_FITNESS_DB.STAGING;

-- Create file format for CSV ingestion
CREATE OR REPLACE FILE FORMAT CSV_FORMAT
    TYPE = 'CSV'
    FIELD_DELIMITER = ','
    SKIP_HEADER = 1
    FIELD_OPTIONALLY_ENCLOSED_BY = '"'
    TRIM_SPACE = TRUE
    ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
    ESCAPE = 'NONE'
    ESCAPE_UNENCLOSED_FIELD = '\134'
    DATE_FORMAT = 'AUTO'
    TIMESTAMP_FORMAT = 'AUTO'
    NULL_IF = ('NULL', 'null', '');

-- Create file format for JSON ingestion
CREATE OR REPLACE FILE FORMAT JSON_FORMAT
    TYPE = 'JSON'
    STRIP_OUTER_ARRAY = TRUE
    DATE_FORMAT = 'AUTO'
    TIMESTAMP_FORMAT = 'AUTO';

-- ============================================================================
-- CURATED LAYER: Cleaned and validated data
-- ============================================================================

CREATE DATABASE IF NOT EXISTS CURATED_FITNESS_DB
    COMMENT = 'Curated layer for cleaned and validated fitness data';

CREATE SCHEMA IF NOT EXISTS CURATED_FITNESS_DB.FITNESS_DATA
    COMMENT = 'Curated fitness and health data';

-- ============================================================================
-- ANALYTICS LAYER: Star schema for reporting
-- ============================================================================

CREATE DATABASE IF NOT EXISTS ANALYTICS_FITNESS_DB
    COMMENT = 'Analytics layer with star schema for Power BI reporting';

CREATE SCHEMA IF NOT EXISTS ANALYTICS_FITNESS_DB.DIMENSIONS
    COMMENT = 'Dimension tables for star schema';

CREATE SCHEMA IF NOT EXISTS ANALYTICS_FITNESS_DB.FACTS
    COMMENT = 'Fact tables for star schema';

CREATE SCHEMA IF NOT EXISTS ANALYTICS_FITNESS_DB.AGGREGATES
    COMMENT = 'Pre-aggregated tables for dashboard performance';

-- ============================================================================
-- Create metadata schema for ETL tracking
-- ============================================================================

CREATE SCHEMA IF NOT EXISTS RAW_FITNESS_DB.METADATA
    COMMENT = 'Metadata schema for ETL job tracking and data lineage';

USE SCHEMA RAW_FITNESS_DB.METADATA;

-- ETL job tracking table
CREATE OR REPLACE TABLE ETL_JOB_LOG (
    job_id NUMBER AUTOINCREMENT,
    job_name VARCHAR(200),
    job_type VARCHAR(50),
    source_system VARCHAR(100),
    target_table VARCHAR(200),
    start_time TIMESTAMP_NTZ,
    end_time TIMESTAMP_NTZ,
    status VARCHAR(20),
    records_processed NUMBER,
    records_inserted NUMBER,
    records_updated NUMBER,
    records_rejected NUMBER,
    error_message VARCHAR(5000),
    created_by VARCHAR(100) DEFAULT CURRENT_USER(),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    PRIMARY KEY (job_id)
);

-- Data quality check results
CREATE OR REPLACE TABLE DATA_QUALITY_LOG (
    quality_check_id NUMBER AUTOINCREMENT,
    table_name VARCHAR(200),
    check_name VARCHAR(200),
    check_type VARCHAR(50),
    check_result VARCHAR(20),
    records_checked NUMBER,
    records_failed NUMBER,
    failure_percentage NUMBER(5,2),
    check_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    details VARCHAR(5000),
    PRIMARY KEY (quality_check_id)
);

-- ============================================================================
-- Grant privileges
-- ============================================================================

-- Grant usage on databases
GRANT USAGE ON DATABASE RAW_FITNESS_DB TO ROLE SYSADMIN;
GRANT USAGE ON DATABASE CURATED_FITNESS_DB TO ROLE SYSADMIN;
GRANT USAGE ON DATABASE ANALYTICS_FITNESS_DB TO ROLE SYSADMIN;

-- Grant usage on schemas
GRANT USAGE ON ALL SCHEMAS IN DATABASE RAW_FITNESS_DB TO ROLE SYSADMIN;
GRANT USAGE ON ALL SCHEMAS IN DATABASE CURATED_FITNESS_DB TO ROLE SYSADMIN;
GRANT USAGE ON ALL SCHEMAS IN DATABASE ANALYTICS_FITNESS_DB TO ROLE SYSADMIN;

-- Grant privileges on tables
GRANT ALL PRIVILEGES ON ALL TABLES IN DATABASE RAW_FITNESS_DB TO ROLE SYSADMIN;
GRANT ALL PRIVILEGES ON ALL TABLES IN DATABASE CURATED_FITNESS_DB TO ROLE SYSADMIN;
GRANT ALL PRIVILEGES ON ALL TABLES IN DATABASE ANALYTICS_FITNESS_DB TO ROLE SYSADMIN;

-- Grant future privileges
GRANT ALL PRIVILEGES ON FUTURE TABLES IN DATABASE RAW_FITNESS_DB TO ROLE SYSADMIN;
GRANT ALL PRIVILEGES ON FUTURE TABLES IN DATABASE CURATED_FITNESS_DB TO ROLE SYSADMIN;
GRANT ALL PRIVILEGES ON FUTURE TABLES IN DATABASE ANALYTICS_FITNESS_DB TO ROLE SYSADMIN;

-- ============================================================================
-- Verification queries
-- ============================================================================

-- Show created databases
SHOW DATABASES LIKE '%FITNESS%';

-- Show schemas in each database
SHOW SCHEMAS IN DATABASE RAW_FITNESS_DB;
SHOW SCHEMAS IN DATABASE CURATED_FITNESS_DB;
SHOW SCHEMAS IN DATABASE ANALYTICS_FITNESS_DB;

-- Verify file formats
SHOW FILE FORMATS IN SCHEMA RAW_FITNESS_DB.STAGING;

SELECT 'Database setup completed successfully!' AS status;
