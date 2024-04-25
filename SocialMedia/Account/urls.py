from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.RegistrationView.as_view()),
    path('login/', views.UserloginView.as_view()),
    
    path('user-profile/', views.UserProfileAPIView.as_view(),),
    
]