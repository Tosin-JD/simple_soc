from django.urls import path
from posts import views

app_name = 'posts'

urlpatterns = [
    path('', views.PostList.as_view(), name='all'),
    path('<int:pk>/detail/', views.SinglePostDetail.as_view(), name='each'),
    path('by/<username>', views.UserPost.as_view(), name='for_user'),
    path('new/<int:group_id>', views.PostToGroup.as_view(), name='create'),
    path('by/<username>/<int:pk>', views.PostDetailForUser.as_view(), name='single'),
    path('delete/<int:pk>', views.DeletePost.as_view(), name='delete'),
    path('<int:post_id>/comment/', views.CreateComment.as_view(), name='create_comment'),
    path('edit-comment/<int:pk>/', 
         views.EditComment.as_view(), name='edit_comment'),
    path('comment-delete/<int:pk>/',
         views.DeleteComment.as_view(), name='comment_delete'),
]
