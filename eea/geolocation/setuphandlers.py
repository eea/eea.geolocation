""" Custom setup
"""
import os
from Products.CMFPlone.interfaces import INonInstallable
from zope.interface import implementer
from collective.taxonomy.factory import registerTaxonomy
from collective.taxonomy.exportimport import TaxonomyImportExportAdapter, parseConfigFile


try:
    # Plone 4
    from Products.CMFPlone.interfaces import IFactoryTool
    IS_PLONE_4 = True
except ImportError:
    IS_PLONE_4 = False


TAXONOMIES = {
    'eea.geolocation.biotags.taxonomy': 'Biogeographical Regions',
    'eea.geolocation.geotags.taxonomy': 'EEA Geolocation Geotags',
    'eea.geolocation.countries_mapping.taxonomy': 'EEA Custom Country Names Mappings',
}


@implementer(INonInstallable)
class HiddenProfiles(object):
    """ Hidden profiles
    """

    def getNonInstallableProfiles(self):
        """ Hide uninstall profile from site-creation and quickinstaller.
        """
        return [
            'eea.geolocation:uninstall',
        ]


def post_install(context):
    """ Post install script
    """
    site = context.aq_parent
    if IS_PLONE_4:
        language = 'en'
        directory = '/profiles/plone4imports/'
    else:
        language = 'en-us'
        directory = '/profiles/plone5imports/'

    for name, title in TAXONOMIES.items():
        taxonomy = registerTaxonomy(site, name, title, language, 'Created at install')

        path = os.path.dirname(os.path.realpath(__file__))
        path += directory + name + '.xml'

        # import pdb; pdb.set_trace()
        with open(path) as file:
            data = file.read().encode()
            import_adapter = TaxonomyImportExportAdapter(site)
            import_adapter.importDocument(taxonomy, data)



def uninstall(context):
    """ Uninstall script
    """
    # Do something at the end of the uninstallation of this package.

# 1.remove added taxonomies
