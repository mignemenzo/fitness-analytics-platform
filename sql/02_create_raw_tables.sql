/*
================================================================================
Health & Fitness Analytics Platform - RAW Layer Tables
================================================================================
Author: Miguel Nemenzo
Date: December 2025
Purpose: Create staging tables in RAW layer for initial data ingestion

These tables preserve the source data structure with minimal transformations
and include metadata fields for tracking data lineage.
================================================================================
*/

USE ROLE SYSADMIN;
USE WAREHOUSE COMPUTE_WH;
USE SCHEMA RAW_FITNESS_DB.STAGING;

-- ============================================================================
-- RAW_EXERCISES: Exercise catalog from API
-- ============================================================================

CREATE OR REPLACE TABLE RAW_EXERCISES (
    raw_exercise_id NUMBER AUTOINCREMENT,
    exercise_name VARCHAR(500),
    exercise_type VARCHAR(100),
    muscle_group VARCHAR(100),
    difficulty_level VARCHAR(50),
    equipments VARCHAR(1000),
    instructions VARCHAR(10000),
    safety_info VARCHAR(5000),
    -- Metadata fields
    source_system VARCHAR(100) DEFAULT 'API_NINJAS_EXERCISES',
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    batch_id VARCHAR(100),
    record_hash VARCHAR(64),
    PRIMARY KEY (raw_exercise_id)
);

-- ============================================================================
-- RAW_NUTRITION: Nutrition data from API
-- ============================================================================

CREATE OR REPLACE TABLE RAW_NUTRITION (
    raw_nutrition_id NUMBER AUTOINCREMENT,
    food_name VARCHAR(500),
    calories NUMBER(10,2),
    serving_size_g NUMBER(10,2),
    fat_total_g NUMBER(10,2),
    fat_saturated_g NUMBER(10,2),
    protein_g NUMBER(10,2),
    sodium_mg NUMBER(10,2),
    potassium_mg NUMBER(10,2),
    cholesterol_mg NUMBER(10,2),
    carbohydrates_total_g NUMBER(10,2),
    fiber_g NUMBER(10,2),
    sugar_g NUMBER(10,2),
    -- Metadata fields
    source_system VARCHAR(100) DEFAULT 'API_NINJAS_NUTRITION',
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    batch_id VARCHAR(100),
    record_hash VARCHAR(64),
    PRIMARY KEY (raw_nutrition_id)
);

-- ============================================================================
-- RAW_MEMBERS: Member profile data
-- ============================================================================

CREATE OR REPLACE TABLE RAW_MEMBERS (
    raw_member_id NUMBER AUTOINCREMENT,
    member_id VARCHAR(50),
    first_name VARCHAR(200),
    last_name VARCHAR(200),
    email VARCHAR(500),
    age NUMBER,
    gender VARCHAR(50),
    membership_type VARCHAR(100),
    membership_status VARCHAR(50),
    join_date DATE,
    fitness_goal VARCHAR(200),
    height_cm NUMBER(10,2),
    initial_weight_kg NUMBER(10,2),
    -- Metadata fields
    source_system VARCHAR(100) DEFAULT 'MEMBER_SYSTEM',
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    batch_id VARCHAR(100),
    record_hash VARCHAR(64),
    PRIMARY KEY (raw_member_id)
);

-- ============================================================================
-- RAW_WORKOUT_LOGS: Workout activity logs
-- ============================================================================

CREATE OR REPLACE TABLE RAW_WORKOUT_LOGS (
    raw_workout_log_id NUMBER AUTOINCREMENT,
    workout_log_id VARCHAR(50),
    member_id VARCHAR(50),
    workout_date DATE,
    workout_time TIME,
    exercise_name VARCHAR(500),
    exercise_type VARCHAR(100),
    muscle_group VARCHAR(100),
    sets NUMBER,
    reps NUMBER,
    weight_kg NUMBER(10,2),
    duration_minutes NUMBER,
    calories_burned NUMBER(10,2),
    difficulty_rating NUMBER,
    notes VARCHAR(5000),
    -- Metadata fields
    source_system VARCHAR(100) DEFAULT 'WORKOUT_TRACKING_SYSTEM',
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    batch_id VARCHAR(100),
    record_hash VARCHAR(64),
    PRIMARY KEY (raw_workout_log_id)
);

-- ============================================================================
-- RAW_NUTRITION_LOGS: Nutrition intake logs
-- ============================================================================

CREATE OR REPLACE TABLE RAW_NUTRITION_LOGS (
    raw_nutrition_log_id NUMBER AUTOINCREMENT,
    nutrition_log_id VARCHAR(50),
    member_id VARCHAR(50),
    log_date DATE,
    meal_type VARCHAR(100),
    food_item VARCHAR(500),
    serving_size_g NUMBER(10,2),
    servings NUMBER(10,2),
    calories NUMBER(10,2),
    protein_g NUMBER(10,2),
    carbs_g NUMBER(10,2),
    fat_g NUMBER(10,2),
    fiber_g NUMBER(10,2),
    sugar_g NUMBER(10,2),
    -- Metadata fields
    source_system VARCHAR(100) DEFAULT 'NUTRITION_TRACKING_SYSTEM',
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    batch_id VARCHAR(100),
    record_hash VARCHAR(64),
    PRIMARY KEY (raw_nutrition_log_id)
);

-- ============================================================================
-- RAW_MEMBER_ENGAGEMENT: Member engagement metrics
-- ============================================================================

CREATE OR REPLACE TABLE RAW_MEMBER_ENGAGEMENT (
    raw_engagement_id NUMBER AUTOINCREMENT,
    engagement_id VARCHAR(50),
    member_id VARCHAR(50),
    record_date DATE,
    check_ins NUMBER,
    app_logins NUMBER,
    classes_attended NUMBER,
    trainer_sessions NUMBER,
    engagement_score NUMBER(10,2),
    -- Metadata fields
    source_system VARCHAR(100) DEFAULT 'ENGAGEMENT_TRACKING_SYSTEM',
    load_timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    batch_id VARCHAR(100),
    record_hash VARCHAR(64),
    PRIMARY KEY (raw_engagement_id)
);

-- ============================================================================
-- Create indexes for performance
-- ============================================================================

-- Indexes on member_id for join performance
CREATE INDEX IF NOT EXISTS idx_raw_members_member_id ON RAW_MEMBERS(member_id);
CREATE INDEX IF NOT EXISTS idx_raw_workout_logs_member_id ON RAW_WORKOUT_LOGS(member_id);
CREATE INDEX IF NOT EXISTS idx_raw_nutrition_logs_member_id ON RAW_NUTRITION_LOGS(member_id);
CREATE INDEX IF NOT EXISTS idx_raw_engagement_member_id ON RAW_MEMBER_ENGAGEMENT(member_id);

-- Indexes on date fields for time-based queries
CREATE INDEX IF NOT EXISTS idx_raw_workout_logs_date ON RAW_WORKOUT_LOGS(workout_date);
CREATE INDEX IF NOT EXISTS idx_raw_nutrition_logs_date ON RAW_NUTRITION_LOGS(log_date);
CREATE INDEX IF NOT EXISTS idx_raw_engagement_date ON RAW_MEMBER_ENGAGEMENT(record_date);

-- ============================================================================
-- Create stages for file loading
-- ============================================================================

-- Internal stage for CSV files
CREATE OR REPLACE STAGE FITNESS_DATA_STAGE
    FILE_FORMAT = CSV_FORMAT
    COMMENT = 'Internal stage for loading fitness data CSV files';

-- Internal stage for JSON files
CREATE OR REPLACE STAGE FITNESS_JSON_STAGE
    FILE_FORMAT = JSON_FORMAT
    COMMENT = 'Internal stage for loading fitness data JSON files';

-- ============================================================================
-- Verification queries
-- ============================================================================

-- Show all tables in RAW layer
SHOW TABLES IN SCHEMA RAW_FITNESS_DB.STAGING;

-- Show table structures
DESCRIBE TABLE RAW_EXERCISES;
DESCRIBE TABLE RAW_NUTRITION;
DESCRIBE TABLE RAW_MEMBERS;
DESCRIBE TABLE RAW_WORKOUT_LOGS;
DESCRIBE TABLE RAW_NUTRITION_LOGS;
DESCRIBE TABLE RAW_MEMBER_ENGAGEMENT;

-- Show stages
SHOW STAGES IN SCHEMA RAW_FITNESS_DB.STAGING;

SELECT 'RAW layer tables created successfully!' AS status;
