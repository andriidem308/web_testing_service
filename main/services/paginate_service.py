from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def create_paginator(request, items: list, limit: int = 12):
    paginator = Paginator(items, limit)
    page_number = request.GET.get('page')

    try:
        result = paginator.page(page_number)
    except PageNotAnInteger:
        result = paginator.page(1)
    except EmptyPage:
        result = paginator.page(paginator.num_pages)

    return result
