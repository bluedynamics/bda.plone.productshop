# -*- coding: utf-8 -*-
from bda.plone.productshop.utils import available_variant_aspects
from bda.plone.productshop.utils import dotted_name
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from plone.app.vocabularies.catalog import KeywordsVocabulary
from zope.interface import implementer


@provider(IVocabularyFactory)
def AvailableVariantAspectsVocabulary(context):
    terms = list()
    for definition in available_variant_aspects():
        terms.append(
            SimpleTerm(value=dotted_name(definition.interface), title=definition.title)
        )
    return SimpleVocabulary(terms)


@implementer(IVocabularyFactory)
class SizeAspectVocabulary(KeywordsVocabulary):
    """
    """

    keyword_index = "size_aspect"


SizeAspectVocabularyFactory = SizeAspectVocabulary()


@implementer(IVocabularyFactory)
class MateriaAspectVocabulary(KeywordsVocabulary):
    """
    """

    keyword_index = "material_aspect"


MateriaAspectVocabularyFactory = MateriaAspectVocabulary()

# Todo add more aspect vocabularies
