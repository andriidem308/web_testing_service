from django.urls import path

from main import create_models_view, error_views
from main import views

urlpatterns = [
    path('', views.index, name='home'),

    path('problems/', views.ProblemListView.as_view(), name='problems'),
    path('problems/add/', views.ProblemCreateView.as_view(), name='problem_add'),
    path('problems/<int:pk>/', views.ProblemView.as_view(), name='problem'),
    path('problems/<int:pk>/edit/', views.ProblemUpdateView.as_view(), name='problem_edit'),
    path('problems/<int:pk>/delete/', views.ProblemDeleteView.as_view(), name='problem_delete'),
    path('problems/<int:pk>/take/', views.ProblemTakeView.as_view(), name='problem_take'),
    path('problems/<int:pk>/solutions/', views.ProblemSolutionListView.as_view(), name='solutions'),
    path('solutions/<int:pk>', views.ProblemSolutionView.as_view(), name='solution'),

    path('lectures/', views.LectureListView.as_view(), name='lectures'),
    path('lectures/add/', views.LectureCreateView.as_view(), name='lecture_add'),
    path('lectures/<int:pk>/', views.LectureView.as_view(), name='lecture'),
    path('lectures/<int:pk>/edit/', views.LectureUpdateView.as_view(), name='lecture_edit'),
    path('lectures/<int:pk>/delete/', views.LectureDeleteView.as_view(), name='lecture_delete'),

    path('groups/', views.GroupListView.as_view(), name='groups'),
    path('groups/add/', views.GroupCreateView.as_view(), name='group_add'),
    path('groups/<int:pk>/', views.GroupView.as_view(), name='group'),
    path('groups/<int:pk>/edit/', views.GroupUpdateView.as_view(), name='group_edit'),
    path('groups/<int:pk>/delete/', views.GroupDeleteView.as_view(), name='group_delete'),

    path('tests/', views.TestListView.as_view(), name='tests'),
    path('tests/add/', views.TestCreateView.as_view(), name='test_add'),
    path('tests/<int:pk>/', views.TestView.as_view(), name='test'),
    path('tests/<int:pk>/edit/', views.TestUpdateView.as_view(), name='test_edit'),
    path('tests/<int:pk>/delete/', views.TestDeleteView.as_view(), name='test_delete'),
    path('tests/<int:pk>/take/', views.test_take, name='test_take'),
    path('tests/<int:pk>/questions/', views.questions, name='questions'),
    path('tests/<int:pk>/questions/add/', views.question_add, name='question_add'),

    path('view_notification/<int:pk>/', views.view_notification, name='view_notification'),

    path('forbidden/', error_views.e403_handle, name='forbidden'),
    path('forbidden/<str:user_type>/', error_views.forbidden_user_view, name='forbidden_user'),
]

create_models_urls = [
    path('create_all_models/', create_models_view.create_all_models, name='create_all_models'),
    path('create_teachers/', create_models_view.create_teachers, name='create_teachers'),
    path('create_students/', create_models_view.create_students, name='create_students'),
    path('create_groups/', create_models_view.create_groups, name='create_groups'),
    path('create_problems/', create_models_view.create_problems, name='create_problems'),
    path('create_lectures/', create_models_view.create_lectures, name='create_lectures'),
]

urlpatterns += create_models_urls
