from django import forms
from .models import User


class EmployeeCreationForm(forms.ModelForm):

    password = forms.CharField(
        widget=forms.PasswordInput,
        min_length=8
    )

    class Meta:
        model = User

        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'employee_id',
            'phone',
            'role',
            'department',
            'manager',
            'joining_date',
            'profile_image',
            'password',
        ]

        widgets = {
            'joining_date': forms.DateInput(
                attrs={'type': 'date'}
            ),
        }

    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        self.fields['manager'].queryset = User.objects.filter(
            role=User.Role.MANAGER
        )

    def clean_role(self):

        role = self.cleaned_data['role']

        if role == User.Role.ADMIN:

            raise forms.ValidationError(
                'Admin accounts cannot be created here.'
            )

        return role


class LoginForm(forms.Form):

    username = forms.CharField(
        max_length=150
    )

    password = forms.CharField(
        widget=forms.PasswordInput
    )


class ProfileUpdateForm(forms.ModelForm):

    class Meta:

        model = User

        fields = [
            'first_name',
            'last_name',
            'email',
            'phone',
            'profile_image',
        ]