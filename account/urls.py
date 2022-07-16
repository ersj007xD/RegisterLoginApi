from django.urls import path
from account.views import UserRegistrationView
from account.views import UserLoginView
from . import views

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('user_details/<str:name>', views.User_view),

]
