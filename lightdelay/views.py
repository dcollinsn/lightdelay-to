from astropy.time import Time
from django.shortcuts import render
from django.utils import timezone

from lightdelay.utils import get_location, calculate_distance


def lightdelay_0arg(request):
    # Homepage. Calculate delay to common options.

    # Aware time for display
    now = timezone.now()
    # Astropy time for calculations
    time = Time(now)

    earth = get_location('earth', time)
    bodies = (
        ('mars', 'Mars'),
        ('moon', 'The Moon'),
    )
    body_data = []
    for body in bodies:
        location = get_location(body[0], time)
        distance = calculate_distance(earth, location)
        body_data.append({
            'slug': body[0],
            'name': body[1],
            'location': location,
            'distance': distance,
        })

    context = {
        'time': now,
        'body_data': body_data,
    }

    return render(
        request,
        'lightdelay/homepage.html',
        context,
    )


def lightdelay_1arg(request, loc2):
    # Calculate delay to a specific body.
    # TODO: Warn if closer than ~0.1AU, need to get earthloc
    # TODO: Error handling - can't parse location

    time = Time.now()
    earth = get_location('earth', time)
    body2 = get_location(loc2, time)
    distance = calculate_distance(earth, body2)

    context = {
        'time': time,
        'body2': body2,
        'distance': distance,
    }

    return render(
        request,
        'lightdelay/1arg.html',
        context,
    )


def lightdelay_2arg(request, loc1, loc2):
    return


def lightdelay_3arg(request, loc1, loc2, date):
    return
