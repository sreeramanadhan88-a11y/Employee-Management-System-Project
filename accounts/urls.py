from django.urls import path
from . import views

urlpatterns = [
    path(
        'admin-dashboard/',
        views.admin_dashboard,
        name='admin_dashboard'
    ),

    path(
        'employees/',
        views.employee_list,
        name='employee_list'
    ),

    path(
        'employees/add/',
        views.add_employee,
        name='add_employee'
    ),

    path(
        'employees/<int:employee_id>/edit/',
        views.edit_employee,
        name='edit_employee'
    ),

    path(
        'employees/<int:employee_id>/delete/',
        views.delete_employee,
        name='delete_employee'
    ),
    path(
    'manager-dashboard/',
    views.manager_dashboard,
    name='manager_dashboard'
),
path(
    'login/',
    views.user_login,
    name='login'
),
path(
    'logout/',
    views.user_logout,
    name='logout'
),
path(
    'staff-dashboard/',
    views.staff_dashboard,
    name='staff_dashboard'
),
path(
    'accountant-dashboard/',
    views.accountant_dashboard,
    name='accountant_dashboard'
),
path(
    'profile/',
    views.my_profile,
    name='my_profile'
),
path(
    'admin-login-activity/',
    views.admin_login_activity,
    name='admin_login_activity'
),
]