from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, DetailView
from . import forms
from accounts.models import MyUser


# Create your views here.
class HomePage(TemplateView):
    """This is the view for the home page."""
    template_name = 'index.html'


class ThanksPage(TemplateView):
    """users will be redirected to this view if they
    log out"""
    template_name = 'accounts/thanks.html'


class SignUp(CreateView):
    """This is the view for users to signup"""
    form_class = forms.SignUpForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/sign_up.html'


class ProfileView(TemplateView, LoginRequiredMixin):
    """this is the view for user profiles"""
    model = MyUser
    template_name = 'accounts/user_profile.html'


