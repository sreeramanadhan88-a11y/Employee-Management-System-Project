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

]