from datetime import timedelta
from django import template

register = template.Library()


@register.filter
def convert_to(value, unit):
    return value.to(unit).value


@register.filter
def distance_to_delay(value):
    lightyears = value.to('lyr').value
    lightseconds = lightyears * 31557600  # SI Definition
    delay = timedelta(seconds=lightseconds)
    days = delay.days
    hours = delay.seconds // 3600
    minutes = delay.seconds % 3600 // 60
    seconds = delay.seconds % 60 + delay.microseconds / 1000000

    delay_str = "%d hours, %d minutes, %.2f seconds" % (
        hours, minutes, seconds,
    )
    if days:
        delay_str = "%d days, %s" % (
            days, delay_str,
        )

    return delay_str


@register.filter
def pretty_query(value):
    value = value.replace('_', ' ')
    value = value.title()
    return value
