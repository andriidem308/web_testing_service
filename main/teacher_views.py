from django.shortcuts import render


def problem_list(request):
    return render(request, 'base.html')

