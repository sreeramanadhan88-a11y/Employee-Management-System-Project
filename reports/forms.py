from django import forms

from .models import DailyReport


class DailyReportForm(forms.ModelForm):

    class Meta:
        model = DailyReport

        fields = [
            'report_date',
            'work_title',
            'work_description',
        ]

        widgets = {
            'report_date': forms.DateInput(
                attrs={
                    'type': 'date'
                }
            ),

            'work_description': forms.Textarea(
                attrs={
                    'rows': 5,
                    'placeholder': 'Describe the work you completed today...'
                }
            ),
        }