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


class Announcement(models.Model):

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    created_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='announcements'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title
class Notification(models.Model):

    employee = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='notifications'
    )

    title = models.CharField(
        max_length=200
    )

    message = models.TextField()

    is_read = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.employee.username} - {self.title}"