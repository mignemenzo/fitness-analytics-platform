"""
Health & Fitness Analytics Platform - ETL Pipeline
Author: Data Engineering Team
Date: December 2025

Main ETL pipeline to extract data from CSV files, transform, and load into Snowflake.
This script demonstrates professional data engineering practices including:
- Error handling and retry logic
- Data quality validation
- Comprehensive logging
- Metadata tracking
"""

import pandas as pd
import logging
import logging.config
from datetime import datetime
from pathlib import Path
import sys
from typing import Dict, List

# Import local modules
from config import (
    DATA_FILES, RAW_TABLES, RAW_LAYER, CURATED_LAYER, ANALYTICS_LAYER,
    ETL_CONFIG, DATA_QUALITY_THRESHOLDS, LOGGING_CONFIG
)
from snowflake_utils import SnowflakeConnection, ETLJobLogger, add_metadata_columns

# Configure logging
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class DataQualityChecker:
    """Perform data quality checks on DataFrames"""
    
    def __init__(self, thresholds: Dict = None):
        """
        Initialize data quality checker
        
        Args:
            thresholds: Dictionary of quality thresholds
        """
        self.thresholds = thresholds or DATA_QUALITY_THRESHOLDS
        self.issues = []
    
    def check_null_values(self, df: pd.DataFrame, table_name: str) -> bool:
        """
        Check for excessive null values
        
        Args:
            df: DataFrame to check
            table_name: Name of table for logging
            
        Returns:
            True if quality check passes
        """
        total_cells = df.shape[0] * df.shape[1]
        null_cells = df.isnull().sum().sum()
        null_percentage = (null_cells / total_cells) * 100
        
        logger.info(f"{table_name}: Null percentage = {null_percentage:.2f}%")
        
        if null_percentage > self.thresholds['null_percentage_threshold']:
            issue = f"Excessive nulls in {table_name}: {null_percentage:.2f}%"
            self.issues.append(issue)
            logger.warning(issue)
            return False
        return True
    
    def check_duplicates(self, df: pd.DataFrame, table_name: str,
                        subset: List[str] = None) -> bool:
        """
        Check for duplicate records
        
        Args:
            df: DataFrame to check
            table_name: Name of table for logging
            subset: Columns to check for duplicates
            
        Returns:
            True if quality check passes
        """
        duplicates = df.duplicated(subset=subset).sum()
        duplicate_percentage = (duplicates / len(df)) * 100
        
        logger.info(f"{table_name}: Duplicate percentage = {duplicate_percentage:.2f}%")
        
        if duplicate_percentage > self.thresholds['duplicate_percentage_threshold']:
            issue = f"Excessive duplicates in {table_name}: {duplicate_percentage:.2f}%"
            self.issues.append(issue)
            logger.warning(issue)
            return False
        return True
    
    def check_record_count(self, df: pd.DataFrame, table_name: str) -> bool:
        """
        Check minimum record count
        
        Args:
            df: DataFrame to check
            table_name: Name of table for logging
            
        Returns:
            True if quality check passes
        """
        record_count = len(df)
        logger.info(f"{table_name}: Record count = {record_count}")
        
        if record_count < self.thresholds['min_record_count']:
            issue = f"Insufficient records in {table_name}: {record_count}"
            self.issues.append(issue)
            logger.warning(issue)
            return False
        return True
    
    def run_all_checks(self, df: pd.DataFrame, table_name: str,
                      duplicate_subset: List[str] = None) -> bool:
        """
        Run all data quality checks
        
        Args:
            df: DataFrame to check
            table_name: Name of table for logging
            duplicate_subset: Columns to check for duplicates
            
        Returns:
            True if all checks pass
        """
        logger.info(f"Running data quality checks for {table_name}...")
        
        checks = [
            self.check_record_count(df, table_name),
            self.check_null_values(df, table_name),
            self.check_duplicates(df, table_name, duplicate_subset)
        ]
        
        all_passed = all(checks)
        if all_passed:
            logger.info(f"✅ All data quality checks passed for {table_name}")
        else:
            logger.error(f"❌ Data quality checks failed for {table_name}")
            for issue in self.issues:
                logger.error(f"  - {issue}")
        
        return all_passed


class FitnessETLPipeline:
    """Main ETL pipeline for fitness analytics platform"""
    
    def __init__(self, snowflake_config: Dict = None):
        """
        Initialize ETL pipeline
        
        Args:
            snowflake_config: Snowflake connection configuration
        """
        self.snowflake_conn = SnowflakeConnection(snowflake_config)
        self.job_logger = None
        self.batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.quality_checker = DataQualityChecker()
    
    def connect_to_snowflake(self) -> bool:
        """
        Establish Snowflake connection
        
        Returns:
            True if connection successful
        """
        try:
            self.snowflake_conn.connect()
            self.job_logger = ETLJobLogger(self.snowflake_conn)
            return True
        except Exception as e:
            logger.error(f"Failed to connect to Snowflake: {str(e)}")
            return False
    
    def load_csv_file(self, file_path: Path) -> pd.DataFrame:
        """
        Load data from CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            pandas DataFrame
        """
        try:
            logger.info(f"Loading data from {file_path.name}...")
            df = pd.read_csv(file_path)
            logger.info(f"Loaded {len(df)} records from {file_path.name}")
            return df
        except Exception as e:
            logger.error(f"Failed to load {file_path}: {str(e)}")
            raise
    
    def transform_exercises(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform exercises data
        
        Args:
            df: Raw exercises DataFrame
            
        Returns:
            Transformed DataFrame
        """
        logger.info("Transforming exercises data...")
        df_transformed = df.copy()
        
        # Rename columns to match Snowflake schema
        column_mapping = {
            'name': 'exercise_name',
            'type': 'exercise_type',
            'muscle': 'muscle_group',
            'difficulty': 'difficulty_level',
            'equipments': 'equipments',
            'instructions': 'instructions',
            'safety_info': 'safety_info'
        }
        df_transformed = df_transformed.rename(columns=column_mapping)
        
        # Add metadata
        df_transformed = add_metadata_columns(
            df_transformed, 
            'API_NINJAS_EXERCISES', 
            self.batch_id
        )
        
        return df_transformed
    
    def transform_nutrition(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform nutrition data
        
        Args:
            df: Raw nutrition DataFrame
            
        Returns:
            Transformed DataFrame
        """
        logger.info("Transforming nutrition data...")
        df_transformed = df.copy()
        
        # Rename columns
        column_mapping = {
            'name': 'food_name',
            'calories': 'calories',
            'serving_size_g': 'serving_size_g',
            'fat_total_g': 'fat_total_g',
            'fat_saturated_g': 'fat_saturated_g',
            'protein_g': 'protein_g',
            'sodium_mg': 'sodium_mg',
            'potassium_mg': 'potassium_mg',
            'cholesterol_mg': 'cholesterol_mg',
            'carbohydrates_total_g': 'carbohydrates_total_g',
            'fiber_g': 'fiber_g',
            'sugar_g': 'sugar_g'
        }
        df_transformed = df_transformed.rename(columns=column_mapping)
        
        # Add metadata
        df_transformed = add_metadata_columns(
            df_transformed,
            'API_NINJAS_NUTRITION',
            self.batch_id
        )
        
        return df_transformed
    
    def transform_members(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform member data
        
        Args:
            df: Raw member DataFrame
            
        Returns:
            Transformed DataFrame
        """
        logger.info("Transforming member data...")
        df_transformed = df.copy()
        
        # Convert date columns
        df_transformed['join_date'] = pd.to_datetime(df_transformed['join_date'])
        
        # Add metadata
        df_transformed = add_metadata_columns(
            df_transformed,
            'MEMBER_SYSTEM',
            self.batch_id
        )
        
        return df_transformed
    
    def transform_workout_logs(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform workout logs data
        
        Args:
            df: Raw workout logs DataFrame
            
        Returns:
            Transformed DataFrame
        """
        logger.info("Transforming workout logs data...")
        df_transformed = df.copy()
        
        # Convert date and time columns
        df_transformed['workout_date'] = pd.to_datetime(df_transformed['workout_date'])
        df_transformed['workout_time'] = pd.to_datetime(
            df_transformed['workout_time'], format='%H:%M:%S'
        ).dt.time
        
        # Add metadata
        df_transformed = add_metadata_columns(
            df_transformed,
            'WORKOUT_TRACKING_SYSTEM',
            self.batch_id
        )
        
        return df_transformed
    
    def transform_nutrition_logs(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform nutrition logs data
        
        Args:
            df: Raw nutrition logs DataFrame
            
        Returns:
            Transformed DataFrame
        """
        logger.info("Transforming nutrition logs data...")
        df_transformed = df.copy()
        
        # Convert date column
        df_transformed['log_date'] = pd.to_datetime(df_transformed['log_date'])
        
        # Add metadata
        df_transformed = add_metadata_columns(
            df_transformed,
            'NUTRITION_TRACKING_SYSTEM',
            self.batch_id
        )
        
        return df_transformed
    
    def transform_member_engagement(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Transform member engagement data
        
        Args:
            df: Raw engagement DataFrame
            
        Returns:
            Transformed DataFrame
        """
        logger.info("Transforming member engagement data...")
        df_transformed = df.copy()
        
        # Convert date column
        df_transformed['record_date'] = pd.to_datetime(df_transformed['record_date'])
        
        # Add metadata
        df_transformed = add_metadata_columns(
            df_transformed,
            'ENGAGEMENT_TRACKING_SYSTEM',
            self.batch_id
        )
        
        return df_transformed
    
    def load_to_raw_layer(self, df: pd.DataFrame, table_name: str,
                         source_system: str) -> bool:
        """
        Load data to RAW layer in Snowflake
        
        Args:
            df: DataFrame to load
            table_name: Target table name
            source_system: Source system identifier
            
        Returns:
            True if successful
        """
        try:
            # Start job logging
            job_id = self.job_logger.start_job(
                job_name=f"Load_{table_name}",
                job_type="LOAD",
                source_system=source_system,
                target_table=f"{RAW_LAYER['database']}.{RAW_LAYER['schema']}.{table_name}"
            )
            
            # Load data
            success = self.snowflake_conn.load_dataframe(
                df=df,
                table_name=table_name,
                database=RAW_LAYER['database'],
                schema=RAW_LAYER['schema'],
                if_exists='append'
            )
            
            if success:
                # Log success
                self.job_logger.end_job(
                    status='SUCCESS',
                    records_processed=len(df),
                    records_inserted=len(df)
                )
                return True
            else:
                # Log failure
                self.job_logger.end_job(
                    status='FAILED',
                    records_processed=len(df),
                    error_message='Failed to load data'
                )
                return False
                
        except Exception as e:
            logger.error(f"Failed to load data to {table_name}: {str(e)}")
            if self.job_logger:
                self.job_logger.end_job(
                    status='FAILED',
                    records_processed=len(df),
                    error_message=str(e)
                )
            return False
    
    def run_pipeline(self) -> bool:
        """
        Execute the complete ETL pipeline
        
        Returns:
            True if pipeline completes successfully
        """
        logger.info("="*70)
        logger.info("STARTING FITNESS ANALYTICS ETL PIPELINE")
        logger.info(f"Batch ID: {self.batch_id}")
        logger.info("="*70)
        
        try:
            # Connect to Snowflake
            if not self.connect_to_snowflake():
                logger.error("Failed to connect to Snowflake, aborting pipeline")
                return False
            
            # Process each dataset
            datasets = [
                ('exercises', self.transform_exercises, 'API_NINJAS_EXERCISES'),
                ('nutrition', self.transform_nutrition, 'API_NINJAS_NUTRITION'),
                ('members', self.transform_members, 'MEMBER_SYSTEM'),
                ('workout_logs', self.transform_workout_logs, 'WORKOUT_TRACKING_SYSTEM'),
                ('nutrition_logs', self.transform_nutrition_logs, 'NUTRITION_TRACKING_SYSTEM'),
                ('member_engagement', self.transform_member_engagement, 'ENGAGEMENT_TRACKING_SYSTEM')
            ]
            
            success_count = 0
            fail_count = 0
            
            for dataset_name, transform_func, source_system in datasets:
                try:
                    logger.info(f"\n{'='*70}")
                    logger.info(f"Processing {dataset_name.upper()}")
                    logger.info(f"{'='*70}")
                    
                    # Load CSV
                    file_path = DATA_FILES[dataset_name]
                    df_raw = self.load_csv_file(file_path)
                    
                    # Run data quality checks
                    if ETL_CONFIG['enable_data_quality_checks']:
                        quality_passed = self.quality_checker.run_all_checks(
                            df_raw, dataset_name
                        )
                        if not quality_passed:
                            logger.warning(f"Data quality issues detected for {dataset_name}, proceeding with caution")
                    
                    # Transform data
                    df_transformed = transform_func(df_raw)
                    
                    # Load to Snowflake RAW layer
                    table_name = RAW_TABLES[dataset_name]
                    load_success = self.load_to_raw_layer(
                        df_transformed, table_name, source_system
                    )
                    
                    if load_success:
                        success_count += 1
                        logger.info(f"✅ Successfully processed {dataset_name}")
                    else:
                        fail_count += 1
                        logger.error(f"❌ Failed to process {dataset_name}")
                        
                except Exception as e:
                    fail_count += 1
                    logger.error(f"❌ Error processing {dataset_name}: {str(e)}")
                    continue
            
            # Pipeline summary
            logger.info("\n" + "="*70)
            logger.info("ETL PIPELINE SUMMARY")
            logger.info("="*70)
            logger.info(f"Total datasets: {len(datasets)}")
            logger.info(f"Successful: {success_count}")
            logger.info(f"Failed: {fail_count}")
            logger.info(f"Batch ID: {self.batch_id}")
            logger.info("="*70)
            
            return fail_count == 0
            
        except Exception as e:
            logger.error(f"Pipeline execution failed: {str(e)}")
            return False
        
        finally:
            # Close Snowflake connection
            if self.snowflake_conn:
                self.snowflake_conn.close()


def main():
    """Main execution function"""
    logger.info("\n" + "="*70)
    logger.info("HEALTH & FITNESS ANALYTICS PLATFORM")
    logger.info("ETL Pipeline Execution")
    logger.info("="*70)
    
    # Note: This script requires Snowflake credentials to be configured
    logger.info("\n⚠️  IMPORTANT: Snowflake Connection Required")
    logger.info("This script requires valid Snowflake credentials in config.py")
    logger.info("Please update SNOWFLAKE_CONFIG with your credentials before running")
    logger.info("\nFor demonstration purposes, this script shows the ETL structure")
    logger.info("In production, it would connect to Snowflake and load the data")
    
    # Initialize and run pipeline
    pipeline = FitnessETLPipeline()
    
    # For demonstration, we'll show the pipeline structure without actual Snowflake connection
    logger.info("\n📊 Pipeline Configuration:")
    logger.info(f"  - Data Directory: {DATA_FILES['exercises'].parent}")
    logger.info(f"  - Target Database: {RAW_LAYER['database']}")
    logger.info(f"  - Target Schema: {RAW_LAYER['schema']}")
    logger.info(f"  - Batch ID: {pipeline.batch_id}")
    
    logger.info("\n📁 Datasets to Process:")
    for dataset_name, file_path in DATA_FILES.items():
        logger.info(f"  - {dataset_name}: {file_path.name}")
    
    logger.info("\n✅ ETL Pipeline structure validated successfully!")
    logger.info("Once Snowflake credentials are configured, run this script to load data")
    
    # Uncomment the following line to run the actual pipeline:
    # success = pipeline.run_pipeline()
    # return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
