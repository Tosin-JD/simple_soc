from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView, CreateView, DetailView, DeleteView, ListView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from groups.models import Group
from accounts.models import MyUser
from django.http import Http404, HttpResponse
from posts import models
from .models import Post, Comment

from braces.views import SelectRelatedMixin

from posts.forms import PostToGroupForm, CommentForm

User = MyUser


# Create your views here.
class PostList(SelectRelatedMixin, ListView):
    """the list of posts of members of a particular
    group"""
    model = models.Post
    select_related = ('user', 'group')
    template_name = 'posts/post_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data(**kwargs)
        context['get_user_groups'] = Group.objects.prefetch_related('members')
        context['get_other_groups'] = Group.objects.all()
        return context
    

class UserPost(ListView):
    """contains the list of post of
    a specific member of a group"""
    model = models.Post
    template_name = 'posts/user_post_list.html'

    def get_queryset(self):
        """had check for the username of
        a user to extract their own  post"""
        try:
            self.post_user = \
                User.objects.prefetch_related('posts').get\
                    (username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        """return the post that is specific
        to every user."""
        context = super().get_context_data(**kwargs)
        context['post_user'] = self.post_user
        return context


class SinglePostDetail(DetailView):
    """this will provide the details of a
    post not related to a group"""
    model = models.Post
    template_name = 'posts/single_post_detail.html'

    def get(self, request, *args, **kwargs):
       self.post_comment =get_object_or_404(Post, id=kwargs['pk'])
       return super(SinglePostDetail, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """add the comments to what will be displayed
        in the template"""
        context = super().get_context_data(**kwargs)
        member_comments = Comment.objects.filter(post_id=self.post_comment.id)
        context['member_comments'] = member_comments
        return context


class PostDetailForUser(SelectRelatedMixin, DetailView):
    """This will display the details of the post
    related to a group and a user"""
    model = models.Post
    template_name = 'posts/posts_detail.html'
    select_related = ('user', 'group')

    def get_queryset(self):
        """Select the post belonging to a
        specific user"""
        queryset = super().get_queryset()
        return \
            queryset.filter(user__username__iexact=
                            self.kwargs.get('username'))


class PostToGroup(LoginRequiredMixin, CreateView):
    """handles post that a user makes to
    a particular particular group"""
    model = models.Post
    form_class = PostToGroupForm
    template_name = 'posts/new_post.html'
    success_url = reverse_lazy('posts:all')
    
    def get_context_data(self, **kwargs):
        self.group = get_object_or_404(Group, id=self.kwargs['group_id'])
        kwargs['group'] = self.group
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        """overwrite the parent form in order
        to add the group and user"""
        self.group = get_object_or_404(Group, id=self.kwargs['group_id'])
        form.instance.group = self.group    
        form.instance.user = self.request.user
        messages.success(self.request, 'Post successful!')
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, DeleteView):
    """This is the view for deleting post."""
    model = models.Post
    select_related = ('user', 'group')
    success_url = reverse_lazy('posts:all')

    def get_queryset(self):
        """get the post pertaining to a specific user"""
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        """override the parent delete method to
        display successful message"""
        messages.success(self.request, "Post Deleted")
        return super().delete(*args, **kwargs)


class CreateComment(LoginRequiredMixin, CreateView):
    """this view is for creating comments
    on a post"""
    model = models.Comment
    fields = ('text',)

    def get(self, request, *args, **kwargs):
        """override the parent get to get the mother post"""
        self.post = Post.objects.get(id=self.kwargs['post_id'])
        return super(CreateComment, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """override the parent to add post"""
        self.post = get_object_or_404(Post, id=kwargs['post_id'])
        kwargs['post'] = self.post
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        """override the parent to add the related post"""
        self.post = get_object_or_404(Post, id=self.kwargs['post_id'])
        form.instance.post = self.post
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditComment(LoginRequiredMixin, UpdateView):
    """if a user is to edit their comment"""
    model = models.Comment
    form_class = CommentForm
    template_name = "posts/edit_comment.html"
    
    def get_context_data(self, **kwargs):
        """override the parent to add post"""
        self.post = get_object_or_404(Post, id=kwargs['post_id'])
        kwargs['post'] = self.post
        return super().get_context_data(**kwargs)
    
    def get_success_url(self):
        """return to this url if it was 
        successful editing it"""
        return  reverse_lazy('posts:all')
    

class DeleteComment(LoginRequiredMixin, DeleteView):
    """This is for deleting comments"""
    model = models.Comment
    template_name = "posts/comment_delete.html"

    def get_success_url(self):
        """return to the post if the delete wa successful"""
        return reverse_lazy('posts:all')
    
    





