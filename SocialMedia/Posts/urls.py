from django.urls import path
from . import views

urlpatterns = [
    path('listpostsofauthenticateduser/',views.AuthenticatedUserPostListView.as_view()),
    path('create-post/', views.CreatePostView.as_view(), name='create-post'),
    path('like-unlike-post/',views.Like_dislikePostView.as_view()),
    path('post-delete/<int:pk>/', views.DeletePostView.as_view(), name='delete-comment'),
    
    
    path('comments-create/', views.CreateCommentView.as_view(), name='create-comment'),
    
    path('list-comments-of-post/<int:post_id>/', views.ListCommentsForPostView.as_view(), name='list-comments-for-post'),
    path('comment-delete/<int:pk>/', views.DeleteCommentView.as_view(), name='delete-comment'),
    
]