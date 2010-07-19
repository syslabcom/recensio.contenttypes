# -*- coding: utf-8 -*-
"""Definition of the Presentation Online Resource content type
"""

from zope.interface import implements

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary
from Products.Archetypes import atapi
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column

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
    DataGridField(
        'institution',
        storage=atapi.AnnotationStorage(),
        columns=("institution", "lastname", "firstname"),
        widget=DataGridWidget(
            label=_(u"Institution"),
            columns = {"institution" : Column(_(u"Institution")),
                       "lastname" : Column(_(u"Lastname")),
                       "firstname" : Column(_(u"Firstname")),
                       }
        ),
    ),
    atapi.StringField(
        'documenttypes_institution',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('institution_values'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Dokumentarten: Institution"),
            format="checkbox",
        ),
    ),
    atapi.StringField(
        'documenttypes_cooperation',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('cooperations_and_communication_values'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Dokumentarten: Cooperation und Kommunikation"),
            format="checkbox",
        ),
    ),
    atapi.StringField(
        'documenttypes_referenceworks',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('reference_values'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Dokumentarten: Nachschlagewerke"),
            format="checkbox",
        ),
    ),
    atapi.StringField(
        'documenttypes_bibliographical',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('bibliographic_source_values'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Dokumentarten: Bibliographical Quellen"),
            format="checkbox",
        ),
    ),
    atapi.StringField(
        'documenttypes_individual',
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

# finalizeATCTSchema moves 'subject' into "categorization" which we
# don't want
PresentationOnlineResourceSchema.changeSchemataForField('subject', 'default')


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
    customCitation = atapi.ATFieldProperty('customCitation')
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
    documenttypes_institution = \
                         atapi.ATFieldProperty('documenttypes_institution')
    documenttypes_cooperation = \
                         atapi.ATFieldProperty('documenttypes_cooperation')
    documenttypes_referenceworks = \
                         atapi.ATFieldProperty('documenttypes_referenceworks')
    documenttypes_bibliographical = \
                         atapi.ATFieldProperty('documenttypes_bibliographical')
    documenttypes_individual = atapi.ATFieldProperty('documenttypes_individual')

    # Reorder the fields as required
    ordered_fields = ["title", "url", "urn", "pdf", "doc", "review",
                      "customCitation", "reviewAuthorHonorific",
                      "reviewAuthorLastname", "reviewAuthorFirstname",
                      "reviewAuthorEmail", "institution",
                      "documenttypes_institution",
                      "documenttypes_cooperation",
                      "documenttypes_referenceworks",
                      "documenttypes_bibliographical",
                      "documenttypes_individual",
                      "languagePresentation", "languageReview",
                      "ddcSubject", "ddcTime", "ddcPlace", "subject",
                      "description", "isLicenceApproved"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # Präsentator, presentation of: Titel, URL Ressource, URL recensio.
    citation_template =  u"{reviewAuthorLastname}, {text_presentation_of}: "+\
                        "{title}, {url}"

atapi.registerType(PresentationOnlineResource, PROJECTNAME)
