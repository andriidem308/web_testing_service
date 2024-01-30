from django.urls import path, include
# from main.views import index
from main.views import *

urlpatterns = [
    path('', index, name='home'),

    path('problems/', problems, name='problems'),
    path('problems/add/', ProblemCreateView.as_view(), name='problem_add'),
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
]
