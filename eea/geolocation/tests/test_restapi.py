"""Integration tests for eea.geolocation

Tests for view classes and installation.
"""

import unittest
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID
from transaction import commit
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


if __name__ == "__main__":
    unittest.main()
