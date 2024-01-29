from django.shortcuts import render


def problem_list(request):
    return render(request, 'base.html')


def lectures(request):
    return render(request, 'students/lectures.html')

def lecture(request):
    return render(request, 'students/lecture.html')

def problems(request):
    return render(request, 'students/problems.html')

def problem(request):
    return render(request, 'students/problem.html')

