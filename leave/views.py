from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import LeaveRequestForm
from .models import LeaveRequest
from reports.models import Notification


@login_required
def apply_leave(request):

    if request.user.role != 'STAFF':
        return render(
            request,
            'leave/access_denied.html'
        )

    if request.method == 'POST':

        form = LeaveRequestForm(
            request.POST
        )

        if form.is_valid():

            leave_request = form.save(
                commit=False
            )

            leave_request.employee = request.user

            leave_request.save()

            return redirect(
                'my_leaves'
            )

    else:

        form = LeaveRequestForm()

    return render(
        request,
        'leave/apply_leave.html',
        {
            'form': form
        }
    )


@login_required
def my_leaves(request):

    if request.user.role != 'STAFF':
        return render(
            request,
            'leave/access_denied.html'
        )

    leaves = LeaveRequest.objects.filter(
        employee=request.user
    ).order_by('-created_at')

    return render(
        request,
        'leave/my_leaves.html',
        {
            'leaves': leaves
        }
    )
@login_required
def manager_leave_requests(request):

    if request.user.role != 'MANAGER':
        return render(
            request,
            'leave/access_denied.html'
        )

    leave_requests = LeaveRequest.objects.filter(
        employee__manager=request.user
    ).order_by('-created_at')

    return render(
        request,
        'leave/manager_leave_requests.html',
        {
            'leave_requests': leave_requests
        }
    )
@login_required
def approve_leave(request, leave_id):

    if request.user.role != 'MANAGER':
        return render(
            request,
            'leave/access_denied.html'
        )

    leave_request = LeaveRequest.objects.get(
        id=leave_id
    )

    if leave_request.employee.manager != request.user:
        return render(
            request,
            'leave/access_denied.html'
        )

    leave_request.status = LeaveRequest.Status.APPROVED
    leave_request.reviewed_by = request.user
    leave_request.save()

    Notification.objects.create(
        employee=leave_request.employee,
        title='Leave Approved',
        message=f'Your {leave_request.leave_type} leave has been approved.'
    )

    return redirect(
        'manager_leave_requests'
    )

@login_required
def reject_leave(request, leave_id):

    if request.user.role != 'MANAGER':
        return render(
            request,
            'leave/access_denied.html'
        )

    leave_request = LeaveRequest.objects.get(
        id=leave_id
    )

    if leave_request.employee.manager != request.user:
        return render(
            request,
            'leave/access_denied.html'
        )

    leave_request.status = LeaveRequest.Status.REJECTED
    leave_request.reviewed_by = request.user
    leave_request.save()

    Notification.objects.create(
        employee=leave_request.employee,
        title='Leave Rejected',
        message=f'Your {leave_request.leave_type} leave has been rejected.'
    )

    return redirect(
        'manager_leave_requests'
    )