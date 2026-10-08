from django.urls import path
from . import views


urlpatterns = [

    path(
        'apply/',
        views.apply_leave,
        name='apply_leave'
    ),

    path(
        'my-leaves/',
        views.my_leaves,
        name='my_leaves'
    ),
    path(
    'manager-requests/',
    views.manager_leave_requests,
    name='manager_leave_requests'
),
path(
    'approve/<int:leave_id>/',
    views.approve_leave,
    name='approve_leave'
),

path(
    'reject/<int:leave_id>/',
    views.reject_leave,
    name='reject_leave'
),

path(
    'admin-requests/',
    views.admin_leave_requests,
    name='admin_leave_requests'
),

]