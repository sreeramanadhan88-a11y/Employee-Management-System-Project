from django.contrib import admin

from .models import Salary


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):

    list_display = (
        'employee',
        'basic_salary',
        'allowances',
        'deductions',
        'net_salary',
        'effective_from',
    )

    list_filter = (
        'effective_from',
    )

    search_fields = (
        'employee__username',
        'employee__employee_id',
        'employee__first_name',
        'employee__last_name',
    )