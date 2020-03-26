# -*- coding: utf-8 -*-
from bda.plone.productshop.interfaces import IProductShopExtensionLayer
from bda.plone.shop.tests import Shop_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from zope.interface import alsoProvides


def set_browserlayer(request):
    """Set the BrowserLayer for the request.

    We have to set the browserlayer manually, since importing the profile alone
    doesn't do it in tests.
    """
    alsoProvides(request, IProductShopExtensionLayer)


class ProductShopLayer(PloneSandboxLayer):
    defaultBases = (Shop_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        import bda.plone.productshop

        self.loadZCML(package=bda.plone.productshop, context=configurationContext)

    def setUpPloneSite(self, portal):
        self.applyProfile(portal, "bda.plone.productshop:default")

    def tearDownZope(self, app):
        pass


ProductShop_FIXTURE = ProductShopLayer()
ProductShop_INTEGRATION_TESTING = IntegrationTesting(
    bases=(ProductShop_FIXTURE,), name="ProductShop:Integration"
)
