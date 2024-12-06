from typing import Dict, Any

class DatabaseConfig:
    HOST: str = 'localhost'
    PORT: int = 3307
    DATABASE: str = 'educaplan'
    USER: str = 'superuser'
    PASSWORD: str = 'superuser'

    @classmethod
    def as_dict(cls) -> Dict[str, Any]:
        return {
            'host': cls.HOST,
            'port': cls.PORT,
            'database': cls.DATABASE,
            'user': cls.USER,
            'password': cls.PASSWORD
        }

