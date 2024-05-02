from django.urls import path
from . import views

urlpatterns = [
    path('feed/',views.Feed.as_view()),
    
    path('list_posts_of_authenticatedUser/',views.AuthenticatedUserPostListView.as_view()),
    path('create-post/', views.CreatePostView.as_view(),),
    path('like-unlike-post/',views.Like_dislikePostView.as_view()),
    path('list-liked-users-of-post/<int:post_id>/', views.ListlikedusesForPostView.as_view(),),
    path('post-delete/<int:pk>/', views.DeletePostView.as_view(),),
    
    
    path('comments-create/', views.CreateCommentView.as_view(),),  
    path('list-comments-of-post/<int:post_id>/', views.ListCommentsForPostView.as_view(),),
    path('comment-delete/<int:pk>/', views.DeleteCommentView.as_view(),),
    
]