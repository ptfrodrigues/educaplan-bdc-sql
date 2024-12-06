class AppConfig:
    APP_NAME = "EducaPlan"

    @staticmethod
    def get_navbar_config(username, logout_command, exit_command):
        return {
            'app_name': AppConfig.APP_NAME,
            'username': username,
            'menu_items': [
                {'label': "Logout", 'command': logout_command},
                {'label': "Exit", 'command': exit_command}
            ]
        }

    @staticmethod
    def get_footer_config():
        return {
            'font': ("Helvetica", 10),
            'styles': {
                'error': "Error.TLabel",
                'success': "Success.TLabel",
                'info': "TLabel"
            },
            'message_duration': 5000
        }

