# -*- coding: utf-8 -*-
"""Definition of the Presentation Online Resource content type
"""

from zope.interface import implements

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary
from Products.Archetypes import atapi

from recensio.contenttypes.interfaces import \
     IPresentationOnlineResource
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import CommonReviewSchema
from recensio.contenttypes.content.schemata import InternetSchema
from recensio.contenttypes.content.schemata import PresentationSchema

PresentationOnlineResourceSchema = CommonReviewSchema.copy() + \
                                   PresentationSchema.copy() + \
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

PresentationOnlineResourceSchema['title'].storage = \
                                                       atapi.AnnotationStorage()
PresentationOnlineResourceSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PresentationOnlineResourceSchema,
                            moveDiscussion=False)


class PresentationOnlineResource(BaseReview):
    """Presentation Online Resource"""
    implements(IPresentationOnlineResource)

    meta_type = "PresentationOnlineResource"
    schema = PresentationOnlineResourceSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    # Common = Base +

    # Base
    reviewAuthorHonorific = atapi.ATFieldProperty('reviewAuthorHonorific')
    reviewAuthorLastname = atapi.ATFieldProperty('reviewAuthorLastname')
    reviewAuthorFirstname = atapi.ATFieldProperty('reviewAuthorFirstname')
    reviewAuthorEmail = atapi.ATFieldProperty('reviewAuthorEmail')
    languageReview = atapi.ATFieldProperty(
        'languageReview')
    languagePresentation = atapi.ATFieldProperty('languagePresentation')
    recensioID = atapi.ATFieldProperty('recensioID')
    subject = atapi.ATFieldProperty('subject')
    pdf = atapi.ATFieldProperty('pdf')
    doc = atapi.ATFieldProperty('doc')
    review = atapi.ATFieldProperty('review')
    urn = atapi.ATFieldProperty('urn')


    # Common
    ddcPlace = atapi.ATFieldProperty('ddcPlace')
    ddcSubject = atapi.ATFieldProperty('ddcSubject')
    ddcTime = atapi.ATFieldProperty('ddcTime')

    # Presentation 
    isLicenceApproved = atapi.ATFieldProperty('isLicenceApproved')

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
    ordered_fields = ["title", "institution",
                      "languagePresentation", "languageReview",
                      "documentarten_institution",
                      "documentarten_kooperation",
                      "documentarten_bibliographische",
                      "documentarten_individual", "description",
                      "reviewAuthorHonorific", "reviewAuthorLastname",
                      "reviewAuthorFirstname", "reviewAuthorEmail",
                      "url", "ddcPlace", "ddcSubject", "ddcTime",
                      "subject", "pdf", "doc", "urn", "review",
                      "isLicenceApproved"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # Präsentator, presentation of: Titel, URL Ressource, URL recensio.
    citation_template =  u"{reviewAuthorLastname}, {text_presentation_of}: "+\
                        "{title}, {url}"

atapi.registerType(PresentationOnlineResource, PROJECTNAME)
