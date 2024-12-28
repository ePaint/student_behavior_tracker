from django import template


register = template.Library()


@register.filter
def dict_key(value, arg):
    """Return the value of a dictionary key."""
    return value[arg]
