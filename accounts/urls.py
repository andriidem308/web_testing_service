from django.urls import path
from django.contrib.auth.views import LogoutView
# from main.views import index

from accounts.views import (profile,
                            SignUpView, LoginView)


urlpatterns = [
    path('profile/', profile, name='profile'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/<str:user_type>/', SignUpView.as_view(), name='signup'),

    # path('login/', _login, name='login'),
    # path('signupt/', signupt, name='signupt'),
    # path('signups/', signups, name='signups'),
    # path('signupstudent/', SignUpStudentView.as_view(), name='signupstudent'),
    # path('signupteacher/', SignUpTeacherView.as_view(), name='signupteacher'),
    # path('signup/teacher/', signup_teacher, name='signup_teacher'),
    # path('signup/student/', signup_student, name='signup_student'),
]
