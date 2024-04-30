from django.urls import path
from . import views
from .views import CreateFollower

urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
    path('login/', views.UserloginView.as_view()),
    path('user-profile/', views.UserProfileAPIView.as_view(),),
    path('CreateFollower/<int:user_id>/', views.CreateFollower.as_view(),name='CreateFollower'),
    path('authenticated-user-profile/', views.UserProfileAPIView.as_view(),),
    
]