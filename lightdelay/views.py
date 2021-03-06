import pytz
from dateutil import parser
from astropy.time import Time
from django.shortcuts import render, redirect
from django.utils import timezone

from lightdelay.utils import (get_location,
                              encode_url_param,
                              calculate_distance,
                              LocationNotResolved)


def lightdelay_locationerror(request, e):
    return render(
        request,
        'lightdelay/locationerror.html',
        {'e': e},
    )


def lightdelay_homepage(request, time):
    # Homepage.

    # Astropy time for calculations
    astrotime = Time(time)

    _, earth = get_location('earth', astrotime)
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
        try:
            _, location = get_location(body[0], astrotime)
        except LocationNotResolved as e:
            return lightdelay_locationerror(request, e)
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
    _, earth = get_location('earth', astrotime)
    try:
        body_name, body = get_location(query, astrotime)
    except LocationNotResolved as e:
        return lightdelay_locationerror(request, e)
    distance = calculate_distance(earth, body)

    context = {
        'time': time,
        'query': query,
        'body_name': body_name,
        'earth': earth,
        'body': body,
        'distance': distance,
    }

    return render(
        request,
        'lightdelay/1arg.html',
        context,
    )


def lightdelay_2body(request, query1, query2, time):
    # Calculate delay to a specific body.
    # TODO: Warn if closer than ~0.1AU, need to get earthloc
    # TODO: Error handling - can't parse location

    astrotime = Time(time)
    try:
        body1_name, body1 = get_location(query1, astrotime)
        body2_name, body2 = get_location(query2, astrotime)
    except LocationNotResolved as e:
        return lightdelay_locationerror(request, e)
    distance = calculate_distance(body1, body2)

    context = {
        'time': time,
        'query1': query1,
        'body1_name': body1_name,
        'body1': body1,
        'query2': query2,
        'body2_name': body2_name,
        'body2': body2,
        'distance': distance,
    }

    return render(
        request,
        'lightdelay/2arg.html',
        context,
    )


def lightdelay_search(request):
    args = []
    if request.GET.get('body1'):
        args.append(encode_url_param(request.GET.get('body1')))
    if request.GET.get('body2'):
        args.append(encode_url_param(request.GET.get('body2')))
    if request.GET.get('time'):
        args.append(encode_url_param(request.GET.get('time')))

    if len(args) == 3:
        return redirect('lightdelay_3arg', *args)
    if len(args) == 2:
        return redirect('lightdelay_2arg', *args)
    if len(args) == 1:
        return redirect('lightdelay_1arg', *args)
    if len(args) == 0:
        return redirect('lightdelay_0arg', *args)



    # See if we got a time
    try:
        time = parser.parse(request.GET.get('time'))
    except (TypeError, ValueError):
        time = timezone.now()

    if request.GET.get('body2'):
        # TODO: Return Redirect?
        return lightdelay_2body(request, request.GET.get('body1'), request.GET.get('body2'), time)

    if request.GET.get('body1'):
        # TODO: Return Redirect?
        return lightdelay_1body(request, request.GET.get('body1'), time)

    return lightdelay_homepage(request, time)


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
    args = [query2, query1]
    time = None
    for arg in args:
        try:
            time = parser.parse(arg)
            if time.tzinfo is None:
                time = time.replace(tzinfo=pytz.utc)
            args.remove(arg)
            break
        except ValueError:
            pass

    if time is None:
        time = timezone.now()

    if len(args) == 2:
        return lightdelay_2body(request, args[1], args[0], time)
    if len(args) == 1:
        return lightdelay_1body(request, args[0], time)

    return


def lightdelay_3arg(request, query1, query2, query3):
    args = [query3, query2, query1]
    time = None
    for arg in args:
        try:
            time = parser.parse(arg)
            if time.tzinfo is None:
                time = time.replace(tzinfo=pytz.utc)
            args.remove(arg)
            break
        except ValueError:
            pass

    if time is None:
        time = timezone.now()

    return lightdelay_2body(request, args[1], args[0], time)
