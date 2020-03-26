# -*- coding: utf-8 -*-
from bda.plone.productshop.tests import ProductShop_INTEGRATION_TESTING
from bda.plone.productshop.tests import set_browserlayer

import unittest


class TestProductShop(unittest.TestCase):
    layer = ProductShop_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer["portal"]
        self.request = self.layer["request"]
        set_browserlayer(self.request)

    def test_foo(self):
        self.assertEqual(1, 1)
