from django.urls import path

from . import views


urlpatterns = [

    path(
        'daily-report/',
        views.submit_daily_report,
        name='submit_daily_report'
    ),

    path(
        'my-daily-reports/',
        views.my_daily_reports,
        name='my_daily_reports'
    ),
    path(
    'team-daily-reports/',
    views.team_daily_reports,
    name='team_daily_reports'
),
path(
    'announcements/create/',
    views.create_announcement,
    name='create_announcement'
),
path(
    'announcements/',
    views.admin_announcements,
    name='admin_announcements'
),
path(
    'announcements/view/',
    views.employee_announcements,
    name='employee_announcements'
),
path(
    'notifications/',
    views.notifications,
    name='notifications'
),
path(
    'notifications/<int:notification_id>/read/',
    views.mark_notification_read,
    name='mark_notification_read'
),

]