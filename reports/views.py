
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from accounts.models import User
from django.utils import timezone

from .forms import DailyReportForm, AnnouncementForm
from .models import DailyReport, Announcement, Notification


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
    ).order_by(
        '-report_date',
        '-created_at'
    )

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
def admin_work_monitoring(request):

    if not request.user.is_superuser:
        return render(
            request,
            'reports/access_denied.html'
        )

    reports = DailyReport.objects.all().select_related(
        'employee'
    ).order_by(
        '-report_date',
        '-created_at'
    )

    total_reports = reports.count()

    today = timezone.localdate()

    today_reports = reports.filter(
        report_date=today
    ).count()

    employees_with_reports_today = reports.filter(
        report_date=today
    ).values(
        'employee'
    ).distinct().count()

    total_employees = User.objects.filter(
        is_active=True,
        is_superuser=False
    ).count()

    employees_without_report = max(
        total_employees - employees_with_reports_today,
        0
    )

    recent_reports = reports[:10]

    context = {
        'total_reports': total_reports,
        'today_reports': today_reports,
        'employees_with_reports_today': employees_with_reports_today,
        'employees_without_report': employees_without_report,
        'recent_reports': recent_reports,
    }

    return render(
        request,
        'reports/admin_work_monitoring.html',
        context
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

            # Get all employees who should receive announcements
            employees = User.objects.filter(
                role__in=[
                    'MANAGER',
                    'STAFF',
                    'ACCOUNTANT'
                ]
            )

            # Create an unread notification for each employee
            for employee in employees:

                Notification.objects.create(
                    employee=employee,
                    title=announcement.title,
                    message=announcement.message
                )

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

    if request.method == 'POST':

        form = AnnouncementForm(request.POST)

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
        'reports/admin_announcements.html',
        {
            'form': form
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
