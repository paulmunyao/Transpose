from knox import views as knox_views
from .views import RegisterAPI,LoginAPI
from django.urls import path
from .import views

urlpatterns = [
    path('register', RegisterAPI.as_view(), name='register'), 
    path('login', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout')
]
