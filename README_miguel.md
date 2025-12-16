# Health & Fitness Analytics Platform - Grand Final Version

**Author:** [Miguel Nemenzo] - Data Analyst/Engineer Portfolio Project  
**Date:** December 2025  
**Version:** 2.0 

---

## 1. Project Overview

The **Health & Fitness Analytics Platform** is a comprehensive, end-to-end data engineering and analytics project designed to showcase modern data stack capabilities. This platform ingests data from fitness and health sources, processes it through a multi-layered data warehouse in Snowflake, and provides actionable insights through interactive Power BI dashboards.

This **Grand Final Version** features a production-scale dataset with over **35,000 records**, combining real data from REST APIs with intelligently generated data for a truly impressive portfolio piece.

### Key Features:
- **Real API Integration**: Fetches real exercise and nutrition data from API Ninjas
- **Production-Scale Dataset**: Over 35,000 records for realistic analysis
- **Automated ETL Pipeline**: Python-based pipeline for data extraction, transformation, and loading
- **Three-Layer Data Warehouse**: Scalable and maintainable architecture (RAW, CURATED, ANALYTICS) in Snowflake
- **Star Schema Data Model**: Optimized for analytical queries and Power BI performance
- **Comprehensive Data Model**: Includes dimensions for members, exercises, nutrition, date, and time, and facts for workouts, nutrition intake, and engagement
- **Interactive Power BI Dashboards**: Four detailed dashboards for executive, member, workout, and operational analysis

---

## 2. Architecture

This project utilizes a modern data stack architecture, centered around a three-layer data warehouse in Snowflake.

![Architecture Diagram](docs/architecture.png)  
*(This diagram can be generated based on the `project_architecture.md`)*

### Data Flow

1. **Data Ingestion**: Real data is fetched from REST APIs (API Ninjas) and combined with generated data using Python scripts.
2. **RAW Layer (Snowflake)**: Data is loaded into staging tables with minimal transformation, preserving the original data structure and adding metadata for lineage.
3. **CURATED Layer (Snowflake)**: Data is cleaned, validated, standardized, and enriched with business logic.
4. **ANALYTICS Layer (Snowflake)**: Data is transformed into a star schema, with dimension and fact tables optimized for reporting.
5. **Power BI Dashboards**: Interactive dashboards connect to the ANALYTICS layer using DirectQuery for real-time insights.

---

## 3. The Grand Final Dataset

This version includes a substantial, realistic dataset perfect for demonstrating your skills:

| Dataset | Record Count | Source |
|---|---|---|
| **Exercises** | 165 | 100% from API Ninjas |
| **Nutrition Items** | 85 | 100% from API Ninjas |
| **Members** | 2,500 | Generated |
| **Workout Logs** | 15,000 | Generated (using real exercises) |
| **Nutrition Logs** | 10,000 | Generated (using real food items) |
| **Engagement Records** | 8,000 | Generated |
| **TOTAL** | **35,750** | Hybrid (API + Generated) |

---

## 4. Tech Stack

- **Data Warehouse**: Snowflake
- **ETL/ELT**: Python 3.11, Pandas
- **REST APIs**: API Ninjas (Exercises & Nutrition)
- **Business Intelligence**: Microsoft Power BI
- **Orchestration (Future)**: Apache Airflow or Dagster
- **Infrastructure-as-Code (Future)**: Terraform

---

## 5. Getting Started

### Prerequisites

- **Snowflake Account**: A Snowflake account with `SYSADMIN` or equivalent privileges.
- **Python 3.11**: With `pip` for package management.
- **Power BI Desktop**: For viewing and interacting with the dashboard files.

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository_url>
   cd fitness-analytics-platform
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Snowflake Connection:**
   - Open `scripts/config.py`.
   - Update the `SNOWFLAKE_CONFIG` dictionary with your account details (account, user, password).
   - Your API key is already included!

---

## 6. Usage

### Step 1: Generate the Grand Final Dataset

Run the script to generate the comprehensive dataset. This uses the real API data we fetched and scales it up.

```bash
cd scripts
python 08_generate_grand_final_dataset.py
```

This will create several `_final.csv` files in the `data/` directory.

### Step 2: Set Up Snowflake Environment

Execute the SQL scripts in your Snowflake worksheet in the following order. These scripts must be run by a user with `SYSADMIN` privileges.

1.  `sql/01_create_databases.sql`: Creates the three-layer database architecture.
2.  `sql/02_create_raw_tables.sql`: Creates the staging tables in the RAW layer.
3.  `sql/03_create_analytics_star_schema.sql`: Creates the dimension and fact tables in the ANALYTICS layer.
4.  `sql/04_populate_date_time_dimensions.sql`: Populates the `DIM_DATE` and `DIM_TIME` tables.

### Step 3: Run the ETL Pipeline

Execute the main ETL script to load data from the final CSV files into the Snowflake RAW layer.

```bash
python 03_etl_pipeline.py
```

*Note: You will need to uncomment the `pipeline.run_pipeline()` line in `03_etl_pipeline.py` to perform the actual data load.*

### Step 4: Run Data Transformations in Snowflake

Execute the following SQL scripts in your Snowflake worksheet to transform the data through the layers.

1.  `sql/05_transform_raw_to_curated.sql`: Cleans and transforms data from the RAW to the CURATED layer.
2.  `sql/06_transform_curated_to_analytics.sql`: Populates the ANALYTICS star schema from the CURATED layer.

---

## 7. Power BI Dashboard

### Setup

1.  Open the `Health_Fitness_Analytics.pbix` file in Power BI Desktop.
2.  When prompted, click **"Edit Credentials"** to connect to your Snowflake data source.
3.  Enter your Snowflake server, warehouse, and authentication details.
4.  The dashboards will automatically populate with data from your Snowflake `ANALYTICS_FITNESS_DB`.

### Dashboard Design

For a detailed overview of the dashboard design, including KPIs, visualizations, and data model, please refer to the **[Power BI Dashboard Design Document](docs/PowerBI_Dashboard_Design.md)**.

---

## 8. Project Structure

```
fitness-analytics-platform/
├── data/                     # Final and intermediate data files
├── docs/                     # Project documentation
├── scripts/                  # Python scripts for ETL and data generation
├── sql/                      # SQL scripts for Snowflake setup and transformations
├── Health_Fitness_Analytics.pbix # Power BI dashboard file
└── README.md                 # This file
```

---

## 9. Author

This project was developed by **[Miguel Nemenzo]** as a portfolio piece to demonstrate skills in data engineering and analytics. For any questions or collaboration inquiries, please feel free to connect.

- **LinkedIn**: [www.linkedin.com/in/miguel-nemenzo-4768a0169]
- **GitHub**: [https://github.com/mignemenzo]
- **Portfolio**: [Coming soon!]
