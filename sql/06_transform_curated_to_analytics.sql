/*
================================================================================
Health & Fitness Analytics Platform - CURATED to ANALYTICS Transformations
================================================================================
Author: Miguel Nemenzo
Date: December 2025
Purpose: Populate star schema in ANALYTICS layer from CURATED layer

This script populates dimension and fact tables optimized for Power BI reporting.
================================================================================
*/

USE ROLE SYSADMIN;
USE WAREHOUSE COMPUTE_WH;

-- ============================================================================
-- POPULATE DIMENSION TABLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- DIM_EXERCISE: Exercise dimension
-- ----------------------------------------------------------------------------

USE SCHEMA ANALYTICS_FITNESS_DB.DIMENSIONS;

INSERT INTO DIM_EXERCISE (
    exercise_name,
    exercise_type,
    exercise_category,
    muscle_group,
    muscle_group_category,
    difficulty_level,
    difficulty_score,
    equipments,
    equipment_category,
    is_compound_exercise,
    is_cardio,
    instructions,
    safety_info
)
SELECT DISTINCT
    exercise_name,
    exercise_type,
    CASE exercise_type
        WHEN 'strength' THEN 'Resistance Training'
        WHEN 'cardio' THEN 'Cardiovascular'
        WHEN 'stretching' THEN 'Flexibility'
        ELSE 'Other'
    END AS exercise_category,
    muscle_group,
    muscle_group_category,
    difficulty_level,
    difficulty_score,
    equipments,
    CASE
        WHEN equipments LIKE '%barbell%' OR equipments LIKE '%dumbbell%' THEN 'Free Weights'
        WHEN equipments LIKE '%machine%' THEN 'Machines'
        WHEN equipments LIKE '%bodyweight%' OR equipments = '' THEN 'Bodyweight'
        ELSE 'Mixed Equipment'
    END AS equipment_category,
    CASE
        WHEN muscle_group_category IN ('Upper Body', 'Lower Body') 
             AND exercise_type = 'strength' THEN TRUE
        ELSE FALSE
    END AS is_compound_exercise,
    is_cardio,
    instructions,
    safety_info
FROM CURATED_FITNESS_DB.FITNESS_DATA.CURATED_EXERCISES;

-- ----------------------------------------------------------------------------
-- DIM_NUTRITION: Nutrition dimension
-- ----------------------------------------------------------------------------

INSERT INTO DIM_NUTRITION (
    food_name,
    food_category,
    is_high_protein,
    is_low_carb,
    is_healthy_fat,
    calories_per_100g,
    protein_per_100g,
    carbs_per_100g,
    fat_per_100g,
    fiber_per_100g,
    macro_profile
)
SELECT DISTINCT
    food_name,
    CASE
        WHEN macro_profile = 'High Protein' THEN 'Protein Source'
        WHEN macro_profile = 'High Carb' THEN 'Carbohydrate Source'
        WHEN macro_profile = 'High Fat' THEN 'Fat Source'
        ELSE 'Balanced Food'
    END AS food_category,
    is_high_protein,
    is_low_carb,
    CASE WHEN fat_per_100g > 20 AND fat_saturated_g < 5 THEN TRUE ELSE FALSE END AS is_healthy_fat,
    calories_per_100g,
    protein_per_100g,
    carbs_per_100g,
    fat_per_100g,
    fiber_per_100g,
    macro_profile
FROM CURATED_FITNESS_DB.FITNESS_DATA.CURATED_NUTRITION;

-- ----------------------------------------------------------------------------
-- DIM_MEMBER: Member dimension (SCD Type 2)
-- ----------------------------------------------------------------------------

INSERT INTO DIM_MEMBER (
    member_id,
    first_name,
    last_name,
    full_name,
    email,
    age,
    age_group,
    gender,
    membership_type,
    membership_status,
    join_date,
    tenure_days,
    tenure_months,
    tenure_category,
    fitness_goal,
    height_cm,
    initial_weight_kg,
    bmi_category,
    effective_date,
    expiration_date,
    is_current,
    version
)
SELECT
    member_id,
    first_name,
    last_name,
    full_name,
    email,
    age,
    age_group,
    gender,
    membership_type,
    membership_status,
    join_date,
    tenure_days,
    tenure_months,
    tenure_category,
    fitness_goal,
    height_cm,
    initial_weight_kg,
    bmi_category,
    join_date AS effective_date,
    NULL AS expiration_date,
    TRUE AS is_current,
    1 AS version
FROM CURATED_FITNESS_DB.FITNESS_DATA.CURATED_MEMBERS;

-- ============================================================================
-- POPULATE FACT TABLES
-- ============================================================================

USE SCHEMA ANALYTICS_FITNESS_DB.FACTS;

-- ----------------------------------------------------------------------------
-- FACT_WORKOUT_ACTIVITY: Workout fact table
-- ----------------------------------------------------------------------------

INSERT INTO FACT_WORKOUT_ACTIVITY (
    workout_log_id,
    member_key,
    exercise_key,
    workout_date_key,
    workout_time_key,
    sets,
    reps,
    weight_kg,
    total_volume_kg,
    duration_minutes,
    calories_burned,
    difficulty_rating,
    intensity_score,
    workout_quality_score,
    notes
)
SELECT
    wl.workout_log_id,
    dm.member_key,
    de.exercise_key,
    dd.date_key AS workout_date_key,
    dt.time_key AS workout_time_key,
    wl.sets,
    wl.reps,
    wl.weight_kg,
    wl.total_volume_kg,
    wl.duration_minutes,
    wl.calories_burned,
    wl.difficulty_rating,
    wl.intensity_score,
    CASE wl.workout_quality
        WHEN 'High Quality' THEN 10
        WHEN 'Good Quality' THEN 7
        ELSE 5
    END AS workout_quality_score,
    wl.notes
FROM CURATED_FITNESS_DB.FITNESS_DATA.CURATED_WORKOUT_LOGS wl
INNER JOIN ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_MEMBER dm 
    ON wl.member_id = dm.member_id AND dm.is_current = TRUE
INNER JOIN ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_EXERCISE de 
    ON wl.exercise_name = de.exercise_name
INNER JOIN ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_DATE dd 
    ON wl.workout_date = dd.full_date
LEFT JOIN ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_TIME dt 
    ON wl.workout_time = dt.time_value;

-- ----------------------------------------------------------------------------
-- FACT_NUTRITION_INTAKE: Nutrition fact table
-- ----------------------------------------------------------------------------

INSERT INTO FACT_NUTRITION_INTAKE (
    nutrition_log_id,
    member_key,
    nutrition_key,
    log_date_key,
    meal_type,
    serving_size_g,
    servings,
    calories,
    protein_g,
    carbs_g,
    fat_g,
    fiber_g,
    sugar_g,
    protein_calories,
    carbs_calories,
    fat_calories,
    macro_balance_score
)
SELECT
    nl.nutrition_log_id,
    dm.member_key,
    dn.nutrition_key,
    dd.date_key AS log_date_key,
    nl.meal_type,
    nl.serving_size_g,
    nl.servings,
    nl.calories,
    nl.protein_g,
    nl.carbs_g,
    nl.fat_g,
    nl.fiber_g,
    nl.sugar_g,
    nl.protein_calories,
    nl.carbs_calories,
    nl.fat_calories,
    -- Calculate macro balance score (higher is more balanced)
    100 - (ABS(nl.protein_percentage - 33.3) + 
           ABS(nl.carbs_percentage - 33.3) + 
           ABS(nl.fat_percentage - 33.3)) AS macro_balance_score
FROM CURATED_FITNESS_DB.FITNESS_DATA.CURATED_NUTRITION_LOGS nl
INNER JOIN ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_MEMBER dm 
    ON nl.member_id = dm.member_id AND dm.is_current = TRUE
INNER JOIN ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_NUTRITION dn 
    ON nl.food_item = dn.food_name
INNER JOIN ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_DATE dd 
    ON nl.log_date = dd.full_date;

-- ----------------------------------------------------------------------------
-- FACT_MEMBER_ENGAGEMENT: Engagement fact table
-- ----------------------------------------------------------------------------

INSERT INTO FACT_MEMBER_ENGAGEMENT (
    engagement_id,
    member_key,
    record_date_key,
    check_ins,
    app_logins,
    classes_attended,
    trainer_sessions,
    engagement_score,
    total_interactions,
    engagement_level,
    is_at_risk
)
SELECT
    me.engagement_id,
    dm.member_key,
    dd.date_key AS record_date_key,
    me.check_ins,
    me.app_logins,
    me.classes_attended,
    me.trainer_sessions,
    me.engagement_score,
    me.total_interactions,
    me.engagement_level,
    me.is_at_risk
FROM CURATED_FITNESS_DB.FITNESS_DATA.CURATED_MEMBER_ENGAGEMENT me
INNER JOIN ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_MEMBER dm 
    ON me.member_id = dm.member_id AND dm.is_current = TRUE
INNER JOIN ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_DATE dd 
    ON me.record_date = dd.full_date;

-- ============================================================================
-- POPULATE AGGREGATE TABLES
-- ============================================================================

USE SCHEMA ANALYTICS_FITNESS_DB.AGGREGATES;

-- ----------------------------------------------------------------------------
-- AGG_MEMBER_MONTHLY_SUMMARY: Monthly member activity summary
-- ----------------------------------------------------------------------------

INSERT INTO AGG_MEMBER_MONTHLY_SUMMARY (
    member_key,
    year_month,
    total_workouts,
    total_workout_duration_minutes,
    total_calories_burned,
    avg_workout_duration,
    unique_exercises,
    most_frequent_muscle_group,
    total_nutrition_logs,
    avg_daily_calories,
    avg_daily_protein_g,
    avg_daily_carbs_g,
    avg_daily_fat_g,
    total_check_ins,
    total_app_logins,
    total_classes_attended,
    avg_engagement_score,
    workout_consistency_score,
    nutrition_adherence_score,
    overall_performance_score
)
SELECT
    dm.member_key,
    dd.year_month,
    -- Workout metrics
    COUNT(DISTINCT fw.workout_fact_key) AS total_workouts,
    SUM(fw.duration_minutes) AS total_workout_duration_minutes,
    SUM(fw.calories_burned) AS total_calories_burned,
    AVG(fw.duration_minutes) AS avg_workout_duration,
    COUNT(DISTINCT fw.exercise_key) AS unique_exercises,
    MODE(de.muscle_group) AS most_frequent_muscle_group,
    -- Nutrition metrics
    COUNT(DISTINCT fn.nutrition_fact_key) AS total_nutrition_logs,
    AVG(daily_nutrition.daily_calories) AS avg_daily_calories,
    AVG(daily_nutrition.daily_protein) AS avg_daily_protein_g,
    AVG(daily_nutrition.daily_carbs) AS avg_daily_carbs_g,
    AVG(daily_nutrition.daily_fat) AS avg_daily_fat_g,
    -- Engagement metrics
    SUM(fe.check_ins) AS total_check_ins,
    SUM(fe.app_logins) AS total_app_logins,
    SUM(fe.classes_attended) AS total_classes_attended,
    AVG(fe.engagement_score) AS avg_engagement_score,
    -- Derived scores
    LEAST(100, (COUNT(DISTINCT fw.workout_date_key) / 30.0) * 100) AS workout_consistency_score,
    LEAST(100, (COUNT(DISTINCT fn.log_date_key) / 30.0) * 100) AS nutrition_adherence_score,
    ROUND((AVG(fw.workout_quality_score) + AVG(fe.engagement_score)) / 2, 2) AS overall_performance_score
FROM ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_MEMBER dm
CROSS JOIN ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_DATE dd
LEFT JOIN ANALYTICS_FITNESS_DB.FACTS.FACT_WORKOUT_ACTIVITY fw 
    ON dm.member_key = fw.member_key 
    AND fw.workout_date_key = dd.date_key
LEFT JOIN ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_EXERCISE de 
    ON fw.exercise_key = de.exercise_key
LEFT JOIN ANALYTICS_FITNESS_DB.FACTS.FACT_NUTRITION_INTAKE fn 
    ON dm.member_key = fn.member_key 
    AND fn.log_date_key = dd.date_key
LEFT JOIN (
    SELECT 
        member_key,
        log_date_key,
        SUM(calories) AS daily_calories,
        SUM(protein_g) AS daily_protein,
        SUM(carbs_g) AS daily_carbs,
        SUM(fat_g) AS daily_fat
    FROM ANALYTICS_FITNESS_DB.FACTS.FACT_NUTRITION_INTAKE
    GROUP BY member_key, log_date_key
) daily_nutrition 
    ON dm.member_key = daily_nutrition.member_key 
    AND dd.date_key = daily_nutrition.log_date_key
LEFT JOIN ANALYTICS_FITNESS_DB.FACTS.FACT_MEMBER_ENGAGEMENT fe 
    ON dm.member_key = fe.member_key 
    AND fe.record_date_key = dd.date_key
WHERE dm.is_current = TRUE
  AND dd.year_month >= DATE_TRUNC('month', DATEADD(month, -12, CURRENT_DATE()))
GROUP BY dm.member_key, dd.year_month
HAVING total_workouts > 0 OR total_nutrition_logs > 0 OR total_check_ins > 0;

-- ----------------------------------------------------------------------------
-- AGG_DAILY_KPI: Daily KPI metrics for executive dashboard
-- ----------------------------------------------------------------------------

INSERT INTO AGG_DAILY_KPI (
    kpi_date,
    total_members,
    active_members,
    new_members,
    churned_members,
    member_retention_rate,
    total_workouts,
    total_workout_minutes,
    avg_workouts_per_member,
    total_calories_burned,
    total_check_ins,
    avg_engagement_score,
    high_engagement_members,
    at_risk_members,
    daily_revenue,
    avg_revenue_per_member
)
SELECT
    dd.full_date AS kpi_date,
    -- Member metrics
    COUNT(DISTINCT dm.member_key) AS total_members,
    COUNT(DISTINCT CASE WHEN dm.membership_status = 'Active' THEN dm.member_key END) AS active_members,
    COUNT(DISTINCT CASE WHEN dm.join_date = dd.full_date THEN dm.member_key END) AS new_members,
    0 AS churned_members, -- Placeholder for churn calculation
    ROUND((COUNT(DISTINCT CASE WHEN dm.membership_status = 'Active' THEN dm.member_key END) * 100.0) / 
          NULLIF(COUNT(DISTINCT dm.member_key), 0), 2) AS member_retention_rate,
    -- Activity metrics
    COUNT(DISTINCT fw.workout_fact_key) AS total_workouts,
    SUM(fw.duration_minutes) AS total_workout_minutes,
    ROUND(COUNT(DISTINCT fw.workout_fact_key) * 1.0 / 
          NULLIF(COUNT(DISTINCT dm.member_key), 0), 2) AS avg_workouts_per_member,
    SUM(fw.calories_burned) AS total_calories_burned,
    -- Engagement metrics
    SUM(fe.check_ins) AS total_check_ins,
    AVG(fe.engagement_score) AS avg_engagement_score,
    COUNT(DISTINCT CASE WHEN fe.engagement_level = 'High' THEN fe.member_key END) AS high_engagement_members,
    COUNT(DISTINCT CASE WHEN fe.is_at_risk = TRUE THEN fe.member_key END) AS at_risk_members,
    -- Revenue metrics (placeholder)
    0 AS daily_revenue,
    0 AS avg_revenue_per_member
FROM ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_DATE dd
CROSS JOIN ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_MEMBER dm
LEFT JOIN ANALYTICS_FITNESS_DB.FACTS.FACT_WORKOUT_ACTIVITY fw 
    ON dm.member_key = fw.member_key 
    AND fw.workout_date_key = dd.date_key
LEFT JOIN ANALYTICS_FITNESS_DB.FACTS.FACT_MEMBER_ENGAGEMENT fe 
    ON dm.member_key = fe.member_key 
    AND fe.record_date_key = dd.date_key
WHERE dd.full_date >= DATEADD(day, -90, CURRENT_DATE())
  AND dm.is_current = TRUE
GROUP BY dd.full_date
ORDER BY dd.full_date;

-- ============================================================================
-- Verification Queries
-- ============================================================================

-- Check dimension table counts
SELECT 'DIM_MEMBER' AS table_name, COUNT(*) AS record_count FROM ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_MEMBER
UNION ALL
SELECT 'DIM_EXERCISE', COUNT(*) FROM ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_EXERCISE
UNION ALL
SELECT 'DIM_NUTRITION', COUNT(*) FROM ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_NUTRITION;

-- Check fact table counts
SELECT 'FACT_WORKOUT_ACTIVITY' AS table_name, COUNT(*) AS record_count FROM ANALYTICS_FITNESS_DB.FACTS.FACT_WORKOUT_ACTIVITY
UNION ALL
SELECT 'FACT_NUTRITION_INTAKE', COUNT(*) FROM ANALYTICS_FITNESS_DB.FACTS.FACT_NUTRITION_INTAKE
UNION ALL
SELECT 'FACT_MEMBER_ENGAGEMENT', COUNT(*) FROM ANALYTICS_FITNESS_DB.FACTS.FACT_MEMBER_ENGAGEMENT;

-- Check aggregate table counts
SELECT 'AGG_MEMBER_MONTHLY_SUMMARY' AS table_name, COUNT(*) AS record_count FROM ANALYTICS_FITNESS_DB.AGGREGATES.AGG_MEMBER_MONTHLY_SUMMARY
UNION ALL
SELECT 'AGG_DAILY_KPI', COUNT(*) FROM ANALYTICS_FITNESS_DB.AGGREGATES.AGG_DAILY_KPI;

SELECT 'CURATED to ANALYTICS transformation completed successfully!' AS status;
