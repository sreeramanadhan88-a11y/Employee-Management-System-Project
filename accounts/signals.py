from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone

from .models import LoginActivity


@receiver(user_logged_in)
def create_login_activity(sender, request, user, **kwargs):

    LoginActivity.objects.create(
        employee=user,
        login_time=timezone.now()
    )


@receiver(user_logged_out)
def update_logout_activity(sender, request, user, **kwargs):

    if user is None:
        return

    activity = LoginActivity.objects.filter(
        employee=user,
        logout_time__isnull=True
    ).order_by(
        '-login_time'
    ).first()

    if activity:
        activity.logout_time = timezone.now()
        activity.save()