from django.urls import path
from rest_framework import routers

from api import views


router = routers.DefaultRouter()

router.register('teachers', views.TeacherViewSet, 'api_teachers')
router.register('groups', views.GroupViewSet, 'api_groups')
router.register('students', views.StudentViewSet, 'api_students')
router.register('articles', views.ArticleViewSet, 'api_articles')
router.register('problems', views.ProblemViewSet, 'api_problems')
router.register('lectures', views.LectureViewSet, 'api_lectures')
router.register('comments', views.CommentViewSet, 'api_comments')
router.register('solutions', views.SolutionViewSet, 'api_solutions')


urlpatterns = router.urls + [
    path('group_data/<int:pk>/', views.group_data, name='group_data'),
]
