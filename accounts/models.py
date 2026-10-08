from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        MANAGER = 'MANAGER', 'Manager'
        ACCOUNTANT = 'ACCOUNTANT', 'Accountant'
        STAFF = 'STAFF', 'Staff'

    employee_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True
    )

    phone = models.CharField(
        max_length=15,
        blank=True
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.STAFF
    )

    department = models.ForeignKey(
        'employees.department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees'
    )

    manager = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='team_members'
    )

    joining_date = models.DateField(
        null=True,
        blank=True
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.username


class LoginActivity(models.Model):

    employee = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='login_activities'
    )

    login_time = models.DateTimeField()

    logout_time = models.DateTimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.employee.username} - {self.login_time}"