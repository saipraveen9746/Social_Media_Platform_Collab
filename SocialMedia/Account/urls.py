from django.urls import path
from . import views
from .views import *


urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
    path('login/', views.UserloginView.as_view()),
    path('user-profile/', views.UserProfileAPIView.as_view(),),
    path('CreateFollower/<int:user_id>/', views.CreateFollower.as_view(),name='CreateFollower'),
    path('authenticated-user-profile/', views.UserProfileAPIView.as_view(),),
    path('followingslist/',views.UserFollowingList.as_view()),
    path('followerslist/',views.UserFollowerList.as_view()),
    path('users/', CustomUserList.as_view(), name='user-list'),
    path('users/<int:user_id>/followers/', FollowersList.as_view(), name='followers-list'),
    path('users/<int:user_id>/following/', FollowingList.as_view(), name='following-list'),
    path('createbio/',CreateBioView.as_view(),name='create-bio')

    


    
]

