# -*- coding: utf-8 -*-
from AccessControl import getSecurityManager
from Acquisition import aq_inner
from Acquisition import aq_parent
from bda.plone.ajax.batch import Batch
from bda.plone.cart.utils import get_object_by_uid
from bda.plone.productshop.behaviors import IProductTilesViewSettingsBehavior
from bda.plone.productshop.interfaces import IProduct
from bda.plone.productshop.interfaces import IProductGroup
from bda.plone.productshop.interfaces import IProductShopSettings
from bda.plone.productshop.interfaces import IVariant
from bda.plone.productshop.utils import available_variant_aspects
from bda.plone.productshop.utils import request_property
from bda.plone.shop import permissions
from bda.plone.orders.interfaces import IBuyable
from plone.app.contenttypes.behaviors.leadimage import ILeadImage
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from random import shuffle
from zope.component import getUtility
from zope.i18nmessageid import MessageFactory

import json


_ = MessageFactory("bda.plone.productshop")


def query_children(context, criteria=dict()):
    cat = getToolByName(context, "portal_catalog")
    query = {
        "path": {"query": "/".join(context.getPhysicalPath()), "depth": 1,},
        "sort_on": "getObjPositionInParent",
    }
    query.update(criteria)
    return cat(**query)


def img_scale(context, scale_name):
    if not context.image:
        return None
    scales = context.restrictedTraverse("@@images")
    return scales.scale("image", scale_name)


def img_tag(context, scale_name, css_class):
    scale = img_scale(context, scale_name)
    if not scale:
        return None
    return scale.tag(css_class=css_class)


class ProductView(BrowserView):
    image_scale = "mini"
    overlay_image_scale = "large"

    @property
    def image(self):
        return img_tag(self.context, self.image_scale, "product_image")

    @property
    def details(self):
        return self.context.details

    @property
    def datasheet(self):
        return self.context.datasheet

    @property
    def manual(self):
        manual = getattr(self.context, "manual", None)
        if not manual:
            return None
        return {
            "url": "{0}/@@download/manual".format(self.context.absolute_url()),
            "title": manual.filename,
        }

    @property
    def related_items(self):
        if hasattr(self.context, "relatedItems"):
            related = [_.to_object for _ in self.context.relatedItems]
            return related
        return None

    def overlay_product_image(self):
        self.request.response.setHeader("X-Theme-Disabled", "True")
        return img_tag(self.context, self.overlay_image_scale, "overlay_product_image")


FALLBACK_TILE_COLUMNS = 4


class ProductTiles(BrowserView):
    def query_tile_items(self, context, tile_items, aggregate=True):
        brains = query_children(context)
        if not aggregate:
            brains = [brain for brain in brains]
            shuffle(brains)
        for brain in brains:
            if (
                brain.portal_type == "bda.plone.productshop.productgroup"
                or brain.portal_type == "bda.plone.productshop.product"
            ):
                tile_items.append(brain.getObject())
                if not aggregate:
                    return
            elif brain.portal_type == "Folder":
                obj = brain.getObject()
                if ILeadImage.providedBy(obj) and ILeadImage(obj).image:
                    tile_items.append(obj)
                    continue
                count = len(tile_items)
                self.query_tile_items(
                    brain.getObject(), tile_items, aggregate=False
                )
                # case multi level folder structure
                if len(tile_items) > count + 1:
                    del tile_items[count + 1 :]
                else:
                    tile_items.append(obj)


    def tile_item_context(self, tile_item):
        anchor = aq_inner(self.context)
        context = aq_inner(tile_item)
        while True:
            parent = aq_parent(aq_inner(context))
            if parent == anchor:
                return context
            context = parent

    @property
    def tile_columns(self):
        # read and return from context settings if behavior applied
        if IProductTilesViewSettingsBehavior.providedBy(self.context):
            tile_columns = self.context.product_tiles_view_columns
            if tile_columns and tile_columns > 0:
                return tile_columns
        # read and return from productshop settings
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IProductShopSettings)
        tile_columns = settings.product_tiles_view_columns
        if tile_columns and tile_columns > 0:
            return tile_columns
        # fallback
        return FALLBACK_TILE_COLUMNS

    @property
    def tile_item_image_scale(self):
        # read and return from context settings if behavior applied
        if IProductTilesViewSettingsBehavior.providedBy(self.context):
            return self.context.product_tiles_view_image_scale
        # read and return from productshop settings
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IProductShopSettings)
        return settings.product_tiles_view_image_scale

    def rows(self):
        tile_items = list()
        self.query_tile_items(self.context, tile_items)
        columns = self.tile_columns
        rows = int(len(tile_items) / columns)
        if len(tile_items) % columns > 0:
            rows += 1
        ret = list()
        index = 0
        sm = getSecurityManager()
        for i in range(rows):
            row = list()
            ret.append(row)
            abort = False
            for j in range(columns):
                if index < len(tile_items):
                    tile_item = tile_items[index]
                    item_context = self.tile_item_context(tile_item)
                    if IBuyable.providedBy(item_context) and sm.checkPermission(
                        permissions.ViewBuyableInfo, item_context
                    ):
                        buyable_url = item_context.absolute_url()
                    else:
                        buyable_url = None
                    item_scale = img_scale(tile_item, self.tile_item_image_scale)
                    if item_scale is not None:
                        item_preview = item_scale.url
                    else:
                        item_preview = "++resource++dummy_product.jpg"
                    item_style = """
                        background-image:url('{image}');
                        background-size:cover;
                        background-position:center;
                        background-repeat:no-repeat;
                    """.format(
                        image=item_preview
                    )
                    item_description = item_context.Description()
                    item_description = (
                        item_description and item_description[:60] + "..." or None
                    )
                    row.append(
                        {
                            "display": True,
                            "width": 100.0 / columns,
                            "title": item_context.Title(),
                            "description": item_description,
                            "url": item_context.absolute_url(),
                            "style": item_style,
                            "buyable_url": buyable_url,
                        }
                    )
                else:
                    abort = True
                    row.append(
                        {"display": False, "width": 100.0 / columns,}
                    )
                index += 1
            if abort:
                break
        return ret


LISTING_SLICESIZE = 10


class ProductListingBatch(Batch):
    batchname = "productlisting"

    def __init__(self, context, request, listing):
        self.context = context
        self.request = request
        self.listing = listing

    @property
    def display(self):
        return len(self.listing.result) > LISTING_SLICESIZE

    @property
    def vocab(self):
        ret = list()
        result = self.listing.result
        count = len(result)
        slicesize = self.listing.slicesize
        pages = count / slicesize
        if count % slicesize != 0:
            pages += 1
        current = self.request.get("b_page", "0")
        params = {}
        for param in self.listing.batch_params:
            value = self.request.get(param)
            if value and value != "UNSET":
                params[param] = value
        for i in range(pages):
            params["b_page"] = str(i)
            query = "&".join(
                ["{0}={1}".format(k, v.decode("utf-8")) for k, v in params.items()]
            )
            url = "{0}?{1}".format(self.context.absolute_url(), query)
            ret.append(
                {
                    "page": str(i + 1),
                    "current": current == str(i),
                    "visible": True,
                    "url": url,
                }
            )
        return ret


class ProductListing(BrowserView):
    image_scale = "thumb"
    slicesize = LISTING_SLICESIZE
    batch_params = []

    @property
    def result(self):
        return query_children(self.context)

    @property
    def batch(self):
        return ProductListingBatch(self.context, self.request, self)()

    @property
    def products(self):
        ret = list()
        for brain in self.slice(self.result):
            item = self.create_listing_item(brain)
            if not item:
                continue
            ret.append(item)
        return ret

    def slice(self, result):
        current = int(self.request.get("b_page", "0"))
        start = current * self.slicesize
        end = start + self.slicesize
        return result[start:end]

    def create_listing_item(self, brain):
        obj = brain.getObject()
        if not IProduct.providedBy(obj):
            return None
        item = dict()
        item["obj"] = obj
        item["preview"] = img_tag(obj, self.image_scale, "product_listing_image")
        item["buyable_controls"] = True
        if IProductGroup.providedBy(obj):
            item["buyable_controls"] = False
        return item


class AspectsExtraction(object):
    @property
    def aspects_criteria(self):
        criteria = dict()
        for definition in available_variant_aspects():
            key = definition.attribute
            value = self.request.get(key)
            if value and value != "UNSET":
                criteria["{0}_aspect".format(key)] = value.decode("utf-8")
        return criteria


class ProductGroupListing(ProductListing, AspectsExtraction):
    @property
    def batch_params(self):
        params = list()
        for definition in available_variant_aspects():
            params.append(definition.attribute)
        return params

    @property
    def result(self):
        criteria = self.aspects_criteria
        return query_children(self.context, criteria=criteria)


class ProductGroupView(BrowserView):
    @request_property
    def variant(self):
        obj = None
        for brain in query_children(self.context):
            obj = brain.getObject()
            break
        return obj

    @property
    def rendered_variant(self):
        obj = self.variant
        if obj:
            return obj.restrictedTraverse("@@bda.plone.productshop.variant")
        return None


class Aspects(BrowserView):
    scope = None

    @property
    def variants(self):
        raise NotImplementedError(
            u"Abstract ``Aspects`` does not " u"implement ``variants``."
        )

    @property
    def aspects(self):
        raise NotImplementedError(
            u"Abstract ``Aspects`` does not " u"implement ``aspects``."
        )

    def variant_value(self, definition, context=None):
        if not context:
            context = self.context
        if not definition.interface.providedBy(context):
            return None
        return getattr(context, definition.attribute, None)

    def variant_values(self, definition):
        ret = set()
        for variant in self.variants:
            value = self.variant_value(definition, variant)
            if value:
                ret.add(value)
        return ret

    def create_aspect(self, title, name):
        aspect = dict()
        aspect["title"] = title
        aspect["name"] = name
        aspect["options"] = list()
        return aspect

    def create_option(self, title, value, selected):
        option = dict()
        option["title"] = title
        option["value"] = value
        option["selected"] = selected
        return option


class ProductGroupAspects(Aspects):
    scope = "productgroup"

    @request_property
    def variants(self):
        return [_.getObject() for _ in query_children(self.context)]

    @property
    def aspects(self):
        aspects = list()
        for definition in available_variant_aspects():
            aspect = self.create_aspect(definition.title, definition.attribute)
            options = aspect["options"]
            for value in self.variant_values(definition):
                selected = False
                from_request = self.request.get(definition.attribute)
                if from_request == value.encode("utf-8"):
                    selected = True
                options.append(self.create_option(value, value, selected))
            if options:
                options.insert(0, self.create_option("all", "UNSET", False))
                aspects.append(aspect)
        return aspects


class VariantBase(BrowserView):
    @property
    def product_group(self):
        return aq_parent(aq_inner(self.context))


class VariantAspects(VariantBase, Aspects):
    scope = "variant"

    @request_property
    def variants(self):
        return [_.getObject() for _ in query_children(self.product_group)]

    @property
    def aspects(self):
        aspects = list()
        for definition in available_variant_aspects():
            aspect = self.create_aspect(definition.title, definition.attribute)
            options = aspect["options"]
            selected_value = self.variant_value(definition)
            for value in self.variant_values(definition):
                selected = value == selected_value
                options.append(self.create_option(value, value, selected))
            if options:
                if not selected_value:
                    options.insert(0, self.create_option("-", "UNSET", True))
                aspects.append(aspect)
        return aspects


class VariantView(ProductView, VariantBase):
    @property
    def image(self):
        context_image = img_tag(self.context, self.image_scale, "product_image")
        if context_image:
            return context_image
        return img_tag(self.product_group, self.image_scale, "product_image")

    @property
    def details(self):
        if self.context.details:
            return self.context.details
        return self.product_group.details

    @property
    def datasheet(self):
        if self.context.datasheet:
            return self.context.datasheet
        return self.product_group.datasheet

    @property
    def related_items(self):
        context = self.context
        if hasattr(context, "relatedItems"):
            if context.relatedItems:
                related = [_.to_object for _ in context.relatedItems]
                return related
        product_group = self.product_group
        if hasattr(product_group, "relatedItems"):
            if product_group.relatedItems:
                related = [_.to_object for _ in product_group.relatedItems]
                return related
        return None

    def overlay_product_image(self):
        self.request.response.setHeader("X-Theme-Disabled", "True")
        context_image = img_tag(
            self.context, self.overlay_image_scale, "overlay_product_image"
        )
        if context_image:
            return context_image
        return img_tag(
            self.product_group, self.overlay_image_scale, "overlay_product_image"
        )

    def __call__(self, *args):
        if "_" in self.request.form:
            self.request.response.setHeader("X-Theme-Disabled", "True")
        return super(VariantView, self).__call__()


class VariantLookup(BrowserView, AspectsExtraction):
    @property
    def product_group(self):
        uid = self.request.get("uid")
        if not uid:
            raise ValueError(u"No execution context UID")
        obj = get_object_by_uid(self.context, uid)
        if not obj:
            raise ValueError(u"Execution context object not found by UID")
        if IProductGroup.providedBy(obj):
            return obj
        if IVariant.providedBy(obj):
            return aq_parent(obj)
        raise ValueError(u"Object not implements IProductGroup or IVariant")

    def variant_uid_by_criteria(self):
        """Return UID of first variant found by aspect criteria.

        Base assumption is that each variant has a unique set of aspects. It
        makes not much sence to have 2 Variants with color red and weight 10
        if this 2 aspects are enabled.
        """
        found = False
        oid = uid = url = None
        criteria = self.aspects_criteria
        try:
            product_group = self.product_group
        except ValueError as e:
            return json.dumps({"found": False, "error": str(e),})
        for brain in query_children(product_group, criteria=criteria):
            found = True
            oid = brain.id
            uid = brain.UID
            url = brain.getURL()
            break
        return json.dumps({"found": found, "oid": oid, "uid": uid, "url": url,})
