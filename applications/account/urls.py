from django.urls import path
from applications.account.views import (
    RegisterApiView, ActivationApiView, ForgotPasswordCompleteApiview, ForgotPasswordApiView, ChangePasswordApiView
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)


urlpatterns = [
    path('register/', RegisterApiView.as_view()),
    path('activate/<uuid:activation_code>/', ActivationApiView.as_view()),
    path('login/', TokenObtainPairView.as_view()),
    path('change_password/', ChangePasswordApiView.as_view()),
    path('forgot_password/', ForgotPasswordApiView.as_view()),
    path('forgot_password_complete/', ForgotPasswordCompleteApiview.as_view()),
    path('refresh/', TokenRefreshView.as_view())
]