from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from groups.models import Group, GroupMember

# Create your views here.


class CreateGroup(LoginRequiredMixin, CreateView):
    fields = ('name', 'description')
    model = Group


class SingleGroup(DetailView):
    model = Group


class ListGroups(ListView):
    """show all the groups available"""
    model = Group


class JoinGroup(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self, *args, **kwargs):
        group = get_object_or_404(Group, slug=self.kwargs.get('slug'))
        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except IntegrityError:
            messages.warning(self.request, 'Warning, already a member.')
        else:
            messages.success(self.request, 'You are now a member')
        return super().get(*args, **kwargs)


class LeaveGroup(LoginRequiredMixin, RedirectView):
    def get_redirect_url(self, *args, **kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self, *args, **kwargs):

        try:
            membership = GroupMember.objects.filter(user=self.request.user,
                                                    group__slug=self.kwargs.get('slug')).get()
        except GroupMember.DoesNotExist:
            messages.warning(self.request, 'Sorry, you are not in this group')
        else:
            membership.delete()
            messages.success(self.request, 'You are now part of the group.')
        return super().get(*args, **kwargs)



