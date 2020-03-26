# -*- coding: utf-8 -*-
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition.interfaces import IAcquirer
from bda.plone.productshop.utils import available_variant_aspects
from bda.plone.productshop.utils import dotted_name
from collective.instancebehavior import enable_behaviors
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.interfaces import IDexterityFTI
from plone.dexterity.utils import getAdditionalSchemata
from z3c.form import form
from zope.component import createObject
from zope.component import getUtility


def get_default_variant_aspects(context):
    try:
        default_aspects = getattr(context, "default_variant_aspects")
    except AttributeError:
        return list()
    ret = list()
    for definition in available_variant_aspects():
        aspect_name = dotted_name(definition.interface)
        for default_name in default_aspects:
            if default_name == aspect_name:
                ret.append(definition.interface)
                break
    return ret


class VariantAddForm(DefaultAddForm):
    @property
    def additionalSchemata(self):
        for behavior in getAdditionalSchemata(portal_type=self.portal_type):
            yield behavior

        for behavior in get_default_variant_aspects(self.context):
            yield behavior

    def create(self, data):
        fti = getUtility(IDexterityFTI, name=self.portal_type)

        container = aq_inner(self.context)
        content = createObject(fti.factory)

        if hasattr(content, "_setPortalTypeName"):
            content._setPortalTypeName(fti.getId())

        if IAcquirer.providedBy(content):
            content = content.__of__(container)

        for behavior in get_default_variant_aspects(self.context):
            name = dotted_name(behavior)
            enable_behaviors(content, (name,), (behavior,), reindex=False)

        form.applyChanges(self, content, data)
        for group in self.groups:
            form.applyChanges(group, content, data)

        return aq_base(content)


class VariantAddView(DefaultAddView):
    form = VariantAddForm
