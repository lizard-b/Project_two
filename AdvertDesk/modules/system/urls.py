from django.urls import path

from .views import (ProfileUpdateView, ProfileDetailView,
                    UserRegisterView, UserLoginView, UserLogoutView,
                    UserPasswordChangeView, UserForgotPasswordView,
                    UserPasswordResetConfirmView, EmailConfirmationSentView,
                    EmailConfirmedView, EmailConfirmationFailedView,
                    OTPVerificationView, RequestNewOTPView,
                    )

urlpatterns = [
    path('user/edit/', ProfileUpdateView.as_view(), name='profile_edit'),
    path('user/<str:slug>/', ProfileDetailView.as_view(), name='profile_detail'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('password-change/', UserPasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', UserForgotPasswordView.as_view(), name='password_reset'),
    path('set-new-password/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('register/', UserRegisterView.as_view(), name='register'),
    path('email-confirmation-sent/', EmailConfirmationSentView.as_view(), name='email_confirmation_sent'),
    path('verify-email/', OTPVerificationView.as_view(), name='verify_email'),
    path('request-new-otp/', RequestNewOTPView.as_view(), name='request_new_otp'),
    path('email-confirmed/', EmailConfirmedView.as_view(), name='email_confirmed'),
    path('confirm-email-failed/', EmailConfirmationFailedView.as_view(), name='email_confirmation_failed'),
]
