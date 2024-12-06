from typing import List, Dict, Any
from src.services.database_service import DatabaseService
from src.models.dynamic_entity import DynamicEntity
import logging

class DynamicRepository:
    def __init__(self, db: DatabaseService):
        self.db = db
        self.tables: Dict[str, List[str]] = {}
        self.setup_dynamic_layer()

    def setup_dynamic_layer(self) -> None:
        try:
            print("Setting up dynamic layer")
            with self.db.get_connection() as connection:
                # Get all table names
                with connection.cursor(buffered=True) as cursor:
                    cursor.execute("SHOW TABLES")
                    table_names = [table[0] for table in cursor.fetchall()]

                # Get fields for all tables
                for table_name in table_names:
                    with connection.cursor(dictionary=True, buffered=True) as cursor:
                        cursor.execute(f"DESCRIBE {table_name}")
                        self.tables[table_name] = [field['Field'] for field in cursor.fetchall()]

            print(f"Dynamic layer setup complete. Tables loaded: {', '.join(self.tables.keys())}")
        except Exception as e:
            logging.error(f"Error setting up dynamic layer: {e}")
            self.tables = {}

    def get_all_tables(self) -> List[str]:
        return list(self.tables.keys())

    def get_table_columns(self, table_name: str) -> List[str]:
        return self.tables.get(table_name, [])

    def get_all(self, table_name: str) -> List[DynamicEntity]:
        query = f"SELECT * FROM {table_name}"
        results = self.db.execute_query(query)
        return [DynamicEntity(table_name, row) for row in results]

    def get_by_id(self, table_name: str, id: int) -> DynamicEntity:
        id_column = f"{table_name[:-1]}_ID" if table_name.endswith('s') else 'ID'
        query = f"SELECT * FROM {table_name} WHERE {id_column} = %s"
        result = self.db.execute_query(query, (id,))
        return DynamicEntity(table_name, result[0]) if result else None

    def create(self, entity: DynamicEntity) -> Dict[str, Any]:
        columns = ', '.join(entity.data.keys())
        placeholders = ', '.join(['%s'] * len(entity.data))
        query = f"INSERT INTO {entity.table_name} ({columns}) VALUES ({placeholders})"
        values = tuple(entity.data.values())
        return self.db.execute_query(query, values)[0]

    def update(self, entity: DynamicEntity) -> Dict[str, Any]:
        id_column = f"{entity.table_name[:-1]}_ID" if entity.table_name.endswith('s') else 'ID'
        set_clause = ', '.join([f"{key} = %s" for key in entity.data.keys() if key != id_column])
        query = f"UPDATE {entity.table_name} SET {set_clause} WHERE {id_column} = %s"
        values = tuple(v for k, v in entity.data.items() if k != id_column) + (entity.data[id_column],)
        return self.db.execute_query(query, values)[0]

    def delete(self, table_name: str, id: int) -> Dict[str, Any]:
        id_column = f"{table_name[:-1]}_ID" if table_name.endswith('s') else 'ID'
        query = f"DELETE FROM {table_name} WHERE {id_column} = %s"
        return self.db.execute_query(query, (id,))[0]

    def get_related_data(self, table_name: str, id: int) -> Dict[str, List[DynamicEntity]]:
        related_data = {}
        id_column = f"{table_name[:-1]}_ID" if table_name.endswith('s') else 'ID'
        
        for related_table, columns in self.tables.items():
            if f"{table_name[:-1]}_ID" in columns:
                query = f"SELECT * FROM {related_table} WHERE {table_name[:-1]}_ID = %s"
                results = self.db.execute_query(query, (id,))
                related_data[related_table] = [DynamicEntity(related_table, row) for row in results]

        return related_data

