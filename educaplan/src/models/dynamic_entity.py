from dataclasses import dataclass, field
from typing import Dict, Any

@dataclass
class DynamicEntity:
    table_name: str
    data: Dict[str, Any] = field(default_factory=dict)

    def __getattr__(self, name):
        return self.data.get(name)

    def __setattr__(self, name, value):
        if name in ('table_name', 'data'):
            super().__setattr__(name, value)
        else:
            self.data[name] = value

    def to_dict(self):
        return self.data

