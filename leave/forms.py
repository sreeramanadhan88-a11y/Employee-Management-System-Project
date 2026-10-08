from django import forms
from .models import LeaveRequest


class LeaveRequestForm(forms.ModelForm):

    class Meta:

        model = LeaveRequest

        fields = [
            'leave_type',
            'from_date',
            'to_date',
            'reason',
        ]

        widgets = {

            'leave_type': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter leave type (e.g. Casual Leave)'
                }
            ),

            'from_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'to_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'reason': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 4,
                    'placeholder': 'Enter the reason for your leave'
                }
            ),
        }