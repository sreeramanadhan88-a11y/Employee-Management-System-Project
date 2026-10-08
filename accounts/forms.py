from django import forms
from .models import User


class EmployeeCreationForm(forms.ModelForm):

    username = forms.CharField(
        max_length=150,
        help_text='',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter username'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter password'
            }
        ),
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

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter email address'
                }
            ),

            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter first name'
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter last name'
                }
            ),

            'employee_id': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter employee ID'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter phone number'
                }
            ),

            'role': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'department': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'manager': forms.Select(
                attrs={
                    'class': 'form-select'
                }
            ),

            'joining_date': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                }
            ),

            'profile_image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
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
        max_length=150,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter username',
                'autocomplete': 'username'
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter password',
                'autocomplete': 'current-password'
            }
        )
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

        widgets = {

            'first_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter first name'
                }
            ),

            'last_name': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter last name'
                }
            ),

            'email': forms.EmailInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter email address'
                }
            ),

            'phone': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Enter phone number'
                }
            ),

            'profile_image': forms.ClearableFileInput(
                attrs={
                    'class': 'form-control'
                }
            ),
        }