/*
================================================================================
Health & Fitness Analytics Platform - Populate Date & Time Dimensions
================================================================================
Author: Miguel Nemenzo
Date: December 2025
Purpose: Populate DIM_DATE and DIM_TIME dimensions with comprehensive data

This script generates date records from 2020 to 2030 and all possible time values.
================================================================================
*/

USE ROLE SYSADMIN;
USE WAREHOUSE COMPUTE_WH;
USE SCHEMA ANALYTICS_FITNESS_DB.DIMENSIONS;

-- ============================================================================
-- Populate DIM_DATE dimension (2020-2030)
-- ============================================================================

-- Generate date sequence using recursive CTE
INSERT INTO DIM_DATE (
    date_key,
    full_date,
    day_of_week,
    day_name,
    day_of_month,
    day_of_year,
    week_of_year,
    month_number,
    month_name,
    month_abbr,
    quarter,
    quarter_name,
    year,
    year_month,
    year_quarter,
    is_weekend,
    is_holiday,
    holiday_name,
    fiscal_year,
    fiscal_quarter
)
WITH RECURSIVE date_range AS (
    -- Start date
    SELECT DATE('2020-01-01') AS date_value
    UNION ALL
    -- Recursive part: add one day
    SELECT DATEADD(day, 1, date_value)
    FROM date_range
    WHERE date_value < DATE('2030-12-31')
)
SELECT
    TO_NUMBER(TO_CHAR(date_value, 'YYYYMMDD')) AS date_key,
    date_value AS full_date,
    DAYOFWEEK(date_value) AS day_of_week,
    DAYNAME(date_value) AS day_name,
    DAY(date_value) AS day_of_month,
    DAYOFYEAR(date_value) AS day_of_year,
    WEEKOFYEAR(date_value) AS week_of_year,
    MONTH(date_value) AS month_number,
    MONTHNAME(date_value) AS month_name,
    LEFT(MONTHNAME(date_value), 3) AS month_abbr,
    QUARTER(date_value) AS quarter,
    'Q' || QUARTER(date_value) AS quarter_name,
    YEAR(date_value) AS year,
    TO_CHAR(date_value, 'YYYY-MM') AS year_month,
    TO_CHAR(date_value, 'YYYY') || '-Q' || QUARTER(date_value) AS year_quarter,
    CASE WHEN DAYOFWEEK(date_value) IN (0, 6) THEN TRUE ELSE FALSE END AS is_weekend,
    FALSE AS is_holiday, -- Will be updated separately
    NULL AS holiday_name,
    -- Fiscal year (assuming fiscal year starts in January)
    YEAR(date_value) AS fiscal_year,
    QUARTER(date_value) AS fiscal_quarter
FROM date_range;

-- ============================================================================
-- Update holidays in DIM_DATE
-- ============================================================================

-- US Federal Holidays (example - can be expanded)
UPDATE DIM_DATE
SET is_holiday = TRUE,
    holiday_name = 'New Year''s Day'
WHERE month_number = 1 AND day_of_month = 1;

UPDATE DIM_DATE
SET is_holiday = TRUE,
    holiday_name = 'Independence Day'
WHERE month_number = 7 AND day_of_month = 4;

UPDATE DIM_DATE
SET is_holiday = TRUE,
    holiday_name = 'Christmas Day'
WHERE month_number = 12 AND day_of_month = 25;

UPDATE DIM_DATE
SET is_holiday = TRUE,
    holiday_name = 'Thanksgiving'
WHERE month_number = 11 
  AND day_name = 'Thu'
  AND day_of_month BETWEEN 22 AND 28;

-- ============================================================================
-- Populate DIM_TIME dimension (all 24-hour time values at 15-minute intervals)
-- ============================================================================

INSERT INTO DIM_TIME (
    time_key,
    time_value,
    hour,
    minute,
    hour_12,
    am_pm,
    time_of_day,
    is_peak_hours
)
WITH RECURSIVE time_range AS (
    -- Start time: 00:00:00
    SELECT TIME('00:00:00') AS time_value
    UNION ALL
    -- Recursive part: add 15 minutes
    SELECT DATEADD(minute, 15, time_value)
    FROM time_range
    WHERE time_value < TIME('23:45:00')
)
SELECT
    TO_NUMBER(REPLACE(TO_CHAR(time_value, 'HH24:MI'), ':', '')) AS time_key,
    time_value,
    HOUR(time_value) AS hour,
    MINUTE(time_value) AS minute,
    CASE 
        WHEN HOUR(time_value) = 0 THEN 12
        WHEN HOUR(time_value) <= 12 THEN HOUR(time_value)
        ELSE HOUR(time_value) - 12
    END AS hour_12,
    CASE WHEN HOUR(time_value) < 12 THEN 'AM' ELSE 'PM' END AS am_pm,
    CASE
        WHEN HOUR(time_value) BETWEEN 5 AND 11 THEN 'Morning'
        WHEN HOUR(time_value) BETWEEN 12 AND 16 THEN 'Afternoon'
        WHEN HOUR(time_value) BETWEEN 17 AND 20 THEN 'Evening'
        ELSE 'Night'
    END AS time_of_day,
    CASE 
        WHEN HOUR(time_value) BETWEEN 6 AND 9 THEN TRUE  -- Morning peak
        WHEN HOUR(time_value) BETWEEN 17 AND 20 THEN TRUE  -- Evening peak
        ELSE FALSE
    END AS is_peak_hours
FROM time_range;

-- ============================================================================
-- Verification queries
-- ============================================================================

-- Check DIM_DATE population
SELECT 
    'DIM_DATE' AS dimension,
    COUNT(*) AS total_records,
    MIN(full_date) AS min_date,
    MAX(full_date) AS max_date,
    SUM(CASE WHEN is_weekend THEN 1 ELSE 0 END) AS weekend_days,
    SUM(CASE WHEN is_holiday THEN 1 ELSE 0 END) AS holidays
FROM DIM_DATE;

-- Sample DIM_DATE records
SELECT * FROM DIM_DATE 
WHERE year = 2025 AND month_number = 12 
ORDER BY full_date 
LIMIT 10;

-- Check DIM_TIME population
SELECT 
    'DIM_TIME' AS dimension,
    COUNT(*) AS total_records,
    MIN(time_value) AS min_time,
    MAX(time_value) AS max_time,
    SUM(CASE WHEN is_peak_hours THEN 1 ELSE 0 END) AS peak_hour_slots
FROM DIM_TIME;

-- Sample DIM_TIME records
SELECT * FROM DIM_TIME 
WHERE time_of_day = 'Morning'
ORDER BY time_value 
LIMIT 10;

-- Time of day distribution
SELECT 
    time_of_day,
    COUNT(*) AS time_slots,
    SUM(CASE WHEN is_peak_hours THEN 1 ELSE 0 END) AS peak_slots
FROM DIM_TIME
GROUP BY time_of_day
ORDER BY time_of_day;

SELECT 'Date and Time dimensions populated successfully!' AS status;
