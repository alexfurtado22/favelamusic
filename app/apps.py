from django.apps import AppConfig


class MyAppConfig(AppConfig):  # better to rename from generic "AppConfig"
    default_auto_field = "django.db.models.BigAutoField"
    name = "app"

    def ready(self):
        import app.signals  # noqa: F401 to avoid unused import warning
