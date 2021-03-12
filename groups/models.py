from django.db import models
from django.urls import reverse
from django.utils.text import  slugify
from django.contrib.auth import get_user_model
from django import template
from accounts.models import MyUser


# Create your models here.
User = MyUser
register = template.Library()


class Group(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    members = models.ManyToManyField(User, through='GroupMember')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """if a group is created or deleted,
        it should return to this url as the default"""
        return reverse('groups:single', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='memeberships', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

