# Health & Fitness Analytics Platform - Setup Guide

**Author:** [Miguel Nemenzo]  
**Date:** December 2025

---

## Introduction

This guide provides step-by-step instructions to set up and run the Health & Fitness Analytics Platform project. Following these steps will allow you to replicate the data warehouse environment in Snowflake, run the ETL pipeline, and view the final dashboards in Power BI.

---

## 1. Prerequisites

Before you begin, ensure you have the following:

- **Snowflake Account**: An active Snowflake account with `SYSADMIN` role access or equivalent permissions to create databases, schemas, and tables.
- **Python**: Version 3.10 or higher.
- **Power BI Desktop**: The latest version installed on your machine.
- **Git**: For cloning the project repository.

---

## 2. Environment Setup

### Step 2.1: Clone the Project Repository

Open your terminal or command prompt and clone the project repository from GitHub.

```bash
# Replace with the actual repository URL
git clone https://github.com/your-username/fitness-analytics-platform.git
cd fitness-analytics-platform
```

### Step 2.2: Install Python Dependencies

It is recommended to use a virtual environment to manage Python packages.

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
# venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install the required packages
pip install -r requirements.txt
```

### Step 2.3: Configure Snowflake Credentials

Securely configure your Snowflake connection details.

1.  **Navigate to the scripts directory**:
    ```bash
    cd scripts
    ```

2.  **Edit the configuration file**:
    Open `config.py` in a text editor.

3.  **Update `SNOWFLAKE_CONFIG`**:
    Modify the `SNOWFLAKE_CONFIG` dictionary with your Snowflake account information.

    ```python
    SNOWFLAKE_CONFIG = {
        "account": "YOUR_SNOWFLAKE_ACCOUNT_LOCATOR",  # e.g., xy12345.us-east-1
        "user": "YOUR_SNOWFLAKE_USERNAME",
        "password": "YOUR_SNOWFLAKE_PASSWORD",
        "warehouse": "COMPUTE_WH",
        "role": "SYSADMIN",
        "database": "RAW_FITNESS_DB",
        "schema": "STAGING"
    }
    ```

    **Security Note**: For a production setup, it is strongly recommended to use environment variables or a secrets management tool (like AWS Secrets Manager or HashiCorp Vault) instead of hardcoding credentials.

---

## 3. Data Generation and Warehouse Setup

### Step 3.1: Generate Sample Data

This script creates the raw CSV data files that the ETL pipeline will ingest.

```bash
# Ensure you are in the scripts/ directory
python 02_generate_sample_data.py
```

After running, you should see several `_sample.csv` files in the `data/` directory.

### Step 3.2: Execute Snowflake SQL Scripts

Log in to your Snowflake account via the web interface (Snowsight) and open a new worksheet. Execute the following SQL scripts in the specified order. You must use a role with permissions to create databases (e.g., `SYSADMIN`).

1.  **`sql/01_create_databases.sql`**
    - **Purpose**: Creates the `RAW_FITNESS_DB`, `CURATED_FITNESS_DB`, and `ANALYTICS_FITNESS_DB` databases.
    - **Instructions**: Copy the entire content of this file into your Snowflake worksheet and run it.

2.  **`sql/02_create_raw_tables.sql`**
    - **Purpose**: Creates the staging tables in the `RAW_FITNESS_DB`.
    - **Instructions**: Copy and run the full script.

3.  **`sql/03_create_analytics_star_schema.sql`**
    - **Purpose**: Builds the star schema (dimension and fact tables) in the `ANALYTICS_FITNESS_DB`.
    - **Instructions**: Copy and run the full script.

4.  **`sql/04_populate_date_time_dimensions.sql`**
    - **Purpose**: Populates the `DIM_DATE` and `DIM_TIME` tables with data.
    - **Instructions**: Copy and run the full script.

---

## 4. Running the ETL Pipeline

### Step 4.1: Load Data into the RAW Layer

This Python script reads the generated CSV files and loads them into the staging tables in your Snowflake `RAW_FITNESS_DB`.

1.  **Uncomment the execution line**:
    - Open `scripts/03_etl_pipeline.py`.
    - Go to the `main()` function at the bottom of the file.
    - Uncomment the line `success = pipeline.run_pipeline()`.

2.  **Run the script**:
    ```bash
    # Ensure you are in the scripts/ directory
    python 03_etl_pipeline.py
    ```

    You will see log output in your terminal as the script processes and loads each data file. Check the `logs/etl_pipeline.log` file for detailed execution logs.

### Step 4.2: Transform Data in Snowflake

Return to your Snowflake worksheet and execute the final set of SQL scripts to process the data through the warehouse layers.

1.  **`sql/05_transform_raw_to_curated.sql`**
    - **Purpose**: Cleans, validates, and transforms data from the RAW layer into the CURATED layer.
    - **Instructions**: Copy and run the full script.

2.  **`sql/06_transform_curated_to_analytics.sql`**
    - **Purpose**: Populates the final star schema in the ANALYTICS layer from the CURATED data.
    - **Instructions**: Copy and run the full script.

At this point, your Snowflake data warehouse is fully populated and ready for analytics.

---

## 5. Connecting Power BI

### Step 5.1: Open the Power BI File

Navigate to the root of the project directory and open the `Health_Fitness_Analytics.pbix` file in Power BI Desktop.

### Step 5.2: Configure Data Source Credentials

Power BI will likely prompt you that the credentials for the data source are required.

1.  In the yellow warning banner, click **"Edit Credentials"**.
2.  In the Snowflake connection dialog, ensure the following are correct:
    - **Server**: `YOUR_SNOWFLAKE_ACCOUNT_LOCATOR.snowflakecomputing.com`
    - **Warehouse**: `COMPUTE_WH`
3.  Select your authentication method (e.g., **Username/Password**) and enter the same credentials you configured in `config.py`.
4.  Click **"Connect"**.

### Step 5.3: Refresh the Data

Once connected, click the **"Refresh"** button in the Home ribbon of Power BI Desktop. This will pull the data from your `ANALYTICS_FITNESS_DB` and populate all the visuals in the dashboard.

---

## 6. Troubleshooting

- **Python `Permission denied` error**: If you encounter permission errors during `pip install`, try running `pip install --user -r requirements.txt` or ensure you have the necessary permissions to write to your Python site-packages directory.
- **Snowflake Connection Error**: Double-check your account locator, username, and password in `config.py`. Ensure your network firewall allows outbound connections to your Snowflake instance.
- **Power BI Connection Issues**: Verify that the server and warehouse names are correct. Ensure the user has `USAGE` privileges on the `ANALYTICS_FITNESS_DB` and `SELECT` privileges on all tables within it.
- **Empty Visuals in Power BI**: If visuals are empty after refreshing, go to the **Transform Data** window in Power BI to check if the tables are being loaded correctly. Also, verify in Snowflake that the `ANALYTICS_FITNESS_DB` tables contain data.

---

Congratulations! Your Health & Fitness Analytics Platform is now fully set up.
