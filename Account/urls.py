from django.urls import path
from Account import views

urlpatterns = [
    path('signup', views.AccountSignupView.as_view(), name='Signup'),
    path('login', views.AccountLoginView.as_view(), name='Login'),
    path('logout', views.LogoutView.as_view(), name='Logout'),
    path('forget-pass', views.ForgotPasswordView.as_view(), name='Forgot-Password'),
    path('reset-pass/<email_verified>', views.ResetPasswordView.as_view(), name='Reset-Password'),
    path('activated-code/<email_verified>', views.ActivatedCodeView.as_view(), name='Activated-code'),
]
