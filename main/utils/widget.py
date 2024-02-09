from django.forms import DateTimeInput


class TimePicker(DateTimeInput):
    # template_name = 'TimePicker.html'

    def get_context(self, name, value, attrs):


        datetimepicker_id = 'id_{name}'.format(name=name)
        print(datetimepicker_id)
        if attrs is None:
            attrs = dict()
        attrs['data-target'] = '#{id}'.format(id=datetimepicker_id)
        attrs['class'] = 'form-control datetimeinput datetimepicker-input pretty-input'

        context = super().get_context(name, value, attrs)
        context['widget']['datetimepicker_id'] = datetimepicker_id

        return context
