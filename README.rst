=====================
bda.plone.productshop
=====================

.. image:: https://travis-ci.org/bluedynamics/bda.plone.productshop.svg?branch=master
    :target: https://travis-ci.org/bluedynamics/bda.plone.productshop
.. image:: https://coveralls.io/repos/bluedynamics/bda.plone.productshop/badge.png
    :target: https://coveralls.io/r/bluedynamics/bda.plone.productshop

Product shop extension for ``bda.plone.shop``.

Overview
========

This package contains dexterity content types and the corresponding views
for building a typical product shop.


A brief description about the contained types
---------------------------------------------

**Product**

A product which can be added to folders. A product consists of default
metadata, an image, a detailed description, a datasheet and related items.

**Product Group**

A product group is a collection of product like objects with several aspects
applied to it. The contained items are of type ``Variant``. Further a
product group provides the same fields as a ``Product``. The default variant
aspects for newly created variants inside this product group can be defined
on the product group.

**Variant**

A Variant is a ``Product`` with several aspects applied to it, like weight,
size, etc. and is contained in a ``Product Group``. The different aspects
can be enabled and disabled explicitly after creation via object actions. The
default aspects enabled are read from parent product group


A brief description about the contained views
---------------------------------------------

**product tiles**

The product tiles view can be applied on site root and folders. The view
displays a grid of tiles built of contained folders and buyable items. If tile
context is a folder, title and description are taken from the folder, and the
preview image is taken randomly from a contained buyable item. If tile context
is a buyable item, title, description and preview image are taken from it and
on mouse over buyable controls are rendered in an overlay for this item. The
number of grid columns rendered can be defined globally in control panel, or,
if ``IProductTilesViewSettingsBehavior`` is applied on folders directly
(``plone.app.contenttypes`` only, Archetypes folders are not suppoerted).

**product listing**

The product listing can be applied on folders and on product groups. When
applied on folder it lists the first level of the contained products and
product groups. When applied on a product group it lists the contained variants
and a filter at the top to restrict listing by variant aspects.

**product view**

The product view can be applied on products, product groups an variants. When
applied on products, it displays the product data and the buyable controls
provided by ``bda.plone.shop``. When applied on a variant, additionally the
aspect filter gets shown which can be used for instant navigation between
available variants in containing product group. When applied on a product group
the first contained variant gets displayed as descibed above.


Installation
============

Install standalone
------------------

Install system dependencies::

    sudo apt-get install python-virtualenv

Install Instance::

    virtualenv --no-site-packages vpython
    ./vpython/bin/python bootstrap.py
    ./bin/buildout


Install as product
------------------

Add ``bda.plone.productshop`` to the instance eggs in buildout.cfg or depend
your integration package to it.

Install as addon in plone control panel or via generic setup dependency in your
integration package.


Provide additional variant aspects
==================================

If desired variant aspect is generic, fork this project from
``https://github.com/bluedynamics/bda.plone.productshop``, add it directly
there and create a pull request.


Following steps are necessary to add a variant aspect
-----------------------------------------------------

Create a variant behavior like the ones in
``bda.plone.productshop.behaviors``::

    @provider(IFormFieldProvider)
    class IDemandBehavior(IVariantAspect):
        """Demand variant behavior.
        """
        model.fieldset(
            'aspects',
            label=_(u'aspects', default=u'Aspects'),
            fields=['demand'])
        demand = schema.TextLine(
            title=_(u'demand_title', default=u'Demand'),
            description=_(u'demand_description',
                          default=u'Demand of the product'),
            required=False)

**Note**: Aspect field type must always be a text line to work correctly with
          the filter views.

Register this behavior via ZCML::

    <plone:behavior
      title="Demand"
      description="Extend content with product demand."
      provides=".behaviors.IDemandBehavior"
      for="collective.instancebehavior.IInstanceBehaviorAssignableContent" />

Create an indexer for the aspect field like the ones in
``bda.plone.productshop.indexer``::

    @indexer(IDemandBehavior)
    def demand_aspect(obj):
        return obj.demand

**Note**: Index name must be postfixed with ``_aspect`` all over the place.
          this way we hopefully avoid naming collisions.

Register the indexer via ZCML::

    <adapter name="demand_aspect" factory=".indexer.demand_aspect" />

Create the index at install time via generic setup profile. Add to
``catalog.xml``::

    <index name="demand_aspect" meta_type="FieldIndex">
      <indexed_attr value="demand_aspect" />
    </index>

Create the object action for the aspect that it can be enabled ttw like the
ones in ``bda.plone.productshop.browser.actions``::

    class DemandAction(VariantAspectAction):
        aspect_title = _(u'aspect_demand', default=u'Demand')
        aspect_behavior = 'bda.plone.productshop.behaviors.IDemandBehavior'
        aspect_schema = IDemandBehavior

Configure necessary action views::

    <!-- demand -->
    <browser:page
      name="enable_demand"
      attribute="enable_aspect"
      for="..interfaces.IVariant"
      class=".actions.DemandAction"
      permission="cmf.ModifyPortalContent"
      layer="..interfaces.IProductShopExtensionLayer" />

    <browser:page
      name="disable_demand"
      attribute="disable_aspect"
      for="..interfaces.IVariant"
      class=".actions.DemandAction"
      permission="cmf.ModifyPortalContent"
      layer="..interfaces.IProductShopExtensionLayer" />

    <browser:page
      name="can_enable_demand"
      attribute="can_enable"
      for="*"
      class=".actions.DemandAction"
      permission="cmf.ModifyPortalContent"
      layer="..interfaces.IProductShopExtensionLayer" />

    <browser:page
      name="can_disable_demand"
      attribute="can_disable"
      for="*"
      class=".actions.DemandAction"
      permission="cmf.ModifyPortalContent"
      layer="..interfaces.IProductShopExtensionLayer" />

Create the corresponding object actions at install time via generic setup
profile. Add to ``actions.xml``::

    <!-- demand -->
    <object name="enable_demand"
            meta_type="CMF Action"
            i18n:domain="bda.plone.productshop">
      <property name="title" i18n:translate="">
          Add demand
      </property>
      <property name="description" i18n:translate="">
          Add demand to product variant
      </property>
      <property name="url_expr">
          string:${object/absolute_url}/@@enable_demand
      </property>
      <property name="icon_expr"></property>
      <property name="available_expr">
          object/@@can_enable_demand
      </property>
      <property name="permissions">
          <element value="Modify portal content" />
      </property>
      <property name="visible">True</property>
    </object>

    <object name="disable_demand"
            meta_type="CMF Action"
            i18n:domain="bda.plone.productshop">
      <property name="title" i18n:translate="">
          Remove demand
      </property>
      <property name="description" i18n:translate="">
          Remove demand from product variant
      </property>
      <property name="url_expr">
          string:${object/absolute_url}/@@disable_demand
      </property>
      <property name="icon_expr"></property>
      <property name="available_expr">
          object/@@can_disable_demand
      </property>
      <property name="permissions">
          <element value="Modify portal content" />
      </property>
      <property name="visible">True</property>
    </object>


TODO
====

- Define which richtext fields of a product gets rendered as tabs in
  product view.

- Create control panel. This should contain global configuration which
  variant aspects are available in the instance.


Contributors
============

- Robert Niederreiter (Autor)
- Espen Moe-Nilssen
- Peter Holzer


Dummy product image from
========================

- http://thelittlereaper.deviantart.com/art/Test-Crash-Dummy-169618976
