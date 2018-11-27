from astroquery.mpc import MPC
from astroquery.exceptions import InvalidQueryError
from astropy import units as u
from astropy.coordinates import get_body
from astropy.coordinates import EarthLocation
from astropy.coordinates import SkyCoord
from astropy.coordinates import GCRS, Angle
from astropy.coordinates import errors
#from astropy.coordinates import solar_system_ephemeris
from astropy.time import Time
#import ephem
from django.utils.dateparse import parse_datetime

#from lightdelay.models import MinorPlanet

class LocationNotResolved(Exception):
    pass


class QueryArgNotResolved(Exception):
    pass


def get_location(query, time):
#    solar_system_ephemeris.set('de432s')
    try:
        body = get_body(query, time)
        return body
    except KeyError:
        pass

    try:
        ephemeris = MPC.get_ephemeris(query, start=time, number=1)
        ephem_object = GCRS(
            ra=Angle(ephemeris[0]['RA'], unit=u.deg),
            dec=Angle(ephemeris[0]['Dec'], unit=u.deg),
            distance=u.Quantity(ephemeris[0]['Delta'], unit=u.AU),
        )
        return SkyCoord(ephem_object)
    except InvalidQueryError:
        pass

#    try:
#        minor_planet = MinorPlanet.objects.filter(
#            name__icontains=query,
#        )[0]
#        ephem_object = ephem.readdb(minor_planet.xephem)
#        ephem_object.compute(time.datetime.date().strftime('%m/%d/%Y'))
#    except MinorPlanet.DoesNotExist:
#        pass

    try:
        earth_site = EarthLocation.of_site(query)
        earth_site = SkyCoord(earth_site.get_gcrs(time))
        return earth_site
    except errors.UnknownSiteException:
        pass

#    Disabled - too many false positives
#    try:
#        earth_site = EarthLocation.of_address(query)
#        earth_site = SkyCoord(earth_site.get_gcrs(time))
#        return earth_site
#    except NameResolveError:
#        pass

    raise LocationNotResolved(query)


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
