from django.contrib import admin
from django.urls import path, include
# from main.views import index
from main.views.common_views import index
from main.views import teacher_views, student_views


urlpatterns = [
    path('', index, name='home'),
    path(
        'teacher/',
        include(
            ([
                path('problems/', teacher_views.problem_list, name='problem_list'),
            ], 'main'),
            namespace='teachers'
        )
    ),
    path(
        'student/',
        include(
            ([
                path('problems/', student_views.problems, name='problems'),
                path('problem/', student_views.problem, name='problem'),
                path('lectures/', student_views.lectures, name='lectures'),
                path('lecture/', student_views.lecture, name='lecture'),
            ], 'main'),
            namespace='students'
        )
    ),
]
