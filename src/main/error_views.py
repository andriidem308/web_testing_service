from django.shortcuts import render


def forbidden_user_view(request, user_type):
    next_page = request.GET.get('next')
    context = {
        'user_type': user_type,
        'next_page': next_page
    }
    response = render(request, 'errors/forbidden_user.html', context=context)
    response.status_code = 403
    return response


def e403_handle(request, exception):
    response = render(request, 'errors/403.html')
    response.status_code = 403
    return response


def e404_handle(request, exception):
    response = render(request, 'errors/404.html')
    response.status_code = 404
    return response
