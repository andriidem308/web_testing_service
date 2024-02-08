from ninja import NinjaAPI
from main.models import Teacher, Group, Student, Article, Problem, Lecture, Attachment, TestFile, Comment, Solution


api = NinjaAPI()

@api.get("/teachers")
def get_teachers(request):
    teachers = Teacher.objects.all().values()
    return list(teachers)


@api.get("/teachers/{teacher_id}")
def get_teacher(request, teacher_id: int):
    teacher = Teacher.objects.get(id=teacher_id)
    return teacher


@api.get("/groups")
def get_groups(request):
    groups = Group.objects.all().values()
    return list(groups)


@api.get("/groups/{group_id}")
def get_group(request, group_id: int):
    group = Group.objects.get(id=group_id)
    return group


@api.get("/students")
def get_students(request):
    students = Student.objects.all().values()
    return list(students)


@api.get("/students/{student_id}")
def get_student(request, student_id: int):
    student = Student.objects.get(id=student_id)
    return student


@api.get("/articles")
def get_articles(request):
    articles = Article.objects.all().values()
    return list(articles)


@api.get("/articles/{article_id}")
def get_article(request, article_id: int):
    article = Article.objects.get(id=article_id)
    return article


@api.get("/problems")
def get_problems(request):
    problems = Problem.objects.all().values()
    return list(problems)


@api.get("/problems/{problem_id}")
def get_problem(request, problem_id: int):
    problem = Problem.objects.get(id=problem_id)
    return problem


@api.get("/lectures")
def get_lectures(request):
    lectures = Lecture.objects.all().values()
    return list(lectures)


@api.get("/lectures/{lecture_id}")
def get_lecture(request, lecture_id: int):
    lecture = Lecture.objects.get(id=lecture_id)
    return lecture


@api.get("/attachments")
def get_attachments(request):
    attachments = Attachment.objects.all().values()
    return list(attachments)


@api.get("/attachments/{attachment_id}")
def get_attachment(request, attachment_id: int):
    attachment = Attachment.objects.get(id=attachment_id)
    return attachment


@api.get("/test-files")
def get_test_files(request):
    test_files = TestFile.objects.all().values()
    return list(test_files)


@api.get("/test-files/{test_file_id}")
def get_test_file(request, test_file_id: int):
    test_file = TestFile.objects.get(id=test_file_id)
    return test_file


@api.get("/comments")
def get_comments(request):
    comments = Comment.objects.all().values()
    return list(comments)


@api.get("/comments/{comment_id}")
def get_comment(request, comment_id: int):
    comment = Comment.objects.get(id=comment_id)
    return comment


@api.get("/solutions")
def get_solutions(request):
    solutions = Solution.objects.all().values()
    return list(solutions)


@api.get("/solutions/{solution_id}")
def get_solution(request, solution_id: int):
    solution = Solution.objects.get(id=solution_id)
    return solution