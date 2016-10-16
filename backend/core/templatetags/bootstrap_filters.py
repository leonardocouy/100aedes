from django import template

register = template.Library()


@register.filter(name='bootstrap_input')
def bootstrap_input(value, arg):
    return value.as_widget(attrs={'class': 'form-control', 'placeholder': arg})

