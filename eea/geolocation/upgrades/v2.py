# -*- coding: utf-8 -*-

import logging


# from base import reload_gs_profile
# from plone import api


def upgrade(setup_tool=None):
    """ """
    logger = logging.getLogger("eea.geolocation")
    logger.info("Running upgrade (Python): Rename controlpanel id")
