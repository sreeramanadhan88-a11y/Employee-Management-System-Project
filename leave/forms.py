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
            'from_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'to_date': forms.DateInput(
                attrs={'type': 'date'}
            ),

            'reason': forms.Textarea(
                attrs={
                    'rows': 4
                }
            ),
        }