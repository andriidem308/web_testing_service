from django.contrib.auth.views import LogoutView
from django.urls import path

from accounts.views import LoginView, profile, SignUpView

urlpatterns = [
    path('profile/', profile, name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/<str:user_type>/', SignUpView.as_view(), name='signup'),

]
