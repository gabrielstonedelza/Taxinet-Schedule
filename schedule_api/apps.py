from django.apps import AppConfig


class ScheduleApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'schedule_api'

    def ready(self):
        import schedule_api.signals