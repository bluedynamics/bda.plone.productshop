Changes
=======

1.0b2 (unreleased)
------------------

- Nothing changed yet.


1.0b1 (2024-04-22)
------------------

- Plone 6 compatibility.
  [petschki, agitator]

- Fix problem with AvailableVariantAspectsVocabulary not repescting named behaviors.
  [jensens]

- Fix some namings and DE translation.
  [jensens]

- Edit icon in and edit on overlay in listing.
  [jensens]

- Remove dummy image from product view, only show image if uploaded.
  [jensens]

- Basic responsive tiles view using bootstrap classes [jensens]

- Show empty Folders oder Folders without image in tiles listing [jensens]

- Fix depreaction warnings in behaviors [jensens]

- Fix Problem with Python 3 division (float instead of int) [jensens]

- Remove binding to CMFDefault skin in ZCML [jensens]

- fix condition for `details` richtext
  [petschki]

- Added italian translations
  [ale-rt]


0.8
---

- Add ajax overlay with large product image in product view when clicking on
  thumb.
  [rnix]

- Improve tiles view.
  [rnix]


0.7
---

- Display invalid aspects message in red.
  [rnix]

- Check for ``ILeadImage`` on folder instead of whether ``image`` attributes
  exists in ``ProductTiles.query_tile_items``.
  [rnix]

- Add Generic Setup ``viewlets.xml`` file and hide
  ``plone.belowcontentbody.relateditems`` by default.
  [rnix]


0.6
---

- Format ``actions.xml`` to make action translations work properly. GS Profile
  application required.
  [rnix]

- Remove ``item_number`` from
  ``bda.plone.productshop.behaviors.IProductBehavior``. It's provided by
  ``bda.plone.shop.dx.ITradingBehavior`` now for products and variants, and
  productgroups do not rely on this information at all.
  [rnix]

- Apply ``bda.plone.shop.dx.ITradingBehavior`` behavior to product and variant
  content types.
  [rnix]

- Display link to manual download in product view description tab if present.
  [rnix]

- Also hide buyable controls overlay if mouse cursor enters empty placeholder
  column.
  [rnix]

- Consider view buyable information permission in product tiles.
  [rnix]

- Consider image field on folder if present in product tiles view.
  [rnix]

- Add ``bda.plone.productshop.behavior.IProductManualBehavior`` and apply it
  to product and variant content types.
  [rnix]

- Add ``bda.plone.shop.dx.IBuyablePeriodBehavior`` to product and variant
  content types.
  [rnix]

- Rename ``shopviews.css`` to ``productshop.css``. Re-applying GS profile
  required.
  [rnix]

- Fix product tiles view, overlay buyable controls are shown only if tile item
  represents buyable item directly.
  [rnix]


0.5
---

- Display buyable controls as overlay on mouse over on product tiles if
  displayed item in tile is buyable.
  [rnix]

- Add ``IProductShopSettings`` and ``IProductTilesViewSettingsBehavior``, both
  providing ``product_tiles_view_columns`` and
  ``product_tiles_view_image_scale`` properties, used in ``ProductTiles`` view.
  [rnix]


0.4
---

- Add product tiles view for plone site and folders.
  [rnix]

- Enable discount settings on productgroup.
  [rnix]

- Absolute imports.
  [rnix]

- Add ``IMaterialBehavior`` variant aspect.
  [rnix]

- Apply notification text behaviors to product shop types.
  [rnix]


0.3
---

- Product listing is now batched.
  [rnix]

- Add ``IAngleBehavior`` variant aspect.
  [rnix]

- Add ``IIPCodeBehavior`` variant aspect.
  [rnix]

- Handle query criteria as unicode to avoid ``UnicodeDecodeError``.
  [rnix]

- Add ``IShippingBehavior`` to product and variant types.
  [rnix]

- Add item number to ``IProduct``.
  [rnix]

- Add variant aspects ``ILengthBehavior``, ``IWidthBehavior`` and
  ``IHeightBehavior``.
  [rnix]


0.2
---

- Productgroup can define default variant aspects.
  [rnix]

- Add german translation.
  [rnix]

- Introduce ``IProductExcludeFromNavigation``.
  [rnix]

- Rename package to ``bda.plone.productshop``.
  [rnix]

- Add content types ``product``, ``productgroup``, ``variant``.
  [rnix]

- Reduce available views.
  [rnix]


0.1
---

- Initial work.
  [espenmn]
