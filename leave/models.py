from django.db import  models


class LeaveRequest(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        APPROVED = 'APPROVED', 'Approved'
        REJECTED = 'REJECTED', 'Rejected'

    employee = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='leave_requests'
    )

    leave_type = models.CharField(
        max_length=50
    )

    from_date = models.DateField()

    to_date = models.DateField()

    reason = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )

    reviewed_by = models.ForeignKey(
        'accounts.User',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_leave_requests'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.employee.username} - {self.leave_type}"
