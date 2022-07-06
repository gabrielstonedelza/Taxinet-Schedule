from django.apps import AppConfig


class ScheduleUsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'schedule_users'

    def ready(self):
        import schedule_users.signals
