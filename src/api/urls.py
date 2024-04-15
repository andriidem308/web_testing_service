from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api import views

router = routers.DefaultRouter()

router.register('teachers', views.TeacherViewSet, 'api_teachers')
router.register('groups', views.GroupViewSet, 'api_groups')
router.register('students', views.StudentViewSet, 'api_students')
router.register('articles', views.ArticleViewSet, 'api_articles')
router.register('problems', views.ProblemViewSet, 'api_problems')
router.register('lectures', views.LectureViewSet, 'api_lectures')
router.register('tests', views.TestViewSet, 'api_tests')
router.register('questions', views.QuestionViewSet, 'api_questions')
router.register('comments', views.CommentViewSet, 'api_comments')
router.register('notifications', views.NotificationViewSet, 'api_notifications')
router.register('solutions', views.SolutionViewSet, 'api_solutions')
router.register('test_solutions', views.TestSolutionViewSet, 'api_test_solutions')

urlpatterns = router.urls + [
    path('group_data/<int:pk>/', views.group_data, name='group_data'),
    path('test_solutions_data/<int:pk>/', views.test_solutions_data, name='test_solutions_data'),
    path('auth/', include('rest_framework.urls')),
    path('token', TokenObtainPairView.as_view()),
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]
