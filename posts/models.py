from django.db import models
from django.urls import reverse, reverse_lazy
from django.conf import settings
from groups.models import Group
from accounts.models import MyUser

# Create your models here.
User = MyUser


class Post(models.Model):
    """This is the models for each post a user makes"""
    user = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='post_images')
    title = models.CharField(max_length=50)
    message = models.TextField()
    message_html = models.TextField()
    group = models.ForeignKey(Group,
                              on_delete=models.CASCADE,
                              related_name='posts',
                              null=True, blank=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """it will return to this url if it is
        successful and there is no success url provided"""
        return reverse('posts:each', kwargs={
            'pk': self.pk})

    class Meta:
        """this tells django to order the post by time
        also to make sure every post from a user is unique"""
        ordering = ['-created_at']
        unique_together = ['user', 'message']


class Comment(models.Model):
    """This is for the comment that a user makes
    to a post"""
    text = models.CharField(max_length=256)
    time_stamp = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comment')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """display the username and string
        comment wherever it is instantiated"""
        return self.author.username + " comment"

    def get_absolute_url(self):
        """return to this url if there is any
        action that was successfully performed"""
        return reverse_lazy("posts:each", kwargs={'pk': self.post.pk})

    class Meta:
        """order the comments by the time
        in which they were made"""
        ordering = ['-time_stamp']
