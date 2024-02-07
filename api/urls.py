from rest_framework import routers

from api.views import (TeacherViewSet, GroupViewSet, StudentViewSet, ArticleViewSet, ProblemViewSet, LectureViewSet,
                       AttachmentViewSet, TestFileViewSet, CommentViewSet, SolutionViewSet)


router = routers.DefaultRouter()

router.register('teachers', TeacherViewSet, 'api_teachers')
router.register('groups', GroupViewSet, 'api_groups')
router.register('students', StudentViewSet, 'api_students')
router.register('articles', ArticleViewSet, 'api_articles')
router.register('problems', ProblemViewSet, 'api_problems')
router.register('lectures', LectureViewSet, 'api_lectures')
router.register('attachments', AttachmentViewSet, 'api_attachments')
router.register('testfiles', TestFileViewSet, 'api_testfiles')
router.register('comments', CommentViewSet, 'api_comments')
router.register('solutions', SolutionViewSet, 'api_solutions')


urlpatterns = router.urls
