from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        'username',
        'employee_id',
        'email',
        'role',
        'department',
        'manager',
        'is_active',
    )

    list_filter = (
        'role',
        'department',
        'is_active',
    )

    search_fields = (
        'username',
        'employee_id',
        'email',
        'first_name',
        'last_name',
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            'Employee Information',
            {
                'fields': (
                    'employee_id',
                    'phone',
                    'role',
                    'joining_date',
                    'profile_image',
                    'department',
                    'manager',
                )
            }
        ),
    )