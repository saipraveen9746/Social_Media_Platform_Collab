from django.urls import path
from .views import *
from Account import views


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
    path('updatebio/',UpdateBioView.as_view(),name='create-bio'),
    path('searchview/',UserSearchlistView.as_view(),name='searchview')

    


    
    
]

