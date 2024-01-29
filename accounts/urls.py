from django.contrib import admin
from django.urls import path, include
# from main.views import index
from main.views.common_views import index
from main.views import teacher_views, student_views

from accounts.views import (_login, signupt, signups, signup_student, signup_teacher, profile,
                            SignUpStudentView, SignUpTeacherView, SignUpView, LoginView)


urlpatterns = [
    path('profile/', profile, name='profile'),
    # path('login/', _login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    # path('signupt/', signupt, name='signupt'),
    # path('signups/', signups, name='signups'),
    path('signup/<str:user_type>/', SignUpView.as_view(), name='signup'),
    path('signupstudent/', SignUpStudentView.as_view(), name='signupstudent'),
    path('signupteacher/', SignUpTeacherView.as_view(), name='signupteacher'),
    path('signup/teacher/', signup_teacher, name='signup_teacher'),
    path('signup/student/', signup_student, name='signup_student'),
]
