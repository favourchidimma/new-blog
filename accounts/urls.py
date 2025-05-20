from django.urls import path
from .views import *


urlpatterns = [
    path('user/',UserGenericView.as_view()),
    path('user/<int:pk>', UserGenericByOne.as_view()),
    path('otp/verify/', OtpVerifyView.as_view()),
    path('login/', LoginView.as_view()),
    path('change_password/', ChangePasswordView.as_view()),
    path('logout/', LogoutView.as_view())
]