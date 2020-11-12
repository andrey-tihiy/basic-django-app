from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def frontend_host():
    host = settings.FRONTEND_HOST
    return host
