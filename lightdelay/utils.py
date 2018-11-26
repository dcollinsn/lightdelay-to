from astropy.coordinates import get_body
from astropy.coordinates import EarthLocation
from astropy.coordinates import SkyCoord
from astropy.coordinates import errors
from astropy.coordinates.name_resolve import NameResolveError


def get_location(query, time):
    try:
        body = get_body(query, time)
        return body
    except KeyError:
        pass

    try:
        earth_site = EarthLocation.of_site(query)
        earth_site = SkyCoord(earth_site.get_gcrs(time))
        return earth_site
    except errors.UnknownSiteException:
        pass

    try:
        earth_site = EarthLocation.of_address(query)
        earth_site = SkyCoord(earth_site.get_gcrs(time))
        return earth_site
    except NameResolveError:
        pass


def calculate_distance(loc1, loc2):
    distance = loc1.separation_3d(loc2)
    return distance
