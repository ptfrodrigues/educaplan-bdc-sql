from typing import List, Dict, Any
from src.services.dynamic_service import DynamicService
from src.models.dynamic_entity import DynamicEntity
import logging

class DynamicController:
    def __init__(self, service: DynamicService):
        self.service = service

    def get_all_tables(self) -> List[str]:
        return self.service.get_all_tables()

    def get_table_columns(self, table_name: str) -> List[str]:
        return self.service.get_table_columns(table_name)

    def get_all(self, table_name: str) -> List[DynamicEntity]:
        try:
            return self.service.get_all(table_name)
        except Exception as e:
            logging.error(f"Error getting all records from {table_name}: {e}")
            return []

    def get_by_id(self, table_name: str, id: int) -> DynamicEntity:
        return self.service.get_by_id(table_name, id)

    def create(self, table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.service.create(table_name, data)

    def update(self, table_name: str, id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        return self.service.update(table_name, id, data)

    def delete(self, table_name: str, id: int) -> Dict[str, Any]:
        return self.service.delete(table_name, id)

    def get_related_data(self, table_name: str, id: int) -> Dict[str, List[DynamicEntity]]:
        return self.service.get_related_data(table_name, id)

    def get_foreign_key_names(self, table_name: str, foreign_keys: Dict[str, Any]) -> Dict[str, str]:
        return self.service.get_foreign_key_names(table_name, foreign_keys)

