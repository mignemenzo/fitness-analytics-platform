# Quick Start Guide - Health & Fitness Analytics Platform

**Get up and running in 30 minutes!**

---

## Prerequisites Checklist

- [ ] Snowflake account with SYSADMIN privileges
- [ ] Python 3.10+ installed
- [ ] Power BI Desktop installed
- [ ] 15 minutes of setup time

---

## 5-Step Setup Process

### Step 1: Generate Sample Data (2 minutes)

```bash
cd fitness-analytics-platform/scripts
python 02_generate_sample_data.py
```

**Expected Output**: 6 CSV files in the `data/` directory

---

### Step 2: Configure Snowflake (3 minutes)

1. Open `scripts/config.py`
2. Update these three values:
   ```python
   "account": "xy12345.us-east-1",  # Your Snowflake account
   "user": "your_username",
   "password": "your_password"
   ```

---

### Step 3: Run Snowflake SQL Scripts (10 minutes)

Log into Snowflake and execute these scripts **in order**:

1. ✅ `sql/01_create_databases.sql` - Creates 3 databases
2. ✅ `sql/02_create_raw_tables.sql` - Creates staging tables
3. ✅ `sql/03_create_analytics_star_schema.sql` - Creates star schema
4. ✅ `sql/04_populate_date_time_dimensions.sql` - Populates date/time tables

**Tip**: Copy the entire script content into a Snowflake worksheet and click "Run All"

---

### Step 4: Load Data with Python (5 minutes)

```bash
# In scripts/03_etl_pipeline.py, uncomment this line:
# success = pipeline.run_pipeline()

python 03_etl_pipeline.py
```

Then run these final SQL scripts in Snowflake:

5. ✅ `sql/05_transform_raw_to_curated.sql` - Cleans data
6. ✅ `sql/06_transform_curated_to_analytics.sql` - Populates analytics layer

---

### Step 5: Open Power BI Dashboard (10 minutes)

1. Open `Health_Fitness_Analytics.pbix` in Power BI Desktop
2. Click "Edit Credentials" when prompted
3. Enter your Snowflake credentials
4. Click "Refresh" to load data

**Done!** 🎉

---

## Verification Checklist

Run these queries in Snowflake to verify data loaded correctly:

```sql
-- Should return 3 databases
SHOW DATABASES LIKE '%FITNESS%';

-- Should return record counts
SELECT 'Members' AS table_name, COUNT(*) FROM ANALYTICS_FITNESS_DB.DIMENSIONS.DIM_MEMBER
UNION ALL
SELECT 'Workouts', COUNT(*) FROM ANALYTICS_FITNESS_DB.FACTS.FACT_WORKOUT_ACTIVITY
UNION ALL
SELECT 'Nutrition', COUNT(*) FROM ANALYTICS_FITNESS_DB.FACTS.FACT_NUTRITION_INTAKE;
```

**Expected Results**:
- Members: ~1,000
- Workouts: ~5,000
- Nutrition: ~3,000

---

## Troubleshooting

**Problem**: Python can't connect to Snowflake  
**Solution**: Double-check account locator format (should be `account.region`)

**Problem**: Power BI shows empty visuals  
**Solution**: Verify data loaded in Snowflake using verification queries above

**Problem**: SQL script errors  
**Solution**: Ensure you're running as SYSADMIN role

---

## Next Steps

- Customize the dashboards with your own branding
- Add your contact information to README.md
- Upload to GitHub and share with recruiters
- Add this project to your LinkedIn portfolio

---

**Need Help?** Check the full [SETUP_GUIDE.md](docs/SETUP_GUIDE.md) for detailed instructions.
