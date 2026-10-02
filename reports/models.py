from django.db import models


class DailyReport(models.Model):

    employee = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='daily_reports'
    )

    report_date = models.DateField()

    work_title = models.CharField(
        max_length=200
    )

    work_description = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.employee.username} - {self.report_date}"