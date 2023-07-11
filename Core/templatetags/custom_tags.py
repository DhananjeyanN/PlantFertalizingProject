from django import template

register = template.Library()
@register.filter
def get_item(dictionary,key):
    keys = key.split('.')
    for key in keys:
        dictionary = dictionary.get(key)
    return dictionary.get(key)


