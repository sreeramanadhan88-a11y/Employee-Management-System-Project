from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import (
    SalaryForm,
    PaymentForm,
    BankStatementForm,
    InsuranceForm,
    InsuranceClaimForm
)

from .models import (
    Salary,
    Payment,
    BankStatement,
    Insurance,
    InsuranceClaim
)
from reports.models import Notification


@login_required
def salary_list(request):

    if request.user.role != 'ACCOUNTANT':
        return render(
            request,
            'payroll/access_denied.html'
        )

    salaries = Salary.objects.select_related(
        'employee'
    ).order_by(
        '-effective_from'
    )

    return render(
        request,
        'payroll/salary_list.html',
        {
            'salaries': salaries
        }
    )


@login_required
def add_salary(request):

    if request.user.role != 'ACCOUNTANT':
        return render(
            request,
            'payroll/access_denied.html'
        )

    if request.method == 'POST':

        form = SalaryForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'salary_list'
            )

    else:

        form = SalaryForm()

    return render(
        request,
        'payroll/salary_form.html',
        {
            'form': form
        }
    )


@login_required
def edit_salary(request, salary_id):

    if request.user.role != 'ACCOUNTANT':
        return render(
            request,
            'payroll/access_denied.html'
        )

    salary = get_object_or_404(
        Salary,
        id=salary_id
    )

    if request.method == 'POST':

        form = SalaryForm(
            request.POST,
            instance=salary
        )

        if form.is_valid():

            form.save()

            return redirect(
                'salary_list'
            )

    else:

        form = SalaryForm(
            instance=salary
        )

    return render(
        request,
        'payroll/salary_form.html',
        {
            'form': form,
            'salary': salary
        }
    )


# =========================
# PAYMENT VIEWS
# =========================


@login_required
def payment_list(request):

    if request.user.role != 'ACCOUNTANT':
        return render(
            request,
            'payroll/access_denied.html'
        )

    payments = Payment.objects.select_related(
        'employee',
        'salary',
        'processed_by'
    ).order_by(
        '-payment_date',
        '-created_at'
    )

    return render(
        request,
        'payroll/payment_list.html',
        {
            'payments': payments
        }
    )


@login_required
def add_payment(request):

    if request.user.role != 'ACCOUNTANT':
        return render(
            request,
            'payroll/access_denied.html'
        )

    if request.method == 'POST':

        form = PaymentForm(
            request.POST
        )

        if form.is_valid():

            payment = form.save(
                commit=False
            )

            payment.processed_by = request.user

            payment.save()

            return redirect(
                'payment_list'
            )

    else:

        form = PaymentForm()

    return render(
        request,
        'payroll/payment_form.html',
        {
            'form': form
        }
    )


@login_required
def edit_payment(request, payment_id):

    if request.user.role != 'ACCOUNTANT':
        return render(
            request,
            'payroll/access_denied.html'
        )

    payment = get_object_or_404(
        Payment,
        id=payment_id
    )

    if request.method == 'POST':

        form = PaymentForm(
            request.POST,
            instance=payment
        )

        if form.is_valid():

            payment = form.save(
                commit=False
            )

            payment.processed_by = request.user

            payment.save()

            return redirect(
                'payment_list'
            )

    else:

        form = PaymentForm(
            instance=payment
        )

    return render(
        request,
        'payroll/payment_form.html',
        {
            'form': form,
            'payment': payment
        }
    )
# =========================
# BANK STATEMENT VIEWS
# =========================


@login_required
def bank_statement_list(request):

    if request.user.role != 'ACCOUNTANT':
        return render(
            request,
            'payroll/access_denied.html'
        )

    statements = BankStatement.objects.all().order_by(
        '-transaction_date',
        '-created_at'
    )

    return render(
        request,
        'payroll/bank_statement_list.html',
        {
            'statements': statements
        }
    )


@login_required
def add_bank_statement(request):

    if request.user.role != 'ACCOUNTANT':
        return render(
            request,
            'payroll/access_denied.html'
        )

    if request.method == 'POST':

        form = BankStatementForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'bank_statement_list'
            )

    else:

        form = BankStatementForm()

    return render(
        request,
        'payroll/bank_statement_form.html',
        {
            'form': form
        }
    )


@login_required
def edit_bank_statement(request, statement_id):

    if request.user.role != 'ACCOUNTANT':
        return render(
            request,
            'payroll/access_denied.html'
        )

    statement = get_object_or_404(
        BankStatement,
        id=statement_id
    )

    if request.method == 'POST':

        form = BankStatementForm(
            request.POST,
            instance=statement
        )

        if form.is_valid():

            form.save()

            return redirect(
                'bank_statement_list'
            )

    else:

        form = BankStatementForm(
            instance=statement
        )

    return render(
        request,
        'payroll/bank_statement_form.html',
        {
            'form': form,
            'statement': statement
        }
    )
@login_required
def insurance_list(request):
    if request.user.role != 'ACCOUNTANT':
        return render(request, 'payroll/access_denied.html')

    insurances = Insurance.objects.select_related(
        'employee'
    ).all().order_by('-created_at')

    return render(
        request,
        'payroll/insurance_list.html',
        {'insurances': insurances}
    )


@login_required
def add_insurance(request):
    if request.user.role != 'ACCOUNTANT':
        return render(request, 'payroll/access_denied.html')

    if request.method == 'POST':
        form = InsuranceForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('insurance_list')

    else:
        form = InsuranceForm()

    return render(
        request,
        'payroll/insurance_form.html',
        {'form': form}
    )
@login_required
def submit_insurance_claim(request):
    if request.user.role not in ['STAFF', 'MANAGER', 'ACCOUNTANT']:
        return render(request, 'payroll/access_denied.html')

    try:
        insurance = request.user.insurance
    except Insurance.DoesNotExist:
        return render(
            request,
            'payroll/no_insurance.html'
        )

    if request.method == 'POST':
        form = InsuranceClaimForm(
            request.POST,
            request.FILES
        )

        if form.is_valid():
            claim = form.save(commit=False)
            claim.employee = request.user
            claim.insurance = insurance
            claim.save()

            return redirect('my_insurance_claims')

    else:
        form = InsuranceClaimForm()

    return render(
        request,
        'payroll/insurance_claim_form.html',
        {
            'form': form,
            'insurance': insurance
        }
    )
@login_required
def my_insurance_claims(request):
    if request.user.role not in ['STAFF', 'MANAGER', 'ACCOUNTANT']:
        return render(
            request,
            'payroll/access_denied.html'
        )

    claims = InsuranceClaim.objects.select_related(
        'insurance',
        'employee'
    ).filter(
        employee=request.user
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'payroll/my_insurance_claims.html',
        {
            'claims': claims
        }
    )
@login_required
def insurance_claim_list(request):
    if request.user.role != 'ACCOUNTANT':
        return render(
            request,
            'payroll/access_denied.html'
        )

    claims = InsuranceClaim.objects.select_related(
        'employee',
        'insurance'
    ).order_by(
        '-created_at'
    )

    return render(
        request,
        'payroll/insurance_claim_list.html',
        {
            'claims': claims
        }
    )
@login_required
def approve_insurance_claim(request, claim_id):

    if request.user.role != 'ACCOUNTANT':
        return render(
            request,
            'payroll/access_denied.html'
        )

    claim = get_object_or_404(
        InsuranceClaim,
        id=claim_id
    )

    if claim.status != InsuranceClaim.ClaimStatus.PENDING:
        return redirect('insurance_claim_list')

    if not claim.insurance.is_active:
        return redirect('insurance_claim_list')

    if claim.claim_amount > claim.insurance.coverage_amount:
        return redirect('insurance_claim_list')

    claim.status = InsuranceClaim.ClaimStatus.APPROVED
    claim.reviewed_by = request.user
    claim.reviewed_at = timezone.now()
    claim.save()

    Notification.objects.create(
        employee=claim.employee,
        title='Insurance Claim Approved',
        message=(
            f'Your insurance claim of ₹{claim.claim_amount} '
            f'has been approved.'
        )
    )

    return redirect('insurance_claim_list')


@login_required
def reject_insurance_claim(request, claim_id):

    if request.user.role != 'ACCOUNTANT':
        return render(
            request,
            'payroll/access_denied.html'
        )

    claim = get_object_or_404(
        InsuranceClaim,
        id=claim_id
    )

    if claim.status != InsuranceClaim.ClaimStatus.PENDING:
        return redirect('insurance_claim_list')

    claim.status = InsuranceClaim.ClaimStatus.REJECTED
    claim.reviewed_by = request.user
    claim.reviewed_at = timezone.now()
    claim.save()

    Notification.objects.create(
        employee=claim.employee,
        title='Insurance Claim Rejected',
        message=(
            f'Your insurance claim of ₹{claim.claim_amount} '
            f'has been rejected.'
        )
    )

    return redirect('insurance_claim_list')