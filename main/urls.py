from django.urls import path, include
# from main.views import index
from main.views import *
from main import student_views, teacher_views

urlpatterns = [
    path('', index, name='home'),

    path('problems/', problems, name='problems'),
    path('problems/add/', problem_add, name='problem_add'),
    path('problems/<int:pk>/', problem, name='problem'),
    path('problems/<int:pk>/edit/', problem_edit, name='problem_edit'),
    path('problems/<int:pk>/take/', problem_take, name='problem_take'),

    path('lectures/', LectureListView.as_view(), name='lectures'),
    path('lectures/add/', LectureCreateView.as_view(), name='lecture_add'),
    path('lectures/<int:pk>/', LectureView.as_view(), name='lecture'),
    path('lectures/<int:pk>/edit/', LectureUpdateView.as_view(), name='lecture_edit'),

    path('groups/', GroupListView.as_view(), name='groups'),
    path('groups/add/', GroupCreateView.as_view(), name='group_add'),
    path('groups/<int:pk>/', GroupView.as_view(), name='group'),
    path('groups/<int:pk>/edit', GroupUpdateView.as_view(), name='group_edit'),

    # path(
    #     'teacher/',
    #     include(
    #         ([
    #             path('problems/', teacher_views.problem_list, name='problem_list'),
    #         ], 'main'),
    #         namespace='teachers'
    #     )
    # ),
    # path(
    #     'student/',
    #     include(
    #         ([
    #             path('problems/', student_views.problems, name='problems'),
    #             path('problem/', student_views.problem, name='problem'),
    #             path('lectures/', student_views.lectures, name='lectures'),
    #             path('lecture/', student_views.lecture, name='lecture'),
    #         ], 'main'),
    #         namespace='students'
    #     )
    # ),

    # path('')
]
