""" RestAPI enpoint @geolocation GET
"""
from eea.geolocation.interfaces import IGeolocationClientSettings
from plone import api
from plone.restapi.services import Service
from zope.interface import implementer
from zope.publisher.interfaces import IPublishTraverse


@implementer(IPublishTraverse)
class Get(Service):
    """GET"""

    def reply(self):
        """Reply"""
        return {
            "google": {
                "password": api.portal.get_registry_record(
                    "maps_api_key",
                    interface=IGeolocationClientSettings, default=""
                ),
            },
            "geonames": {
                "password": api.portal.get_registry_record(
                    "geonames_key",
                    interface=IGeolocationClientSettings, default=""
                ),
            },
        }
