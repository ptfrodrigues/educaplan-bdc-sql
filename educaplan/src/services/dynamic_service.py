from typing import List, Dict, Any
from src.repositories.dynamic_repository import DynamicRepository
from src.models.dynamic_entity import DynamicEntity
import logging

class DynamicService:
    def __init__(self, repository: DynamicRepository):
        self.repository = repository

    def get_all_tables(self) -> List[str]:
        return self.repository.get_all_tables()

    def get_table_columns(self, table_name: str) -> List[str]:
        return self.repository.get_table_columns(table_name)

    def get_all(self, table_name: str) -> List[DynamicEntity]:
        return self.repository.get_all(table_name)

    def get_by_id(self, table_name: str, id: int) -> DynamicEntity:
        return self.repository.get_by_id(table_name, id)

    def create(self, table_name: str, data: Dict[str, Any]) -> Dict[str, Any]:
        entity = DynamicEntity(table_name, data)
        return self.repository.create(entity)

    def update(self, table_name: str, id: int, data: Dict[str, Any]) -> Dict[str, Any]:
        entity = DynamicEntity(table_name, {**data, f"{table_name[:-1]}_ID": id})
        return self.repository.update(entity)

    def delete(self, table_name: str, id: int) -> Dict[str, Any]:
        return self.repository.delete(table_name, id)


