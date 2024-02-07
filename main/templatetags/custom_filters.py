from django import template

register = template.Library()


@register.filter
def add_class(field, css):
    classes = field.field.widget.attrs.get('class', '')
    classes += ' ' + css
    return field.as_widget(attrs={'class': classes.strip()})
