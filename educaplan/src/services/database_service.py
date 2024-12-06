import mysql.connector
from mysql.connector.pooling import MySQLConnectionPool
from mysql.connector.connection import MySQLConnection
from contextlib import contextmanager
from typing import List, Dict, Any
import logging

class DatabaseService:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        try:
            print("Creating database connection pool")
            self.pool = MySQLConnectionPool(
                pool_name="mypool",
                pool_size=2,
                autocommit=True,
                **self.config
            )
            logging.info("Database connection pool created successfully")
        except mysql.connector.Error as e:
            logging.error(f"Error creating connection pool: {e}")
            raise

    @contextmanager
    def get_connection(self) -> MySQLConnection:
        print("Acquiring connection from pool")
        connection = self.pool.get_connection()
        try:
            yield connection
        finally:
            print("Releasing connection back to pool")
            connection.close()

    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        print(f"Executing query: {query[:50]}...")  # Print first 50 chars of query for brevity
        with self.get_connection() as connection:
            with connection.cursor(dictionary=True, buffered=True) as cursor:
                try:
                    cursor.execute(query, params or ())
                    if query.strip().upper().startswith("SELECT"):
                        result = cursor.fetchall()
                    else:
                        result = [{"affected_rows": cursor.rowcount}]
                    return result
                except mysql.connector.Error as e:
                    logging.error(f"Error executing query: {e}")
                    raise
                finally:
                    # Ensure all results are consumed
                    while cursor.nextset():
                        pass

    def get_table_names(self) -> List[str]:
        print("Getting table names")
        query = "SHOW TABLES"
        try:
            with self.get_connection() as connection:
                with connection.cursor(buffered=True) as cursor:
                    cursor.execute(query)
                    return [table[0] for table in cursor.fetchall()]
        except mysql.connector.Error as e:
            logging.error(f"Error getting table names: {e}")
            return []

    def get_table_fields(self, table_name: str) -> List[str]:
        print(f"Getting table fields for {table_name}")
        query = f"DESCRIBE {table_name}"
        try:
            with self.get_connection() as connection:
                with connection.cursor(dictionary=True, buffered=True) as cursor:
                    cursor.execute(query)
                    return [field['Field'] for field in cursor.fetchall()]
        except mysql.connector.Error as e:
            logging.error(f"Error getting table fields for {table_name}: {e}")
            return []

    def test_connection(self) -> bool:
        print("Testing database connection")
        try:
            with self.get_connection() as connection:
                with connection.cursor(buffered=True) as cursor:
                    cursor.execute("SELECT 1")
                    result = cursor.fetchone()
                    return result is not None and result[0] == 1
        except mysql.connector.Error as e:
            logging.error(f"Database connection test failed: {e}")
            return False

