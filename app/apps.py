from django.apps import AppConfig
from .recom_emoji import MyEmoji

class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'
    model = MyEmoji()
