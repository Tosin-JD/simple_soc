from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from accounts.models import MyUser
from django.contrib.auth.forms import UserCreationForm


# Create custom forms for the site
class SignUpForm(ModelForm):
    """form for users to signup"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    password1.widget.attrs.update({'class': 'form-control'})
    password2.widget.attrs.update({'class': 'form-control'})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['date_of_birth'].widget.attrs.update({'class': 'form-control'})
        self.fields['profile_pic'].widget.attrs.update({'class': 'form-control'})
        self.fields['username'].widget.attrs.update({'class': 'form-control'})
        self.fields['gender'].widget.attrs.update({'class': 'form-control'})

    class Meta:
        """this are the fields that I want to
        be displayed on the signup form"""
        model = MyUser
        fields = ('username', 'email', 'gender', 'date_of_birth', 'profile_pic')

    def clean_password2(self):
        """Check that the two password entries match"""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """Save the provided password in hashed format"""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
