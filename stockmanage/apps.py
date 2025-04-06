# stockmanage/apps.py
from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in, user_logged_out
from stockmanage.signals import notify_login, notify_logout  # Import the signal handlers

class StockmanageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'stockmanage'

    def ready(self):
        user_logged_in.connect(notify_login)  # Connect login signal
        user_logged_out.connect(notify_logout)  # Connect logout signal