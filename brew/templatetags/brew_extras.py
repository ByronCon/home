from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.simple_tag
def active_page(request, view_name):
    from django.core.urlresolvers import resolve, Resolver404
    if not request:
        return ""
    try:
        return "active" if resolve(request.path_info).url_name == view_name else ""
        #return "active"
    except Resolver404:
        return ""


@register.filter
def tourl(value): # Only one argument.
    """Converts a string into all lowercase"""
    from django.core.urlresolvers import resolve, Resolver404
    return resolve(value).url_name


@register.filter
@stringfilter
def lower(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.lower()

@register.filter
@stringfilter
def upper(value): # Only one argument.
    """Converts a string into all lowercase"""
    return value.upper()


