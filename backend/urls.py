from django.urls import path
from . import views
from .views import MyTokenObtainPairView, RegisterUser

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('', views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterUser.as_view(), name='register'),
    # path('login/', LoginUser.as_view(), name='login'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
]