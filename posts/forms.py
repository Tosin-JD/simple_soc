"""Handle all the form for post and comments
of a particular user to a group"""

import django.forms
from django import forms
from .models import Comment, Post

                     
class PostToGroupForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostToGroupForm, self).__init__(*args, **kwargs)
        self.fields['image'].widget.attrs.update({'class':'form-control my-2'})
        self.fields['title'].widget.attrs.update({'class':'form-control my-2', 'placeholder':'Enter the title',})
        self.fields['message'].widget.attrs.update({'class':'form-control my-2', 'placeholder':'Enter your message...', 'row':2})
        
    class Meta:
        model = Post
        fields = ('image', 'title', 'message')


class CommentForm(forms.ModelForm):
    """handle all the form for comment"""
    
    class Meta:
        """specify the fields to be displayed
        and attach the Comment Model to the form"""
        model = Comment()
        fields = ('text',)
