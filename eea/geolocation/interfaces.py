"""Module where all interfaces, events and exceptions live."""
from zope.interface import Interface
from zope import schema
from zope.publisher.interfaces.browser import IDefaultBrowserLayer
from eea.geolocation import EEAMessageFactory as _


class IEeaGeolocationLayer(IDefaultBrowserLayer):
    """Marker interface that defines a browser layer."""


class IGeolocationClientSettings(Interface):
    """ Client settings for Geolocation
    """
    maps_api_key = schema.TextLine(
        title=_(u"Google Maps API key"),
        description=_(
            u'This will be used to render the Google Maps widget '
            u'for eea.geotags enabled location fields. '
            u'You can get one from '
            u'https://developers.google.com/maps/documentation/javascript/'
            u'get-api-key '
            u'Leave empty to use Open Street Map instead'
        ),
        required=False,
        default=u''
    )

    geonames_key = schema.TextLine(
        title=_(u"Geonames key"),
        description=_(u'http://www.geonames.org/'),
        required=False,
        default=u''
    )
