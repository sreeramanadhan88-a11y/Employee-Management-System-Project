from django import forms

from .models import DailyReport, Announcement


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
                    'type': 'date',
                    'class': 'form-control',
                }
            ),

            'work_title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter the title of your work',
                }
            ),

            'work_description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Describe the work you completed today...',
                }
            ),
        }


class AnnouncementForm(forms.ModelForm):

    class Meta:

        model = Announcement

        fields = [
            'title',
            'message',
        ]

        widgets = {

            'title': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter announcement title',
                }
            ),

            'message': forms.Textarea(
                attrs={
                    'class': 'form-control',
                    'rows': 5,
                    'placeholder': 'Write your announcement here...',
                }
            ),
        }