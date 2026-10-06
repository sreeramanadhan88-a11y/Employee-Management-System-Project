from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.models import User

from .forms import DailyReportForm, AnnouncementForm
from .models import DailyReport,Announcement,Notification


@login_required
def submit_daily_report(request):

    if request.user.role != 'STAFF':
        return render(
            request,
            'reports/access_denied.html'
        )

    if request.method == 'POST':

        form = DailyReportForm(
            request.POST
        )

        if form.is_valid():

            report = form.save(
                commit=False
            )

            report.employee = request.user

            report.save()

            return redirect(
                'my_daily_reports'
            )

    else:

        form = DailyReportForm()

    return render(
        request,
        'reports/submit_daily_report.html',
        {
            'form': form
        }
    )


@login_required
def my_daily_reports(request):

    if request.user.role != 'STAFF':
        return render(
            request,
            'reports/access_denied.html'
        )

    reports = DailyReport.objects.filter(
        employee=request.user
    ).order_by('-report_date', '-created_at')

    return render(
        request,
        'reports/my_daily_reports.html',
        {
            'reports': reports
        }
    )
@login_required
def team_daily_reports(request):

    if request.user.role != 'MANAGER':
        return render(
            request,
            'reports/access_denied.html'
        )

    reports = DailyReport.objects.filter(
        employee__manager=request.user
    ).order_by(
        '-report_date',
        '-created_at'
    )

    return render(
        request,
        'reports/team_daily_reports.html',
        {
            'reports': reports
        }
    )
@login_required
def create_announcement(request):

    if not request.user.is_superuser:
        return render(
            request,
            'reports/access_denied.html'
        )

    if request.method == 'POST':

        form = AnnouncementForm(
            request.POST
        )

        if form.is_valid():

            announcement = form.save(
                commit=False
            )

            announcement.created_by = request.user
            announcement.save()

            

            return redirect(
                'admin_announcements'
            )

    else:

        form = AnnouncementForm()

    return render(
        request,
        'reports/create_announcement.html',
        {
            'form': form
        }
    )
@login_required
def admin_announcements(request):

    if not request.user.is_superuser:
        return render(
            request,
            'reports/access_denied.html'
        )

    announcements = Announcement.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'reports/admin_announcements.html',
        {
            'announcements': announcements
        }
    )
@login_required
def employee_announcements(request):

    if request.user.role not in [
        'MANAGER',
        'STAFF',
        'ACCOUNTANT'
    ]:
        return render(
            request,
            'reports/access_denied.html'
        )

    announcements = Announcement.objects.all().order_by(
        '-created_at'
    )

    return render(
        request,
        'reports/employee_announcements.html',
        {
            'announcements': announcements
        }
    )
@login_required
def notifications(request):

    if request.user.role not in [
        'MANAGER',
        'STAFF',
        'ACCOUNTANT'
    ]:
        return render(
            request,
            'reports/access_denied.html'
        )

    user_notifications = Notification.objects.filter(
        employee=request.user
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'reports/notifications.html',
        {
            'notifications': user_notifications
        }
    )
@login_required
def mark_notification_read(request, notification_id):

    if request.user.role not in [
        'MANAGER',
        'STAFF',
        'ACCOUNTANT'
    ]:
        return render(
            request,
            'reports/access_denied.html'
        )

    notification = Notification.objects.get(
        id=notification_id,
        employee=request.user
    )

    notification.is_read = True
    notification.save()

    return redirect(
        'notifications'
    )