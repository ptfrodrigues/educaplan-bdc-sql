
# EducaPlan - Educational Management System

This repository contains the **EducaPlan** project, an educational management system designed to manage courses, modules, students, teachers, materials, and evaluations. The system supports progress tracking, user management, and database operations.

## **Project Structure**
```
educaplan-bdc-sql/
├── docker-compose.yml
├── docs/
│   ├── MER_Educaplan.png
│   ├── video_interface_grafica.mp4
├── educaplan/
│   ├── requirements.txt
│   ├── src/
│       ├── config/
│       │   ├── app_config.py
│       │   ├── database_config.py
│       ├── controllers/
│       │   ├── dynamic_controller.py
│       ├── database/
│       │   ├── database_interface.py
│       ├── models/
│       │   ├── dynamic_entity.py
│       ├── repositories/
│       │   ├── dynamic_repository.py
│       ├── services/
│       │   ├── auth_service.py
│       │   ├── database_service.py
│       │   ├── dynamic_service.py
│       ├── ui/
│       │   ├── dashboard.py
│       │   ├── footer.py
│       │   ├── navbar.py
│       │   ├── sidebar.py
│       ├── utils/
│           ├── access_control.py
├── mysql-service/
│   ├── init-scripts/
│       ├── 00-create-database.sql
│       ├── 01-create-users.sql
│       ├── 02-create-views.sql
│       ├── 03-store-procedures.sql
│       ├── 04-seed-mock-data.sql
```

---

## **Setup Instructions**

### **Prerequisites**
1. Install **Docker** and **Docker Compose** on your system.
2. Install **Python 3.10+** on your system.
3. Ensure `pip` is installed for Python package management.

---

### **Step 1: Set up MySQL and phpMyAdmin with Docker**
- The project uses Docker to run a MySQL database and phpMyAdmin.

#### **Run the containers:**
1. Open a terminal and navigate to the project directory.
2. Run the following command:
   ```bash
   docker-compose up -d
   ```
3. MySQL will be accessible at `localhost:3307` with:
   - Username: `superuser`
   - Password: `superuser`
4. phpMyAdmin will be accessible at `http://localhost:8080`.

---

### **Step 2: Set up the Python Environment**

#### **Create a Virtual Environment**
- On **Windows**:
  ```cmd
  python -m venv venv
  venv\Scripts\activate
  ```
- On **macOS/Linux**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

#### **Install Required Packages**
- Install the dependencies listed in `requirements.txt`:
  ```bash
  pip install -r educaplan/requirements.txt
  ```

---

### **Step 3: Configure the Database**

If you need to connect to a database other than the default Docker setup, edit the file:
`educaplan/src/config/database_config.py`

#### **Default Configuration for Docker:**
```python
class DatabaseConfig:
    HOST: str = 'localhost'
    PORT: int = 3307
    DATABASE: str = 'educaplan'
    USER: str = 'superuser'
    PASSWORD: str = 'superuser'
```

#### **Example for Local Database:**
Replace the values with your local database settings:
```python
class DatabaseConfig:
    HOST: str = '127.0.0.1'
    PORT: int = 3306
    DATABASE: str = 'your_database_name'
    USER: str = 'your_username'
    PASSWORD: str = 'your_password'
```

---

### **Step 4: Run the Application**
To start the application:
1. Navigate to the `educaplan/src/` directory.
2. Run the `main.py` file:
   ```bash
   python main.py
   ```

---

## **Features**
1. **User Management:** Manage administrators, teachers, and students.
2. **Course Management:** Add, update, and remove courses, modules, and topics.
3. **Student Progress Tracking:** Monitor attendance, grades, and feedback.
4. **Dynamic Queries:** The application uses a flexible query system to interact with the database dynamically.

---

## **Team**
This project was developed by:
- Amauri Donadon
- Henrique Neto
- Pedro Rodrigues

---

## **References**
- **ER Diagram:** [MER_Educaplan.png](./docs/MER_Educaplan.png)
- **Video Demonstration:** [video_interface_grafica.mp4](./docs/video_interface_grafica.mp4)

---

For any issues or inquiries, feel free to open an issue or contact the contributors. Enjoy exploring EducaPlan!