from django.contrib import admin
from django.urls import path, include
# from main.views import index
from main.views.common_views import index
from main.views import teacher_views, student_views

from accounts.views import login, signupt, signups, signup_student, signup_teacher, profile


urlpatterns = [
    path('profile', profile, name='profile'),
    path('login/', login, name='login'),
    # path('signupt/', signupt, name='signupt'),
    # path('signups/', signups, name='signups'),
    path('signup/teacher/', signup_teacher, name='signup_teacher'),
    path('signup/student/', signup_student, name='signup_student'),
]