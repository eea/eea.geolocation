"""Base test cases"""

from plone.testing import z2
from plone.app.testing import TEST_USER_ID
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import setRoles


class EEAFixture(PloneSandboxLayer):
    """EEA Testing Policy"""

    def setUpZope(self, app, configurationContext):
        """Setup Zope"""
        import eea.geolocation
        import collective.taxonomy

        self.loadZCML(package=collective.taxonomy)
        self.loadZCML(package=eea.geolocation)
        z2.installProduct(app, "collective.taxonomy")
        z2.installProduct(app, "eea.geolocation")

    def setUpPloneSite(self, portal):
        """Setup Plone"""
        applyProfile(portal, "collective.taxonomy:default")
        applyProfile(portal, "eea.geolocation:default")

        # Default workflow
        wftool = portal["portal_workflow"]
        wftool.setDefaultChain("simple_publication_workflow")

        # Login as manager
        setRoles(portal, TEST_USER_ID, ["Manager"])

        # Add default Plone content
        applyProfile(portal, "plone.app.contenttypes:plone-content")

        # Create testing environment
        portal.invokeFactory("Folder", "sandbox", title="Sandbox")

    def tearDownZope(self, app):
        """Uninstall Zope"""
        z2.uninstallProduct(app, "eea.geolocation")


EEAFIXTURE = EEAFixture()
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(EEAFIXTURE,), name="EEAgeolocation:Functional"
)
