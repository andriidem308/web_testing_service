from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import LoginView, profile, SignUpView, forbidden_view, PasswordChangeView

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/<str:user_type>/', SignUpView.as_view(), name='signup'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('forbidden/<str:user_type>/', forbidden_view, name='forbidden'),

]
