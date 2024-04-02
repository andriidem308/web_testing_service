from django.urls import path

from main.create_models_view import (create_all_models, create_groups, create_students, create_teachers,
                                     create_lectures, create_problems)
from main.views import (GroupCreateView, GroupDeleteView, GroupListView, GroupUpdateView, GroupView, index,
                        LectureCreateView, LectureDeleteView, LectureListView, LectureUpdateView, LectureView,
                        ProblemCreateView, ProblemDeleteView, ProblemListView, ProblemSolutionListView,
                        ProblemSolutionView, ProblemTakeView, ProblemUpdateView, ProblemView, question_add, questions,
                        TestCreateView, TestDeleteView, TestListView, TestUpdateView, TestView, view_notification)

urlpatterns = [
    path('', index, name='home'),

    path('problems/', ProblemListView.as_view(), name='problems'),
    path('problems/add/', ProblemCreateView.as_view(), name='problem_add'),
    path('problems/<int:pk>/', ProblemView.as_view(), name='problem'),
    path('problems/<int:pk>/edit/', ProblemUpdateView.as_view(), name='problem_edit'),
    path('problems/<int:pk>/delete/', ProblemDeleteView.as_view(), name='problem_delete'),
    path('problems/<int:pk>/take/', ProblemTakeView.as_view(), name='problem_take'),
    path('problems/<int:pk>/solutions/', ProblemSolutionListView.as_view(), name='solutions'),
    path('solutions/<int:pk>', ProblemSolutionView.as_view(), name='solution'),

    path('lectures/', LectureListView.as_view(), name='lectures'),
    path('lectures/add/', LectureCreateView.as_view(), name='lecture_add'),
    path('lectures/<int:pk>/', LectureView.as_view(), name='lecture'),
    path('lectures/<int:pk>/edit/', LectureUpdateView.as_view(), name='lecture_edit'),
    path('lectures/<int:pk>/delete/', LectureDeleteView.as_view(), name='lecture_delete'),

    path('groups/', GroupListView.as_view(), name='groups'),
    path('groups/add/', GroupCreateView.as_view(), name='group_add'),
    path('groups/<int:pk>/', GroupView.as_view(), name='group'),
    path('groups/<int:pk>/edit/', GroupUpdateView.as_view(), name='group_edit'),
    path('groups/<int:pk>/delete/', GroupDeleteView.as_view(), name='group_delete'),

    path('tests/', TestListView.as_view(), name='tests'),
    path('tests/add/', TestCreateView.as_view(), name='test_add'),
    path('tests/<int:pk>/', TestView.as_view(), name='test'),
    path('tests/<int:pk>/edit/', TestUpdateView.as_view(), name='test_edit'),
    path('tests/<int:pk>/delete/', TestDeleteView.as_view(), name='test_delete'),
    path('tests/<int:pk>/questions/', questions, name='questions'),
    path('tests/<int:pk>/questions/add', question_add, name='question_add'),

    path('view_notification/<int:pk>', view_notification, name='view_notification'),
]

create_models_urls = [
    path('create_all_models/', create_all_models, name='create_all_models'),
    path('create_teachers/', create_teachers, name='create_teachers'),
    path('create_students/', create_students, name='create_students'),
    path('create_groups/', create_groups, name='create_groups'),
    path('create_problems/', create_problems, name='create_problems'),
    path('create_lectures/', create_lectures, name='create_lectures'),
]

urlpatterns += create_models_urls
