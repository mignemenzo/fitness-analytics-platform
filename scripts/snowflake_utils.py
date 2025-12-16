"""
Health & Fitness Analytics Platform - Snowflake Utilities
Author: Data Engineering Team
Date: December 2025

Utility functions for Snowflake database operations including connection
management, data loading, and query execution.
"""

import snowflake.connector
from snowflake.connector import DictCursor
from snowflake.connector.pandas_tools import write_pandas
import pandas as pd
import logging
from typing import Optional, Dict, Any, List
from contextlib import contextmanager
import hashlib
from datetime import datetime

from config import SNOWFLAKE_CONFIG, ETL_CONFIG

logger = logging.getLogger(__name__)


class SnowflakeConnection:
    """Manage Snowflake database connections and operations"""
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        Initialize Snowflake connection manager
        
        Args:
            config: Snowflake connection configuration dictionary
        """
        self.config = config or SNOWFLAKE_CONFIG
        self.connection = None
        self.cursor = None
    
    def connect(self) -> snowflake.connector.SnowflakeConnection:
        """
        Establish connection to Snowflake
        
        Returns:
            Snowflake connection object
        """
        try:
            logger.info("Connecting to Snowflake...")
            self.connection = snowflake.connector.connect(
                account=self.config['account'],
                user=self.config['user'],
                password=self.config['password'],
                warehouse=self.config['warehouse'],
                role=self.config['role'],
                database=self.config.get('database'),
                schema=self.config.get('schema')
            )
            logger.info("Successfully connected to Snowflake")
            return self.connection
        except Exception as e:
            logger.error(f"Failed to connect to Snowflake: {str(e)}")
            raise
    
    def close(self):
        """Close Snowflake connection"""
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            logger.info("Snowflake connection closed")
    
    @contextmanager
    def get_cursor(self, dict_cursor: bool = False):
        """
        Context manager for Snowflake cursor
        
        Args:
            dict_cursor: If True, return DictCursor for dictionary results
            
        Yields:
            Snowflake cursor object
        """
        if not self.connection:
            self.connect()
        
        cursor_class = DictCursor if dict_cursor else None
        cursor = self.connection.cursor(cursor_class)
        try:
            yield cursor
        finally:
            cursor.close()
    
    def execute_query(self, query: str, params: tuple = None) -> List[Any]:
        """
        Execute a SQL query and return results
        
        Args:
            query: SQL query string
            params: Query parameters for parameterized queries
            
        Returns:
            List of query results
        """
        try:
            with self.get_cursor() as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                results = cursor.fetchall()
                logger.info(f"Query executed successfully, returned {len(results)} rows")
                return results
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            logger.error(f"Query: {query}")
            raise
    
    def execute_many(self, query: str, data: List[tuple]) -> int:
        """
        Execute a query with multiple parameter sets
        
        Args:
            query: SQL query string with placeholders
            data: List of tuples containing parameter values
            
        Returns:
            Number of rows affected
        """
        try:
            with self.get_cursor() as cursor:
                cursor.executemany(query, data)
                row_count = cursor.rowcount
                self.connection.commit()
                logger.info(f"Batch insert completed: {row_count} rows affected")
                return row_count
        except Exception as e:
            logger.error(f"Batch execution failed: {str(e)}")
            self.connection.rollback()
            raise
    
    def load_dataframe(self, df: pd.DataFrame, table_name: str, 
                      database: str = None, schema: str = None,
                      if_exists: str = 'append') -> bool:
        """
        Load pandas DataFrame into Snowflake table
        
        Args:
            df: pandas DataFrame to load
            table_name: Target table name
            database: Target database (optional)
            schema: Target schema (optional)
            if_exists: Action if table exists ('append', 'replace', 'fail')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            if not self.connection:
                self.connect()
            
            # Set database and schema if provided
            if database:
                self.execute_query(f"USE DATABASE {database}")
            if schema:
                self.execute_query(f"USE SCHEMA {schema}")
            
            logger.info(f"Loading {len(df)} rows into {table_name}...")
            
            # Use Snowflake's optimized write_pandas function
            success, num_chunks, num_rows, output = write_pandas(
                conn=self.connection,
                df=df,
                table_name=table_name,
                auto_create_table=False,  # Tables should be pre-created
                overwrite=(if_exists == 'replace'),
                quote_identifiers=False
            )
            
            if success:
                logger.info(f"Successfully loaded {num_rows} rows into {table_name}")
                return True
            else:
                logger.error(f"Failed to load data into {table_name}")
                return False
                
        except Exception as e:
            logger.error(f"DataFrame load failed: {str(e)}")
            raise
    
    def truncate_table(self, table_name: str, database: str = None, 
                      schema: str = None) -> bool:
        """
        Truncate a Snowflake table
        
        Args:
            table_name: Table to truncate
            database: Database name (optional)
            schema: Schema name (optional)
            
        Returns:
            True if successful
        """
        try:
            full_table_name = table_name
            if database and schema:
                full_table_name = f"{database}.{schema}.{table_name}"
            elif schema:
                full_table_name = f"{schema}.{table_name}"
            
            query = f"TRUNCATE TABLE {full_table_name}"
            self.execute_query(query)
            logger.info(f"Table {full_table_name} truncated successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to truncate table {table_name}: {str(e)}")
            raise
    
    def get_table_row_count(self, table_name: str, database: str = None,
                           schema: str = None) -> int:
        """
        Get row count for a table
        
        Args:
            table_name: Table name
            database: Database name (optional)
            schema: Schema name (optional)
            
        Returns:
            Number of rows in table
        """
        try:
            full_table_name = table_name
            if database and schema:
                full_table_name = f"{database}.{schema}.{table_name}"
            elif schema:
                full_table_name = f"{schema}.{table_name}"
            
            query = f"SELECT COUNT(*) FROM {full_table_name}"
            result = self.execute_query(query)
            count = result[0][0] if result else 0
            return count
        except Exception as e:
            logger.error(f"Failed to get row count for {table_name}: {str(e)}")
            return 0


class ETLJobLogger:
    """Log ETL job execution details to Snowflake metadata tables"""
    
    def __init__(self, snowflake_conn: SnowflakeConnection):
        """
        Initialize ETL job logger
        
        Args:
            snowflake_conn: SnowflakeConnection instance
        """
        self.conn = snowflake_conn
        self.job_id = None
    
    def start_job(self, job_name: str, job_type: str, source_system: str,
                  target_table: str) -> int:
        """
        Log the start of an ETL job
        
        Args:
            job_name: Name of the ETL job
            job_type: Type of job (EXTRACT, TRANSFORM, LOAD)
            source_system: Source system name
            target_table: Target table name
            
        Returns:
            Job ID
        """
        try:
            query = """
            INSERT INTO RAW_FITNESS_DB.METADATA.ETL_JOB_LOG 
            (job_name, job_type, source_system, target_table, start_time, status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
            
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (
                    job_name,
                    job_type,
                    source_system,
                    target_table,
                    datetime.now(),
                    'RUNNING'
                ))
                
                # Get the generated job_id
                cursor.execute("SELECT MAX(job_id) FROM RAW_FITNESS_DB.METADATA.ETL_JOB_LOG")
                self.job_id = cursor.fetchone()[0]
                
                self.conn.connection.commit()
                logger.info(f"ETL job started: {job_name} (Job ID: {self.job_id})")
                return self.job_id
                
        except Exception as e:
            logger.error(f"Failed to log job start: {str(e)}")
            raise
    
    def end_job(self, status: str, records_processed: int = 0,
                records_inserted: int = 0, records_updated: int = 0,
                records_rejected: int = 0, error_message: str = None):
        """
        Log the completion of an ETL job
        
        Args:
            status: Job status (SUCCESS, FAILED, PARTIAL)
            records_processed: Number of records processed
            records_inserted: Number of records inserted
            records_updated: Number of records updated
            records_rejected: Number of records rejected
            error_message: Error message if job failed
        """
        if not self.job_id:
            logger.warning("No job_id found, skipping job end logging")
            return
        
        try:
            query = """
            UPDATE RAW_FITNESS_DB.METADATA.ETL_JOB_LOG
            SET end_time = %s,
                status = %s,
                records_processed = %s,
                records_inserted = %s,
                records_updated = %s,
                records_rejected = %s,
                error_message = %s
            WHERE job_id = %s
            """
            
            with self.conn.get_cursor() as cursor:
                cursor.execute(query, (
                    datetime.now(),
                    status,
                    records_processed,
                    records_inserted,
                    records_updated,
                    records_rejected,
                    error_message,
                    self.job_id
                ))
                self.conn.connection.commit()
                logger.info(f"ETL job completed: Job ID {self.job_id}, Status: {status}")
                
        except Exception as e:
            logger.error(f"Failed to log job end: {str(e)}")


def generate_record_hash(record: pd.Series) -> str:
    """
    Generate MD5 hash for a record to detect duplicates
    
    Args:
        record: pandas Series representing a record
        
    Returns:
        MD5 hash string
    """
    # Convert record to string and generate hash
    record_str = '|'.join(str(v) for v in record.values)
    return hashlib.md5(record_str.encode()).hexdigest()


def add_metadata_columns(df: pd.DataFrame, source_system: str,
                        batch_id: str) -> pd.DataFrame:
    """
    Add metadata columns to DataFrame for tracking
    
    Args:
        df: Input DataFrame
        source_system: Source system name
        batch_id: Batch identifier
        
    Returns:
        DataFrame with metadata columns added
    """
    df_copy = df.copy()
    df_copy['source_system'] = source_system
    df_copy['load_timestamp'] = datetime.now()
    df_copy['batch_id'] = batch_id
    df_copy['record_hash'] = df_copy.apply(generate_record_hash, axis=1)
    return df_copy
