from django import template

register = template.Library()


def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)


register.filter('split', split)
