from django import template


register = template.Library()


@register.filter(name='make_list')
def make_list(number):
    return range(1,number+1)
