from abc import ABC, abstractmethod
from typing import List, Dict, Any

class DatabaseInterface(ABC):
    @abstractmethod
    def execute_query(self, query: str, params: tuple = None) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    def get_table_names(self) -> List[str]:
        pass

    @abstractmethod
    def get_table_fields(self, table_name: str) -> List[str]:
        pass

