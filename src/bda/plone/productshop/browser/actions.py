# -*- coding: utf-8 -*-
from bda.plone.productshop.behaviors import IAngleBehavior
from bda.plone.productshop.behaviors import IColorBehavior
from bda.plone.productshop.behaviors import IDemandBehavior
from bda.plone.productshop.behaviors import IHeightBehavior
from bda.plone.productshop.behaviors import IIPCodeBehavior
from bda.plone.productshop.behaviors import ILengthBehavior
from bda.plone.productshop.behaviors import IMaterialBehavior
from bda.plone.productshop.behaviors import ISizeBehavior
from bda.plone.productshop.behaviors import IWeightBehavior
from bda.plone.productshop.behaviors import IWidthBehavior
from bda.plone.productshop.interfaces import IVariant
from collective.instancebehavior import disable_behaviors
from collective.instancebehavior import enable_behaviors
from Products.Five.browser import BrowserView
from zope.i18nmessageid import MessageFactory


_ = MessageFactory("bda.plone.productshop")


class VariantAspectAction(BrowserView):
    aspect_title = None
    aspect_behavior = None
    aspect_schema = None

    def enable_aspect(self):
        enable_behaviors(self.context, (self.aspect_behavior,), (self.aspect_schema,))
        self.context.plone_utils.addPortalMessage(
            _(
                u"enabled_aspect",
                default=u"Added ${aspect} to object.",
                mapping={"aspect": self.aspect_title},
            )
        )
        self.request.response.redirect(self.context.absolute_url())

    def disable_aspect(self):
        disable_behaviors(self.context, (self.aspect_behavior,), (self.aspect_schema,))
        self.context.plone_utils.addPortalMessage(
            _(
                u"disabled_aspect",
                default=u"Removed ${aspect} from object.",
                mapping={"aspect": self.aspect_title},
            )
        )
        self.request.response.redirect(self.context.absolute_url())

    def can_enable(self):
        return not self.aspect_schema.providedBy(self.context) and IVariant.providedBy(
            self.context
        )

    def can_disable(self):
        return self.aspect_schema.providedBy(self.context)


class ColorAction(VariantAspectAction):
    aspect_title = _(u"aspect_color", default=u"Color")
    aspect_behavior = "bda.plone.productshop.behaviors.IColorBehavior"
    aspect_schema = IColorBehavior


class WeightAction(VariantAspectAction):
    aspect_title = _(u"aspect_weight", default=u"Weight")
    aspect_behavior = "bda.plone.productshop.behaviors.IWeightBehavior"
    aspect_schema = IWeightBehavior


class SizeAction(VariantAspectAction):
    aspect_title = _(u"aspect_size", default=u"Size")
    aspect_behavior = "bda.plone.productshop.behaviors.ISizeBehavior"
    aspect_schema = ISizeBehavior


class DemandAction(VariantAspectAction):
    aspect_title = _(u"aspect_demand", default=u"Demand")
    aspect_behavior = "bda.plone.productshop.behaviors.IDemandBehavior"
    aspect_schema = IDemandBehavior


class LengthAction(VariantAspectAction):
    aspect_title = _(u"aspect_length", default=u"Length")
    aspect_behavior = "bda.plone.productshop.behaviors.ILengthBehavior"
    aspect_schema = ILengthBehavior


class WidthAction(VariantAspectAction):
    aspect_title = _(u"aspect_width", default=u"Width")
    aspect_behavior = "bda.plone.productshop.behaviors.IWidthBehavior"
    aspect_schema = IWidthBehavior


class HeightAction(VariantAspectAction):
    aspect_title = _(u"aspect_height", default=u"Height")
    aspect_behavior = "bda.plone.productshop.behaviors.IHeightBehavior"
    aspect_schema = IHeightBehavior


class IPCodeAction(VariantAspectAction):
    aspect_title = _(u"aspect_ip_code", default=u"IP Code")
    aspect_behavior = "bda.plone.productshop.behaviors.IIPCodeBehavior"
    aspect_schema = IIPCodeBehavior


class AngleAction(VariantAspectAction):
    aspect_title = _(u"aspect_angle", default=u"Angle")
    aspect_behavior = "bda.plone.productshop.behaviors.IAngleBehavior"
    aspect_schema = IAngleBehavior


class MaterialAction(VariantAspectAction):
    aspect_title = _(u"aspect_material", default=u"Material")
    aspect_behavior = "bda.plone.productshop.behaviors.IMaterialBehavior"
    aspect_schema = IMaterialBehavior
