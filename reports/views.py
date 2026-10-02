from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import DailyReportForm
from .models import DailyReport


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