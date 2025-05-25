from django.urls.conf import path

from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from accounts.api.views import UserRegisterApiView

urlpatterns = [
    path('register/', UserRegisterApiView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
