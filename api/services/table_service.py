from django.db.models import Q


def filter_students(request, student_list):
    search_value = request.GET.get('search[value]', '').strip()

    form_order_column = request.GET.get('order[0][column]')
    form_order_dir = request.GET.get('order[0][dir]')
    order = False if form_order_dir == 'desc' else True

    columns = {
        '0': 'user__first_name',
        '1': 'user__last_name',
        '2': 'group',
    }

    order_column = columns[form_order_column] if order else f'-{columns[form_order_column]}'
    filtered_students = student_list.order_by(order_column)

    selected_students = filtered_students.filter(
        Q(user__first_name__contains=search_value) | Q(user__last_name__contains=search_value))

    return selected_students


def highlight_search(text, search_value):
    start_pos = text.lower().find(search_value.lower())

    if start_pos != -1:
        end_pos = start_pos + len(search_value)
        highlighted_text = (
            f"{text[:start_pos]}<mark>{text[start_pos:end_pos]}</mark>{text[end_pos:]}"
        )
        return highlighted_text
    else:
        return text
