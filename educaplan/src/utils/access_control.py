class AccessControl:
    @staticmethod
    def get_allowed_categories(role):
        categories = {
            'Administrator': ['User Management', 'Course Management', 'Student Management', 'Reporting'],
            'Teacher': ['Course Management', 'Student Management', 'Reporting'],
            'Student': ['My Courses', 'My Progress']
        }
        return categories.get(role, [])

    @staticmethod
    def get_tables_in_category(category):
        category_tables = {
            'User Management': ['Users_View', 'Roles_View', 'Recent_User_Activity'],
            'Course Management': ['Courses_View', 'Modules_View', 'Topics_View', 'Materials_View'],
            'Student Management': ['Students_View', 'Attendance_View'],
            'Reporting': ['Feedback_View', 'Progress_View', 'Grades_View'],
            'My Courses': ['My_Courses_View', 'Materials_View'],
            'My Progress': ['Attendance_View', 'Grades_View', 'Feedback_View']
        }
        return category_tables.get(category, [])

    @staticmethod
    def filter_allowed_data(data, allowed_fields):
        return {k: v for k, v in data.items() if k in allowed_fields}