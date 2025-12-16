/*
================================================================================
Health & Fitness Analytics Platform - ANALYTICS Layer Star Schema
================================================================================
Author: Miguel Nemenzo
Date: December 2025
Purpose: Create star schema optimized for Power BI reporting

Star Schema Design:
- Dimension tables: Descriptive attributes for analysis
- Fact tables: Measurable events and metrics
- Optimized for query performance and dashboard responsiveness
================================================================================
*/

USE ROLE SYSADMIN;
USE WAREHOUSE COMPUTE_WH;

-- ============================================================================
-- DIMENSION TABLES
-- ============================================================================

USE SCHEMA ANALYTICS_FITNESS_DB.DIMENSIONS;

-- ----------------------------------------------------------------------------
-- DIM_DATE: Standard date dimension for time-based analysis
-- ----------------------------------------------------------------------------

CREATE OR REPLACE TABLE DIM_DATE (
    date_key NUMBER PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day_of_week NUMBER,
    day_name VARCHAR(20),
    day_of_month NUMBER,
    day_of_year NUMBER,
    week_of_year NUMBER,
    month_number NUMBER,
    month_name VARCHAR(20),
    month_abbr VARCHAR(3),
    quarter NUMBER,
    quarter_name VARCHAR(10),
    year NUMBER,
    year_month VARCHAR(7),
    year_quarter VARCHAR(7),
    is_weekend BOOLEAN,
    is_holiday BOOLEAN,
    holiday_name VARCHAR(100),
    fiscal_year NUMBER,
    fiscal_quarter NUMBER,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- ----------------------------------------------------------------------------
-- DIM_TIME: Time of day dimension for workout timing analysis
-- ----------------------------------------------------------------------------

CREATE OR REPLACE TABLE DIM_TIME (
    time_key NUMBER PRIMARY KEY,
    time_value TIME NOT NULL UNIQUE,
    hour NUMBER,
    minute NUMBER,
    hour_12 NUMBER,
    am_pm VARCHAR(2),
    time_of_day VARCHAR(20), -- Morning, Afternoon, Evening, Night
    is_peak_hours BOOLEAN,
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- ----------------------------------------------------------------------------
-- DIM_MEMBER: Member dimension with slowly changing dimension (SCD Type 2)
-- ----------------------------------------------------------------------------

CREATE OR REPLACE TABLE DIM_MEMBER (
    member_key NUMBER AUTOINCREMENT PRIMARY KEY,
    member_id VARCHAR(50) NOT NULL,
    first_name VARCHAR(200),
    last_name VARCHAR(200),
    full_name VARCHAR(400),
    email VARCHAR(500),
    age NUMBER,
    age_group VARCHAR(50),
    gender VARCHAR(50),
    membership_type VARCHAR(100),
    membership_status VARCHAR(50),
    join_date DATE,
    tenure_days NUMBER,
    tenure_months NUMBER,
    tenure_category VARCHAR(50), -- New, Regular, Veteran
    fitness_goal VARCHAR(200),
    height_cm NUMBER(10,2),
    initial_weight_kg NUMBER(10,2),
    bmi_category VARCHAR(50),
    -- SCD Type 2 fields
    effective_date DATE NOT NULL,
    expiration_date DATE,
    is_current BOOLEAN DEFAULT TRUE,
    version NUMBER DEFAULT 1,
    -- Metadata
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE INDEX idx_dim_member_id ON DIM_MEMBER(member_id);
CREATE INDEX idx_dim_member_current ON DIM_MEMBER(is_current);

-- ----------------------------------------------------------------------------
-- DIM_EXERCISE: Exercise catalog dimension
-- ----------------------------------------------------------------------------

CREATE OR REPLACE TABLE DIM_EXERCISE (
    exercise_key NUMBER AUTOINCREMENT PRIMARY KEY,
    exercise_name VARCHAR(500) NOT NULL,
    exercise_type VARCHAR(100),
    exercise_category VARCHAR(100), -- Derived grouping
    muscle_group VARCHAR(100),
    muscle_group_category VARCHAR(50), -- Upper Body, Lower Body, Core
    difficulty_level VARCHAR(50),
    difficulty_score NUMBER, -- Numeric representation for analysis
    equipments VARCHAR(1000),
    equipment_category VARCHAR(100), -- Free Weights, Machines, Bodyweight, etc.
    is_compound_exercise BOOLEAN,
    is_cardio BOOLEAN,
    instructions VARCHAR(10000),
    safety_info VARCHAR(5000),
    -- Metadata
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE INDEX idx_dim_exercise_name ON DIM_EXERCISE(exercise_name);
CREATE INDEX idx_dim_exercise_type ON DIM_EXERCISE(exercise_type);
CREATE INDEX idx_dim_exercise_muscle ON DIM_EXERCISE(muscle_group);

-- ----------------------------------------------------------------------------
-- DIM_NUTRITION: Nutrition item dimension
-- ----------------------------------------------------------------------------

CREATE OR REPLACE TABLE DIM_NUTRITION (
    nutrition_key NUMBER AUTOINCREMENT PRIMARY KEY,
    food_name VARCHAR(500) NOT NULL,
    food_category VARCHAR(100), -- Protein, Carbs, Fats, Vegetables, Fruits
    is_high_protein BOOLEAN,
    is_low_carb BOOLEAN,
    is_healthy_fat BOOLEAN,
    calories_per_100g NUMBER(10,2),
    protein_per_100g NUMBER(10,2),
    carbs_per_100g NUMBER(10,2),
    fat_per_100g NUMBER(10,2),
    fiber_per_100g NUMBER(10,2),
    macro_profile VARCHAR(50), -- High Protein, High Carb, Balanced, etc.
    -- Metadata
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE INDEX idx_dim_nutrition_name ON DIM_NUTRITION(food_name);
CREATE INDEX idx_dim_nutrition_category ON DIM_NUTRITION(food_category);

-- ============================================================================
-- FACT TABLES
-- ============================================================================

USE SCHEMA ANALYTICS_FITNESS_DB.FACTS;

-- ----------------------------------------------------------------------------
-- FACT_WORKOUT_ACTIVITY: Workout session details
-- ----------------------------------------------------------------------------

CREATE OR REPLACE TABLE FACT_WORKOUT_ACTIVITY (
    workout_fact_key NUMBER AUTOINCREMENT PRIMARY KEY,
    workout_log_id VARCHAR(50) NOT NULL,
    -- Foreign keys to dimensions
    member_key NUMBER NOT NULL,
    exercise_key NUMBER NOT NULL,
    workout_date_key NUMBER NOT NULL,
    workout_time_key NUMBER,
    -- Measures
    sets NUMBER,
    reps NUMBER,
    weight_kg NUMBER(10,2),
    total_volume_kg NUMBER(10,2), -- sets * reps * weight
    duration_minutes NUMBER,
    calories_burned NUMBER(10,2),
    difficulty_rating NUMBER,
    -- Derived metrics
    intensity_score NUMBER(10,2), -- Calculated based on weight, reps, sets
    workout_quality_score NUMBER(10,2),
    -- Metadata
    notes VARCHAR(5000),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    -- Foreign key constraints
    FOREIGN KEY (member_key) REFERENCES ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_MEMBER(member_key),
    FOREIGN KEY (exercise_key) REFERENCES ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_EXERCISE(exercise_key),
    FOREIGN KEY (workout_date_key) REFERENCES ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_DATE(date_key),
    FOREIGN KEY (workout_time_key) REFERENCES ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_TIME(time_key)
);

CREATE INDEX idx_fact_workout_member ON FACT_WORKOUT_ACTIVITY(member_key);
CREATE INDEX idx_fact_workout_date ON FACT_WORKOUT_ACTIVITY(workout_date_key);
CREATE INDEX idx_fact_workout_exercise ON FACT_WORKOUT_ACTIVITY(exercise_key);

-- ----------------------------------------------------------------------------
-- FACT_NUTRITION_INTAKE: Daily nutrition logs
-- ----------------------------------------------------------------------------

CREATE OR REPLACE TABLE FACT_NUTRITION_INTAKE (
    nutrition_fact_key NUMBER AUTOINCREMENT PRIMARY KEY,
    nutrition_log_id VARCHAR(50) NOT NULL,
    -- Foreign keys to dimensions
    member_key NUMBER NOT NULL,
    nutrition_key NUMBER NOT NULL,
    log_date_key NUMBER NOT NULL,
    -- Measures
    meal_type VARCHAR(100),
    serving_size_g NUMBER(10,2),
    servings NUMBER(10,2),
    calories NUMBER(10,2),
    protein_g NUMBER(10,2),
    carbs_g NUMBER(10,2),
    fat_g NUMBER(10,2),
    fiber_g NUMBER(10,2),
    sugar_g NUMBER(10,2),
    -- Derived metrics
    protein_calories NUMBER(10,2), -- protein_g * 4
    carbs_calories NUMBER(10,2), -- carbs_g * 4
    fat_calories NUMBER(10,2), -- fat_g * 9
    macro_balance_score NUMBER(10,2),
    -- Metadata
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    -- Foreign key constraints
    FOREIGN KEY (member_key) REFERENCES ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_MEMBER(member_key),
    FOREIGN KEY (nutrition_key) REFERENCES ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_NUTRITION(nutrition_key),
    FOREIGN KEY (log_date_key) REFERENCES ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_DATE(date_key)
);

CREATE INDEX idx_fact_nutrition_member ON FACT_NUTRITION_INTAKE(member_key);
CREATE INDEX idx_fact_nutrition_date ON FACT_NUTRITION_INTAKE(log_date_key);

-- ----------------------------------------------------------------------------
-- FACT_MEMBER_ENGAGEMENT: Member engagement metrics
-- ----------------------------------------------------------------------------

CREATE OR REPLACE TABLE FACT_MEMBER_ENGAGEMENT (
    engagement_fact_key NUMBER AUTOINCREMENT PRIMARY KEY,
    engagement_id VARCHAR(50) NOT NULL,
    -- Foreign keys to dimensions
    member_key NUMBER NOT NULL,
    record_date_key NUMBER NOT NULL,
    -- Measures
    check_ins NUMBER,
    app_logins NUMBER,
    classes_attended NUMBER,
    trainer_sessions NUMBER,
    engagement_score NUMBER(10,2),
    -- Derived metrics
    total_interactions NUMBER, -- Sum of all engagement activities
    engagement_level VARCHAR(50), -- High, Medium, Low
    is_at_risk BOOLEAN, -- Flag for churn risk
    -- Metadata
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    -- Foreign key constraints
    FOREIGN KEY (member_key) REFERENCES ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_MEMBER(member_key),
    FOREIGN KEY (record_date_key) REFERENCES ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_DATE(date_key)
);

CREATE INDEX idx_fact_engagement_member ON FACT_MEMBER_ENGAGEMENT(member_key);
CREATE INDEX idx_fact_engagement_date ON FACT_MEMBER_ENGAGEMENT(record_date_key);

-- ============================================================================
-- AGGREGATE TABLES FOR DASHBOARD PERFORMANCE
-- ============================================================================

USE SCHEMA ANALYTICS_FITNESS_DB.AGGREGATES;

-- ----------------------------------------------------------------------------
-- AGG_MEMBER_MONTHLY_SUMMARY: Monthly member activity summary
-- ----------------------------------------------------------------------------

CREATE OR REPLACE TABLE AGG_MEMBER_MONTHLY_SUMMARY (
    summary_key NUMBER AUTOINCREMENT PRIMARY KEY,
    member_key NUMBER NOT NULL,
    year_month VARCHAR(7) NOT NULL,
    -- Workout metrics
    total_workouts NUMBER,
    total_workout_duration_minutes NUMBER,
    total_calories_burned NUMBER(10,2),
    avg_workout_duration NUMBER(10,2),
    unique_exercises NUMBER,
    most_frequent_muscle_group VARCHAR(100),
    -- Nutrition metrics
    total_nutrition_logs NUMBER,
    avg_daily_calories NUMBER(10,2),
    avg_daily_protein_g NUMBER(10,2),
    avg_daily_carbs_g NUMBER(10,2),
    avg_daily_fat_g NUMBER(10,2),
    -- Engagement metrics
    total_check_ins NUMBER,
    total_app_logins NUMBER,
    total_classes_attended NUMBER,
    avg_engagement_score NUMBER(10,2),
    -- Derived metrics
    workout_consistency_score NUMBER(10,2),
    nutrition_adherence_score NUMBER(10,2),
    overall_performance_score NUMBER(10,2),
    -- Metadata
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE INDEX idx_agg_monthly_member ON AGG_MEMBER_MONTHLY_SUMMARY(member_key);
CREATE INDEX idx_agg_monthly_period ON AGG_MEMBER_MONTHLY_SUMMARY(year_month);

-- ----------------------------------------------------------------------------
-- AGG_DAILY_KPI: Daily KPI metrics for executive dashboard
-- ----------------------------------------------------------------------------

CREATE OR REPLACE TABLE AGG_DAILY_KPI (
    kpi_key NUMBER AUTOINCREMENT PRIMARY KEY,
    kpi_date DATE NOT NULL UNIQUE,
    -- Member metrics
    total_members NUMBER,
    active_members NUMBER,
    new_members NUMBER,
    churned_members NUMBER,
    member_retention_rate NUMBER(10,2),
    -- Activity metrics
    total_workouts NUMBER,
    total_workout_minutes NUMBER,
    avg_workouts_per_member NUMBER(10,2),
    total_calories_burned NUMBER(10,2),
    -- Engagement metrics
    total_check_ins NUMBER,
    avg_engagement_score NUMBER(10,2),
    high_engagement_members NUMBER,
    at_risk_members NUMBER,
    -- Revenue metrics (placeholder for future integration)
    daily_revenue NUMBER(10,2),
    avg_revenue_per_member NUMBER(10,2),
    -- Metadata
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

CREATE INDEX idx_agg_daily_kpi_date ON AGG_DAILY_KPI(kpi_date);

-- ============================================================================
-- Verification queries
-- ============================================================================

-- Show all dimension tables
SHOW TABLES IN SCHEMA ANALYTICS_FITNESS_DB.DIMENSIONS;

-- Show all fact tables
SHOW TABLES IN SCHEMA ANALYTICS_FITNESS_DB.FACTS;

-- Show all aggregate tables
SHOW TABLES IN SCHEMA ANALYTICS_FITNESS_DB.AGGREGATES;

-- Verify foreign key relationships
SHOW IMPORTED KEYS IN SCHEMA ANALYTICS_FITNESS_DB.FACTS;

SELECT 'ANALYTICS layer star schema created successfully!' AS status;
