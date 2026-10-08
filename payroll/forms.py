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

            'employee': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'basic_salary': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter basic salary',
                    'step': '0.01',
                }
            ),

            'allowances': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter allowances',
                    'step': '0.01',
                }
            ),

            'deductions': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter deductions',
                    'step': '0.01',
                }
            ),

            'effective_from': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
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

            'employee': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'salary': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter payment amount',
                    'step': '0.01',
                }
            ),

            'payment_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),

            'payment_method': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'payment_status': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'transaction_reference': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter transaction reference',
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
                    'type': 'date',
                    'class': 'form-control',
                }
            ),

            'transaction_reference': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter transaction reference',
                }
            ),

            'description': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter transaction description',
                }
            ),

            'transaction_type': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter transaction amount',
                    'step': '0.01',
                }
            ),

            'bank_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter bank name',
                }
            ),

            'reconciled': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
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

            'employee': forms.Select(
                attrs={
                    'class': 'form-select',
                }
            ),

            'insurance_provider': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter insurance provider',
                }
            ),

            'policy_number': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter policy number',
                }
            ),

            'coverage_amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter coverage amount',
                    'step': '0.01',
                }
            ),

            'start_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),

            'end_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control',
                }
            ),

            'is_active': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
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

            'claim_amount': forms.NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter claim amount',
                    'step': '0.01',
                    'min': '0',
                }
            ),

            'claim_reason': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': (
                        'Explain the reason for your insurance claim...'
                    ),
                }
            ),

            'medical_certificate': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control',
                    'accept': '.pdf,.jpg,.jpeg,.png',
                }
            ),
        }

    def __init__(
        self,
        *args,
        insurance=None,
        **kwargs
    ):

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