"""Upgrade to 3.0 - Add EEA40 taxonomy group to geotags"""

import logging
import os

from collective.taxonomy.exportimport import TaxonomyImportExportAdapter
from collective.taxonomy.interfaces import ITaxonomy
from zope.component import queryUtility

logger = logging.getLogger("eea.geolocation")

# EEA40 = EEA38 + Ukraine + Moldova (40 member countries)
TAXONOMY_NAME = "collective.taxonomy.eeageolocationgeotagstaxonomy"
TAXONOMY_FILE = "eea.geolocation.geotags.taxonomy"


def add_eea40_taxonomy(context):
    """Add EEA40 (EEA38 + Ukraine + Moldova) to the geotags taxonomy.

    Re-imports the geotags VDEX profile with clear=False: existing terms
    update in place by path, the EEA40 group is appended. Reusing the
    profile XML (instead of a hardcoded list) keeps upgraded sites
    byte-identical to fresh installs.
    """
    site = context.aq_parent
    taxonomy = queryUtility(ITaxonomy, name=TAXONOMY_NAME)
    if taxonomy is None:
        logger.warning("Taxonomy %s not found, skipping EEA40 import", TAXONOMY_NAME)
        return

    base = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    path = os.path.join(base, "profiles", "plone5imports", TAXONOMY_FILE + ".xml")

    with open(path) as xmlfile:
        data = xmlfile.read().encode()

    TaxonomyImportExportAdapter(site).importDocument(taxonomy, data)
    logger.info("Re-imported %s; EEA40 group added", TAXONOMY_NAME)
