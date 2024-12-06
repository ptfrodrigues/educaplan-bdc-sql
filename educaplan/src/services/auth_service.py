from datetime import datetime
from typing import Dict, Any, Optional
from src.services.database_service import DatabaseService

class AuthService:
    def __init__(self, db_service: DatabaseService):
        self.db_service = db_service

    def login(self, email: str, password: str) -> Optional[Dict[str, Any]]:
        query = """
        SELECT u.User_ID, u.Name, u.Email, u.Password, r.Name AS Role_Name
        FROM Users u
        LEFT JOIN Roles r ON u.Role_ID = r.Role_ID
        WHERE u.Email = %s
        """
        result = self.db_service.execute_query(query, (email,))

        if result and len(result) > 0:
            user = result[0]
            if self.verify_password(password, user['Password']):
                # Update last_login
                self.update_last_login(user['User_ID'])
                return {
                    'User_ID': user['User_ID'],
                    'Name': user['Name'],
                    'Email': user['Email'],
                    'Role_Name': user['Role_Name']
                }
        return None

    def verify_password(self, input_password: str, stored_password: str) -> bool:
        return input_password == stored_password 

    def update_last_login(self, user_id: int) -> None:
        query = "UPDATE Users SET last_login = %s WHERE User_ID = %s"
        self.db_service.execute_query(query, (datetime.now(), user_id))

    def logout(self) -> None:
        pass