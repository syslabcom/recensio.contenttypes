"""Definition of the Praesentationen von Internetressourcen content type
"""

from zope.interface import implements

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary
from Products.Archetypes import atapi

from recensio.contenttypes.interfaces import \
     IPraesentationenvonInternetressourcen
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.schemata import BaseRezension
from recensio.contenttypes.content.schemata import CommonRezensionSchema
from recensio.contenttypes.content.schemata import InternetSchema

PraesentationenvonInternetressourcenSchema = CommonRezensionSchema.copy() + \
                                             InternetSchema.copy() + \
                                             atapi.Schema((
    atapi.StringField(
        'institution',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Institution"),
        ),
    ),
    atapi.StringField(
        'documentarten_institution',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('institution_values'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Dokumentarten: Institution"),
            format="checkbox",
        ),
    ),
    atapi.StringField(
        'documentarten_kooperation',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('cooperations_and_communication_values'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Dokumentarten: Kooperation und Kommunikation"),
            format="checkbox",
        ),
    ),
    atapi.StringField(
        'documentarten_bibliographische',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('bibliographic_source_values'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Dokumentarten: Bibliographische Quellen"),
            format="checkbox",
        ),
    ),
    atapi.StringField(
        'documentarten_individual',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('individual_publication_values'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Dokumentarten: Individuelle Publikationen"),
            format="checkbox",
        ),
    ),

))

PraesentationenvonInternetressourcenSchema['title'].storage = \
                                                       atapi.AnnotationStorage()
PraesentationenvonInternetressourcenSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PraesentationenvonInternetressourcenSchema,
                            moveDiscussion=False)


class PraesentationenvonInternetressourcen(BaseRezension):
    """Praesentationen von Internetressourcen"""
    implements(IPraesentationenvonInternetressourcen)

    meta_type = "PraesentationenvonInternetressourcen"
    schema = PraesentationenvonInternetressourcenSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    # Common = Base +

    # Base
    rezensionAutor = atapi.ATFieldProperty('rezensionAutor')
    praesentiertenSchriftTextsprache = atapi.ATFieldProperty(
        'praesentiertenSchriftTextsprache')
    praesentationTextsprache = atapi.ATFieldProperty('praesentationTextsprache')
    recensioID = atapi.ATFieldProperty('recensioID')
    schlagwoerter = atapi.ATFieldProperty('schlagwoerter')
    pdf = atapi.ATFieldProperty('pdf')
    doc = atapi.ATFieldProperty('doc')
    rezension = atapi.ATFieldProperty('rezension')

    # Common
    ddcRaum = atapi.ATFieldProperty('ddcRaum')
    ddcSach = atapi.ATFieldProperty('ddcSach')
    ddcZeit = atapi.ATFieldProperty('ddcZeit')

    # Internet
    url = atapi.ATFieldProperty('url')

    # Additional fields
    institution = atapi.ATFieldProperty('institution')
    documentarten_institution = \
                         atapi.ATFieldProperty('documentarten_institution')
    documentarten_kooperation = \
                         atapi.ATFieldProperty('documentarten_kooperation')
    documentarten_bibliographische = \
                         atapi.ATFieldProperty('documentarten_bibliographische')
    documentarten_individual = atapi.ATFieldProperty('documentarten_individual')

    # Reorder the fields as required
    ordered_fields = ["recensioID", "title", "institution",
                      "praesentationTextsprache",
                      "praesentiertenSchriftTextsprache",
                      "documentarten_institution",
                      "documentarten_kooperation",
                      "documentarten_bibliographische",
                      "documentarten_individual", "description",
                      "rezensionAutor", "url", "ddcRaum", "ddcSach",
                      "ddcZeit", "schlagwoerter", "pdf", "doc",
                      "rezension"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

atapi.registerType(PraesentationenvonInternetressourcen, PROJECTNAME)
