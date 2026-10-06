from django import forms

from .models import (
    Salary,
    Payment,
    BankStatement,
    Insurance,
    InsuranceClaim
)


class SalaryForm(forms.ModelForm):

    class Meta:
        model = Salary

        fields = [
            'employee',
            'basic_salary',
            'allowances',
            'deductions',
            'effective_from',
        ]

        widgets = {
            'effective_from': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
        }


class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment

        fields = [
            'employee',
            'salary',
            'amount',
            'payment_date',
            'payment_method',
            'payment_status',
            'transaction_reference',
        ]

        widgets = {
            'payment_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
        }


class BankStatementForm(forms.ModelForm):

    class Meta:
        model = BankStatement

        fields = [
            'transaction_date',
            'transaction_reference',
            'description',
            'transaction_type',
            'amount',
            'bank_name',
            'reconciled',
        ]

        widgets = {
            'transaction_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
        }


class InsuranceForm(forms.ModelForm):

    class Meta:
        model = Insurance

        fields = [
            'employee',
            'insurance_provider',
            'policy_number',
            'coverage_amount',
            'start_date',
            'end_date',
            'is_active',
        ]

        widgets = {
            'start_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
            'end_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),
        }

    def clean_coverage_amount(self):

        coverage_amount = self.cleaned_data['coverage_amount']
        employee = self.cleaned_data.get('employee')

        if not employee:
            return coverage_amount

        coverage_limits = {
            'STAFF': 500000,
            'ACCOUNTANT': 1000000,
            'MANAGER': 1500000,
        }

        maximum_coverage = coverage_limits.get(
            employee.role
        )

        if maximum_coverage is None:
            raise forms.ValidationError(
                'Insurance is not available for this role.'
            )

        if coverage_amount > maximum_coverage:
            raise forms.ValidationError(
                f'Maximum insurance coverage for '
                f'{employee.get_role_display()} is '
                f'₹{maximum_coverage:,.0f}.'
            )

        return coverage_amount


class InsuranceClaimForm(forms.ModelForm):

    class Meta:
        model = InsuranceClaim

        fields = [
            'claim_amount',
            'claim_reason',
            'medical_certificate',
        ]

        widgets = {
            'claim_reason': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Explain the reason for your insurance claim...'
                }
            ),
        }

    def __init__(self, *args, insurance=None, **kwargs):

        super().__init__(*args, **kwargs)

        self.insurance = insurance

    def clean_claim_amount(self):

        claim_amount = self.cleaned_data['claim_amount']

        if self.insurance:

            if not self.insurance.is_active:
                raise forms.ValidationError(
                    'Your insurance policy is not active.'
                )

            if claim_amount > self.insurance.coverage_amount:
                raise forms.ValidationError(
                    f'Claim amount cannot exceed your insurance '
                    f'coverage of ₹{self.insurance.coverage_amount:,.2f}.'
                )

        return claim_amount