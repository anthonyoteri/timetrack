from datetime import timedelta

from django import template

register = template.Library()


@register.filter
def format_timedelta(value):

    if not isinstance(value, timedelta):
        return value

    hours, remainder = divmod(int(value.total_seconds()), 3600)
    minutes, _ = divmod(remainder, 60)

    return "%02d:%02d" % (hours, minutes)
