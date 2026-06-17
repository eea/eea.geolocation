"""Integration tests for eea.geolocation

Tests for view classes and installation.
"""

import unittest

from plone.app.testing import TEST_USER_ID, setRoles

from eea.geolocation.tests.base import FUNCTIONAL_TESTING


class TestGeolocationSetup(unittest.TestCase):
    """Test eea.geolocation installation"""

    layer = FUNCTIONAL_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def test_product_installed(self):
        """Test that eea.geolocation is installed"""
        from Products.CMFPlone.utils import get_installer

        installer = get_installer(self.portal, self.layer["request"])
        self.assertTrue(installer.is_product_installed("eea.geolocation"))

    def test_portal_exists(self):
        """Test that portal is set up"""
        self.assertIsNotNone(self.portal)

    def test_sandbox_folder_exists(self):
        """Test that sandbox folder was created"""
        self.assertIn("sandbox", self.portal.objectIds())


class TestGeolocationModuleImport(unittest.TestCase):
    """Test eea.geolocation module imports"""

    def test_get_class_importable(self):
        """Test that Get view class can be imported"""
        from eea.geolocation.restapi.get import Get

        self.assertIsNotNone(Get)

    def test_vocabularies_class_importable(self):
        """Test that GetVocabularies class can be imported"""
        from eea.geolocation.restapi.get import GetVocabularies

        self.assertIsNotNone(GetVocabularies)

    def test_geolocation_settings_importable(self):
        """Test that IGeolocationClientSettings can be imported"""
        from eea.geolocation.interfaces import IGeolocationClientSettings

        self.assertIsNotNone(IGeolocationClientSettings)


class TestEEA40Upgrade(unittest.TestCase):
    """Test the EEA40 geotags taxonomy upgrade step (evolve30)"""

    layer = FUNCTIONAL_TESTING

    TAXONOMY_NAME = "collective.taxonomy.eeageolocationgeotagstaxonomy"

    def setUp(self):
        self.portal = self.layer["portal"]
        setRoles(self.portal, TEST_USER_ID, ["Manager"])

    def _eea40_entries(self):
        """Return {path: value} for all geotags entries under the EEA40 group.

        The EEA40 group is installed by the default profile (updated VDEX),
        so it is present even before the upgrade step runs.
        """
        from collective.taxonomy import PATH_SEPARATOR
        from collective.taxonomy.interfaces import ITaxonomy
        from zope.component import queryUtility

        taxonomy = queryUtility(ITaxonomy, name=self.TAXONOMY_NAME)
        self.assertIsNotNone(taxonomy, "geotags taxonomy is not registered")

        group = PATH_SEPARATOR + "EEA40"
        prefix = group + PATH_SEPARATOR
        return {
            path: value
            for path, value in taxonomy.data["en"].items()
            if path == group or path.startswith(prefix)
        }

    def _country_paths(self, entries):
        """Country nodes are direct children of EEA40 (depth 2)."""
        from collective.taxonomy import PATH_SEPARATOR

        return [path for path in entries if len(path.split(PATH_SEPARATOR)) == 3]

    def test_eea40_present_from_profile(self):
        """EEA40 group, its 40 countries and sample members are installed"""
        from collective.taxonomy import PATH_SEPARATOR

        entries = self._eea40_entries()
        self.assertIn(PATH_SEPARATOR + "EEA40", entries)

        country_paths = self._country_paths(entries)
        self.assertEqual(len(country_paths), 40)

        sep = PATH_SEPARATOR
        for country in ("Ukraine", "Moldova", "Cyprus"):
            self.assertIn(sep + "EEA40" + sep + country, entries)

    def test_upgrade_is_idempotent(self):
        """Re-running the upgrade keeps EEA40 entries identical (no divergence)"""
        from eea.geolocation.upgrades.evolve30 import add_eea40_taxonomy

        before = self._eea40_entries()
        self.assertTrue(before)

        add_eea40_taxonomy(self.portal["portal_setup"])

        after = self._eea40_entries()
        self.assertEqual(before, after)


if __name__ == "__main__":
    unittest.main()
