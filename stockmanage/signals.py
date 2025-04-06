# stockmanage/signals.py
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .utils import send_sns_notification

@receiver(user_logged_in)
def notify_login(sender, user, request, **kwargs):
    send_sns_notification(
        subject="User Login",
        message=f"User {user.username} logged in at {request.META.get('HTTP_HOST')}."
    )

@receiver(user_logged_out)
def notify_logout(sender, user, request, **kwargs):
    send_sns_notification(
        subject="User Logout",
        message=f"User {user.username} logged out from {request.META.get('HTTP_HOST')}."
    )