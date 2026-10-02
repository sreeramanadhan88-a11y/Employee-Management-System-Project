from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .models import User
from .forms import EmployeeCreationForm, LoginForm,ProfileUpdateForm


# =========================
# ADMIN DASHBOARD
# =========================

@login_required
def admin_dashboard(request):

    if not request.user.is_superuser:
        return render(
            request,
            'accounts/access_denied.html'
        )

    return render(
        request,
        'accounts/admin_dashboard.html'
    )


# =========================
# EMPLOYEE LIST
# =========================

@login_required
def employee_list(request):

    if not request.user.is_superuser:
        return render(
            request,
            'accounts/access_denied.html'
        )

    employees = User.objects.exclude(
        is_superuser=True
    )

    return render(
        request,
        'accounts/employee_list.html',
        {
            'employees': employees
        }
    )


# =========================
# ADD EMPLOYEE
# =========================

@login_required
def add_employee(request):

    if not request.user.is_superuser:
        return render(
            request,
            'accounts/access_denied.html'
        )

    if request.method == 'POST':

        form = EmployeeCreationForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():

            employee = form.save(
                commit=False
            )

            employee.set_password(
                form.cleaned_data['password']
            )

            employee.save()

            return redirect(
                'employee_list'
            )

    else:

        form = EmployeeCreationForm()

    return render(
        request,
        'accounts/add_employee.html',
        {
            'form': form
        }
    )


# =========================
# EDIT EMPLOYEE
# =========================

@login_required
def edit_employee(request, employee_id):

    if not request.user.is_superuser:
        return render(
            request,
            'accounts/access_denied.html'
        )

    employee = User.objects.get(
        id=employee_id
    )

    if request.method == 'POST':

        form = EmployeeCreationForm(
            request.POST,
            request.FILES,
            instance=employee
        )

        if form.is_valid():

            employee = form.save(
                commit=False
            )

            # Change password only if
            # a new password was entered

            password = form.cleaned_data.get(
                'password'
            )

            if password:

                employee.set_password(
                    password
                )

            employee.save()

            return redirect(
                'employee_list'
            )

    else:

        form = EmployeeCreationForm(
            instance=employee
        )

        # Password is optional while editing

        form.fields['password'].required = False

    return render(
        request,
        'accounts/edit_employee.html',
        {
            'form': form,
            'employee': employee
        }
    )


# =========================
# DELETE EMPLOYEE
# =========================

@login_required
def delete_employee(request, employee_id):

    if not request.user.is_superuser:
        return render(
            request,
            'accounts/access_denied.html'
        )

    employee = User.objects.get(
        id=employee_id
    )

    if request.method == 'POST':

        employee.delete()

        return redirect(
            'employee_list'
        )

    return render(
        request,
        'accounts/delete_employee.html',
        {
            'employee': employee
        }
    )


# =========================
# MANAGER DASHBOARD
# =========================

@login_required
def manager_dashboard(request):

    if request.user.role != User.Role.MANAGER:
        return render(
            request,
            'accounts/access_denied.html'
        )

    team_members = request.user.team_members.all()

    return render(
        request,
        'accounts/manager_dashboard.html',
        {
            'team_members': team_members
        }
    )


# =========================
# STAFF DASHBOARD
# =========================

@login_required
def staff_dashboard(request):

    if request.user.role != User.Role.STAFF:
        return render(
            request,
            'accounts/access_denied.html'
        )

    return render(
        request,
        'accounts/staff_dashboard.html'
    )


# =========================
# ACCOUNTANT DASHBOARD
# =========================

@login_required
def accountant_dashboard(request):

    if request.user.role != User.Role.ACCOUNTANT:
        return render(
            request,
            'accounts/access_denied.html'
        )

    return render(
        request,
        'accounts/accountant_dashboard.html'
    )


# =========================
# EMS LOGIN
# =========================

def user_login(request):

    # If the user is already logged in,
    # send them to their dashboard.

    if request.user.is_authenticated:

        # Admin

        if request.user.is_superuser:
            return redirect(
                'admin_dashboard'
            )

        # Manager

        if request.user.role == User.Role.MANAGER:
            return redirect(
                'manager_dashboard'
            )

        # Staff

        if request.user.role == User.Role.STAFF:
            return redirect(
                'staff_dashboard'
            )

        # Accountant

        if request.user.role == User.Role.ACCOUNTANT:
            return redirect(
                'accountant_dashboard'
            )

    # Handle login form submission

    if request.method == 'POST':

        form = LoginForm(
            request.POST
        )

        if form.is_valid():

            username = form.cleaned_data[
                'username'
            ]

            password = form.cleaned_data[
                'password'
            ]

            # Check username and password

            user = authenticate(
                request,
                username=username,
                password=password
            )

            if user is not None:

                # Create login session

                login(
                    request,
                    user
                )

                # Admin

                if user.is_superuser:
                    return redirect(
                        'admin_dashboard'
                    )

                # Manager

                if user.role == User.Role.MANAGER:
                    return redirect(
                        'manager_dashboard'
                    )

                # Staff

                if user.role == User.Role.STAFF:
                    return redirect(
                        'staff_dashboard'
                    )

                # Accountant

                if user.role == User.Role.ACCOUNTANT:
                    return redirect(
                        'accountant_dashboard'
                    )

            else:

                form.add_error(
                    None,
                    'Invalid username or password.'
                )

    else:

        form = LoginForm()

    return render(
        request,
        'accounts/login.html',
        {
            'form': form
        }
    )


# =========================
# LOGOUT
# =========================

@login_required
def user_logout(request):

    # End the current login session

    logout(request)

    # Show logout page

    return render(
        request,
        'accounts/logout.html'
    )

# =========================
# MY PROFILE
# =========================

@login_required
def my_profile(request):

    if request.method == 'POST':

        form = ProfileUpdateForm(
            request.POST,
            request.FILES,
            instance=request.user
        )

        if form.is_valid():

            form.save()

            return redirect(
                'my_profile'
            )

    else:

        form = ProfileUpdateForm(
            instance=request.user
        )

    return render(
        request,
        'accounts/my_profile.html',
        {
            'form': form
        }
    )