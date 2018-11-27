import pytz
from dateutil import parser
from astropy.time import Time
from django.shortcuts import render
from django.utils import timezone

from lightdelay.utils import (get_location,
                              calculate_distance)


def lightdelay_homepage(request, time):
    # Homepage.

    # Astropy time for calculations
    astrotime = Time(time)

    earth = get_location('earth', astrotime)
    bodies = (
        ('mars', 'Mars'),
        ('moon', 'The Moon'),
        ('venus', 'Venus'),
        ('mercury', 'Mercury'),
        ('jupiter', 'Jupiter'),
        ('saturn', 'Saturn'),
        ('uranus', 'Uranus'),
        ('neptune', 'Neptune'),
    )
    body_data = []
    for body in bodies:
        location = get_location(body[0], astrotime)
        distance = calculate_distance(earth, location)
        body_data.append({
            'slug': body[0],
            'name': body[1],
            'location': location,
            'distance': distance,
        })

    context = {
        'time': time,
        'body_data': body_data,
    }

    return render(
        request,
        'lightdelay/homepage.html',
        context,
    )


def lightdelay_1body(request, query, time):
    # Calculate delay to a specific body.
    # TODO: Warn if closer than ~0.1AU, need to get earthloc
    # TODO: Error handling - can't parse location

    astrotime = Time(time)
    earth = get_location('earth', astrotime)
    body = get_location(query, astrotime)
    distance = calculate_distance(earth, body)

    context = {
        'time': time,
        'query': query,
        'body': body,
        'distance': distance,
    }

    return render(
        request,
        'lightdelay/1arg.html',
        context,
    )


def lightdelay_0arg(request):
    # No arguments provided, so we'll use the current time

    time = timezone.now()
    return lightdelay_homepage(request, time)


def lightdelay_1arg(request, query):
    # First, look for a datetime.
    try:
        time = parser.parse(query)
        if time.tzinfo is None:
            time = time.replace(tzinfo=pytz.utc)
        return lightdelay_homepage(request, time)
    except ValueError:
        pass

    # Well then, guess we're using timezone.now
    time = timezone.now()
    return lightdelay_1body(request, query, time)


def lightdelay_2arg(request, query1, query2):
    return


def lightdelay_3arg(request, query1, query2, query3):
    return
