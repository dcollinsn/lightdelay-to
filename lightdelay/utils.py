import re
import urllib.parse
from astroquery.mpc import MPC
from astroquery.exceptions import InvalidQueryError
from astropy import units as u
from astropy.coordinates import get_body
from astropy.coordinates import EarthLocation
from astropy.coordinates import SkyCoord
from astropy.coordinates import GCRS, Angle
from astropy.coordinates import errors
from astropy.time import Time
from django.utils.dateparse import parse_datetime


class LocationNotResolved(Exception):
    pass


class QueryArgNotResolved(Exception):
    pass


def get_location(query, time):
    query = query.replace('_', ' ')

    if query.lower() == "the moon" or query.lower == "luna":
        query = "moon"

    try:
        body = get_body(query, time)
        if query.lower() == "moon":
            query = "The Moon"
        return query.title(), body
    except KeyError:
        pass

    # Asteroid using designation
    try:
        number = ''
        name = query
        res = re.match(r'(\d+)\s+(.+)', query)
        if res:
            number = res.group(1)
            name = res.group(2)

        if number:
            asteroid_data = MPC.query_object("asteroid", number=number, name=name)
        else:
            asteroid_data = MPC.query_object("asteroid", name=name)

        if asteroid_data:
            asteroid_desig = "%d %s" % (
                asteroid_data[0]['number'],
                asteroid_data[0]['name'],
            )
            ephemeris = MPC.get_ephemeris(asteroid_desig, start=time, number=1)
            ephem_object = GCRS(
                ra=Angle(ephemeris[0]['RA'], unit=u.deg),
                dec=Angle(ephemeris[0]['Dec'], unit=u.deg),
                distance=u.Quantity(ephemeris[0]['Delta'], unit=u.AU),
                obstime=time,
            )
            return asteroid_desig, SkyCoord(ephem_object)
    except InvalidQueryError:
        pass

    # Asteroid by name
    try:
        asteroid_data = MPC.query_object("asteroid", designation=query)
        if asteroid_data:
            asteroid_desig = asteroid_data[0]['designation']
            ephemeris = MPC.get_ephemeris(asteroid_desig, start=time, number=1)
            ephem_object = GCRS(
                ra=Angle(ephemeris[0]['RA'], unit=u.deg),
                dec=Angle(ephemeris[0]['Dec'], unit=u.deg),
                distance=u.Quantity(ephemeris[0]['Delta'], unit=u.AU),
                obstime=time,
            )
            return asteroid_desig, SkyCoord(ephem_object)
    except InvalidQueryError:
        pass

    # Comet or MPC object using designation
    try:
        name = query
        res = re.match(r'(\d*P|C)\s+(.+)', query)
        if res:
            name = "%s/%s" % (
                res.group(1),
                res.group(2),
            )

        ephemeris = MPC.get_ephemeris(name, start=time, number=1)
        ephem_object = GCRS(
            ra=Angle(ephemeris[0]['RA'], unit=u.deg),
            dec=Angle(ephemeris[0]['Dec'], unit=u.deg),
            distance=u.Quantity(ephemeris[0]['Delta'], unit=u.AU),
            obstime=time,
        )
        return name, SkyCoord(ephem_object)
    except InvalidQueryError:
        pass

#    This section doesn't belong here at all. This section should be in a
#    separate function for earth locations, because earth locations and
#    nonterrestrial objects need to be handled differently.
#
#    try:
#        earth_site = EarthLocation.of_site(query)
#        earth_site = SkyCoord(earth_site.get_gcrs(time))
#        return query, earth_site
#    except errors.UnknownSiteException:
#        pass

    raise LocationNotResolved(query, time)


def calculate_distance(loc1, loc2):
    distance = loc1.separation_3d(loc2)
    return distance


def parse_queryarg(query):
    try:
        body = get_location(query, Time.now())
        return body
    except LocationNotResolved:
        try:
            time = parse_datetime(query)
            if time:
                return time
            else:
                raise QueryArgNotResolved(query)
        except ValueError:
            raise QueryArgNotResolved(query)


def encode_url_param(value):
    # Clean up space characters
    value = value.replace(' ', '_')
    value = value.replace('%20', '_')
    # Clean up slash characters
    value = value.replace('/', '_')
    value = value.replace('%2F', '_')
    return value
