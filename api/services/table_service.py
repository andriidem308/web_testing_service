from django.db.models import Q


def get_table_parameters(request):
    table_parameters = {
        'column': int(request.GET.get('order[0][column]'), 0),
        'reversed': request.GET.get('order[0][dir]') == 'desc',
        'search': request.GET.get('search[value]', '').strip(),
        'size': int(request.GET.get('length', 0)),
        'offset': int(request.GET.get('start', 0)),
    }
    return table_parameters


def filter_students(request, students_list):
    params = get_table_parameters(request)

    searched_students = students_list.filter(
        Q(user__first_name__contains=params['search']) | Q(user__last_name__contains=params['search']))

    order_column = params['column']
    columns = ('first_name', 'last_name', 'total_score', 'problems_solved', )
    order_column = columns[order_column]
    ordered_students = sorted(searched_students, key=lambda s: getattr(s, order_column), reverse=params['reversed'])

    return ordered_students


def select_students(request, students_list):
    params = get_table_parameters(request)
    selected_students = students_list[params['offset']:params['offset']+params['size']]
    return selected_students


def highlight_search(text, request):
    search_value = request.GET.get('search[value]', '').strip()
    start_pos = text.lower().find(search_value.lower())

    if start_pos != -1:
        end_pos = start_pos + len(search_value)
        highlighted_text = (
            f"{text[:start_pos]}<mark>{text[start_pos:end_pos]}</mark>{text[end_pos:]}"
        )
        return highlighted_text
    else:
        return text
