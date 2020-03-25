# -*- coding: utf-8 -*-
from bda.plone.discount.interfaces import IDiscountSettingsEnabled
from bda.plone.shop.interfaces import IShopSettingsProvider
from collective.instancebehavior import IInstanceBehaviorAssignableContent
from plone.namedfile.interfaces import IImageScaleTraversable
from plone.supermodel import model
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.interface import Interface
from zope.interface import provider


_ = MessageFactory('bda.plone.productshop')


class IProductShopExtensionLayer(Interface):
    """Product shop specific browser layer.
    """


##############################################################################
# content markers
##############################################################################

class IProduct(Interface, IImageScaleTraversable):
    """Marker interface for product content.
    """


class IProductGroup(IProduct, IDiscountSettingsEnabled):
    """Marker interface for product group content.
    """


class IVariant(IProduct, IInstanceBehaviorAssignableContent):
    """Marker interface for variant content.
    """


class IVariantAspect(Interface):
    """Aspect of a variant.
    """


###############################################################################
# productshop relates shop settings
###############################################################################

@provider(IShopSettingsProvider)
class IProductShopSettings(model.Schema):
    """Productshop settings.
    """
    model.fieldset(
        'products',
        label=_(u'products', default=u'Products'),
        fields=['product_tiles_view_columns',
                'product_tiles_view_image_scale'])

    product_tiles_view_columns = schema.Int(
        title=_(u'product_tiles_view_columns_title',
                default=u'Product tiles view Columns'),
        description=_(
            u'product_tiles_view_columns_description',
            default=u'Number of columns shown in product tiles view'),
        required=False)

    product_tiles_view_image_scale = schema.Choice(
        title=_(u'product_tiles_view_image_scale_title',
                default=u'Product tiles image scale'),
        description=_(u'product_tiles_view_image_scale_description',
                      default=u'Image scale used for product tiles'),
        vocabulary='plone.app.vocabularies.ImagesScales',
        required=False)
