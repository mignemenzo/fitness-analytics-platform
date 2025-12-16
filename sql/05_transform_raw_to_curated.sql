/*
================================================================================
Health & Fitness Analytics Platform - RAW to CURATED Transformations
================================================================================
Author: Miguel Nemenzo
Date: December 2025
Purpose: Transform and clean data from RAW layer to CURATED layer

This script applies data cleaning, validation, and standardization rules
to prepare data for analytics.
================================================================================
*/

USE ROLE SYSADMIN;
USE WAREHOUSE COMPUTE_WH;
USE SCHEMA CURATED_FITNESS_DB.FITNESS_DATA;

-- ============================================================================
-- CURATED_EXERCISES: Cleaned exercise catalog
-- ============================================================================

CREATE OR REPLACE TABLE CURATED_EXERCISES AS
SELECT
    raw_exercise_id,
    TRIM(UPPER(exercise_name)) AS exercise_name,
    LOWER(exercise_type) AS exercise_type,
    LOWER(muscle_group) AS muscle_group,
    LOWER(difficulty_level) AS difficulty_level,
    equipments,
    instructions,
    safety_info,
    -- Derived fields
    CASE 
        WHEN muscle_group IN ('chest', 'shoulders', 'triceps', 'biceps', 'back', 'forearms') 
        THEN 'Upper Body'
        WHEN muscle_group IN ('legs', 'quadriceps', 'hamstrings', 'glutes', 'calves') 
        THEN 'Lower Body'
        WHEN muscle_group IN ('abs', 'core') 
        THEN 'Core'
        ELSE 'Other'
    END AS muscle_group_category,
    CASE difficulty_level
        WHEN 'beginner' THEN 1
        WHEN 'intermediate' THEN 2
        WHEN 'expert' THEN 3
        ELSE 0
    END AS difficulty_score,
    CASE 
        WHEN exercise_type = 'cardio' THEN TRUE
        ELSE FALSE
    END AS is_cardio,
    -- Metadata
    source_system,
    load_timestamp,
    batch_id,
    CURRENT_TIMESTAMP() AS curated_timestamp
FROM RAW_FITNESS_DB.STAGING.RAW_EXERCISES
WHERE exercise_name IS NOT NULL
  AND exercise_type IS NOT NULL
  AND muscle_group IS NOT NULL;

-- ============================================================================
-- CURATED_NUTRITION: Cleaned nutrition data
-- ============================================================================

CREATE OR REPLACE TABLE CURATED_NUTRITION AS
SELECT
    raw_nutrition_id,
    TRIM(food_name) AS food_name,
    COALESCE(calories, 0) AS calories,
    COALESCE(serving_size_g, 100) AS serving_size_g,
    COALESCE(fat_total_g, 0) AS fat_total_g,
    COALESCE(fat_saturated_g, 0) AS fat_saturated_g,
    COALESCE(protein_g, 0) AS protein_g,
    COALESCE(sodium_mg, 0) AS sodium_mg,
    COALESCE(potassium_mg, 0) AS potassium_mg,
    COALESCE(cholesterol_mg, 0) AS cholesterol_mg,
    COALESCE(carbohydrates_total_g, 0) AS carbohydrates_total_g,
    COALESCE(fiber_g, 0) AS fiber_g,
    COALESCE(sugar_g, 0) AS sugar_g,
    -- Derived fields: Normalize to 100g
    ROUND((calories / NULLIF(serving_size_g, 0)) * 100, 2) AS calories_per_100g,
    ROUND((protein_g / NULLIF(serving_size_g, 0)) * 100, 2) AS protein_per_100g,
    ROUND((carbohydrates_total_g / NULLIF(serving_size_g, 0)) * 100, 2) AS carbs_per_100g,
    ROUND((fat_total_g / NULLIF(serving_size_g, 0)) * 100, 2) AS fat_per_100g,
    ROUND((fiber_g / NULLIF(serving_size_g, 0)) * 100, 2) AS fiber_per_100g,
    -- Food category classification
    CASE
        WHEN protein_per_100g > 20 THEN 'High Protein'
        WHEN carbs_per_100g > 50 THEN 'High Carb'
        WHEN fat_per_100g > 30 THEN 'High Fat'
        ELSE 'Balanced'
    END AS macro_profile,
    CASE 
        WHEN protein_per_100g > 15 THEN TRUE
        ELSE FALSE
    END AS is_high_protein,
    CASE 
        WHEN carbs_per_100g < 10 THEN TRUE
        ELSE FALSE
    END AS is_low_carb,
    -- Metadata
    source_system,
    load_timestamp,
    batch_id,
    CURRENT_TIMESTAMP() AS curated_timestamp
FROM RAW_FITNESS_DB.STAGING.RAW_NUTRITION
WHERE food_name IS NOT NULL
  AND calories >= 0
  AND serving_size_g > 0;

-- ============================================================================
-- CURATED_MEMBERS: Cleaned member profiles
-- ============================================================================

CREATE OR REPLACE TABLE CURATED_MEMBERS AS
SELECT
    raw_member_id,
    member_id,
    TRIM(first_name) AS first_name,
    TRIM(last_name) AS last_name,
    TRIM(first_name) || ' ' || TRIM(last_name) AS full_name,
    LOWER(TRIM(email)) AS email,
    age,
    CASE
        WHEN age BETWEEN 18 AND 25 THEN '18-25'
        WHEN age BETWEEN 26 AND 35 THEN '26-35'
        WHEN age BETWEEN 36 AND 45 THEN '36-45'
        WHEN age BETWEEN 46 AND 55 THEN '46-55'
        WHEN age > 55 THEN '55+'
        ELSE 'Unknown'
    END AS age_group,
    gender,
    membership_type,
    membership_status,
    join_date,
    DATEDIFF(day, join_date, CURRENT_DATE()) AS tenure_days,
    ROUND(DATEDIFF(day, join_date, CURRENT_DATE()) / 30.0, 1) AS tenure_months,
    CASE
        WHEN DATEDIFF(day, join_date, CURRENT_DATE()) < 90 THEN 'New'
        WHEN DATEDIFF(day, join_date, CURRENT_DATE()) BETWEEN 90 AND 365 THEN 'Regular'
        ELSE 'Veteran'
    END AS tenure_category,
    fitness_goal,
    height_cm,
    initial_weight_kg,
    ROUND(initial_weight_kg / POWER(height_cm / 100.0, 2), 2) AS bmi,
    CASE
        WHEN initial_weight_kg / POWER(height_cm / 100.0, 2) < 18.5 THEN 'Underweight'
        WHEN initial_weight_kg / POWER(height_cm / 100.0, 2) BETWEEN 18.5 AND 24.9 THEN 'Normal'
        WHEN initial_weight_kg / POWER(height_cm / 100.0, 2) BETWEEN 25 AND 29.9 THEN 'Overweight'
        ELSE 'Obese'
    END AS bmi_category,
    -- Metadata
    source_system,
    load_timestamp,
    batch_id,
    CURRENT_TIMESTAMP() AS curated_timestamp
FROM RAW_FITNESS_DB.STAGING.RAW_MEMBERS
WHERE member_id IS NOT NULL
  AND email IS NOT NULL
  AND join_date IS NOT NULL;

-- ============================================================================
-- CURATED_WORKOUT_LOGS: Cleaned workout activity logs
-- ============================================================================

CREATE OR REPLACE TABLE CURATED_WORKOUT_LOGS AS
SELECT
    raw_workout_log_id,
    workout_log_id,
    member_id,
    workout_date,
    workout_time,
    TRIM(exercise_name) AS exercise_name,
    exercise_type,
    muscle_group,
    COALESCE(sets, 0) AS sets,
    COALESCE(reps, 0) AS reps,
    COALESCE(weight_kg, 0) AS weight_kg,
    COALESCE(duration_minutes, 0) AS duration_minutes,
    COALESCE(calories_burned, 0) AS calories_burned,
    difficulty_rating,
    notes,
    -- Derived metrics
    ROUND(sets * reps * weight_kg, 2) AS total_volume_kg,
    CASE
        WHEN weight_kg > 0 AND reps > 0 THEN 
            ROUND((weight_kg * reps * sets) / NULLIF(duration_minutes, 0), 2)
        ELSE 0
    END AS intensity_score,
    CASE
        WHEN duration_minutes >= 45 AND difficulty_rating >= 7 THEN 'High Quality'
        WHEN duration_minutes >= 30 AND difficulty_rating >= 5 THEN 'Good Quality'
        ELSE 'Standard'
    END AS workout_quality,
    -- Metadata
    source_system,
    load_timestamp,
    batch_id,
    CURRENT_TIMESTAMP() AS curated_timestamp
FROM RAW_FITNESS_DB.STAGING.RAW_WORKOUT_LOGS
WHERE workout_log_id IS NOT NULL
  AND member_id IS NOT NULL
  AND workout_date IS NOT NULL;

-- ============================================================================
-- CURATED_NUTRITION_LOGS: Cleaned nutrition intake logs
-- ============================================================================

CREATE OR REPLACE TABLE CURATED_NUTRITION_LOGS AS
SELECT
    raw_nutrition_log_id,
    nutrition_log_id,
    member_id,
    log_date,
    meal_type,
    TRIM(food_item) AS food_item,
    serving_size_g,
    servings,
    COALESCE(calories, 0) AS calories,
    COALESCE(protein_g, 0) AS protein_g,
    COALESCE(carbs_g, 0) AS carbs_g,
    COALESCE(fat_g, 0) AS fat_g,
    COALESCE(fiber_g, 0) AS fiber_g,
    COALESCE(sugar_g, 0) AS sugar_g,
    -- Derived metrics
    ROUND(protein_g * 4, 2) AS protein_calories,
    ROUND(carbs_g * 4, 2) AS carbs_calories,
    ROUND(fat_g * 9, 2) AS fat_calories,
    ROUND((protein_g / NULLIF(protein_g + carbs_g + fat_g, 0)) * 100, 1) AS protein_percentage,
    ROUND((carbs_g / NULLIF(protein_g + carbs_g + fat_g, 0)) * 100, 1) AS carbs_percentage,
    ROUND((fat_g / NULLIF(protein_g + carbs_g + fat_g, 0)) * 100, 1) AS fat_percentage,
    -- Metadata
    source_system,
    load_timestamp,
    batch_id,
    CURRENT_TIMESTAMP() AS curated_timestamp
FROM RAW_FITNESS_DB.STAGING.RAW_NUTRITION_LOGS
WHERE nutrition_log_id IS NOT NULL
  AND member_id IS NOT NULL
  AND log_date IS NOT NULL;

-- ============================================================================
-- CURATED_MEMBER_ENGAGEMENT: Cleaned engagement metrics
-- ============================================================================

CREATE OR REPLACE TABLE CURATED_MEMBER_ENGAGEMENT AS
SELECT
    raw_engagement_id,
    engagement_id,
    member_id,
    record_date,
    COALESCE(check_ins, 0) AS check_ins,
    COALESCE(app_logins, 0) AS app_logins,
    COALESCE(classes_attended, 0) AS classes_attended,
    COALESCE(trainer_sessions, 0) AS trainer_sessions,
    COALESCE(engagement_score, 0) AS engagement_score,
    -- Derived metrics
    (COALESCE(check_ins, 0) + COALESCE(app_logins, 0) + 
     COALESCE(classes_attended, 0) + COALESCE(trainer_sessions, 0)) AS total_interactions,
    CASE
        WHEN engagement_score >= 70 THEN 'High'
        WHEN engagement_score >= 40 THEN 'Medium'
        ELSE 'Low'
    END AS engagement_level,
    CASE
        WHEN engagement_score < 30 AND check_ins < 2 THEN TRUE
        ELSE FALSE
    END AS is_at_risk,
    -- Metadata
    source_system,
    load_timestamp,
    batch_id,
    CURRENT_TIMESTAMP() AS curated_timestamp
FROM RAW_FITNESS_DB.STAGING.RAW_MEMBER_ENGAGEMENT
WHERE engagement_id IS NOT NULL
  AND member_id IS NOT NULL
  AND record_date IS NOT NULL;

-- ============================================================================
-- Data Quality Checks
-- ============================================================================

-- Check record counts
SELECT 'CURATED_EXERCISES' AS table_name, COUNT(*) AS record_count FROM CURATED_EXERCISES
UNION ALL
SELECT 'CURATED_NUTRITION', COUNT(*) FROM CURATED_NUTRITION
UNION ALL
SELECT 'CURATED_MEMBERS', COUNT(*) FROM CURATED_MEMBERS
UNION ALL
SELECT 'CURATED_WORKOUT_LOGS', COUNT(*) FROM CURATED_WORKOUT_LOGS
UNION ALL
SELECT 'CURATED_NUTRITION_LOGS', COUNT(*) FROM CURATED_NUTRITION_LOGS
UNION ALL
SELECT 'CURATED_MEMBER_ENGAGEMENT', COUNT(*) FROM CURATED_MEMBER_ENGAGEMENT;

SELECT 'RAW to CURATED transformation completed successfully!' AS status;
