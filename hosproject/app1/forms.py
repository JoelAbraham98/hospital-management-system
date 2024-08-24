from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Patient,Doctor

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone_number = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=None,
    )
    password2 = forms.CharField(
        label="Password Confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control'}),
        help_text=None,
    )

    class Meta:
        model = User
        fields = [
            'first_name', 'last_name', 'username', 'email', 'phone_number','password1', 'password2'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'username', 'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}),
        }

class CustomLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'autocomplete': 'username', 'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'username',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'autocomplete': 'current-password',
        })


class PatientForm(forms.ModelForm):
    TIME_CHOICES = [
        ('9-10', '9-10'),
        ('10-11', '10-11'),
        ('11-12', '11-12'),
        ('1-2', '1-2'),
        ('2-3', '2-3'),
        ('3-4', '3-4'),
        ('4-5', '4-5'),
    ]
    
    slot = forms.ChoiceField(choices=TIME_CHOICES, required=True, widget=forms.Select(attrs={'class': 'form-control'}))
    
    appointment_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
        required=True
    )

    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'date_of_birth', 'address', 'phone_number', 'gender', 'appointment_date', 'slot']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Last Name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'YYYY-MM-DD'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter Address'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'}),
            'gender': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['appointment_date'].required = True
        self.fields['slot'].required = True