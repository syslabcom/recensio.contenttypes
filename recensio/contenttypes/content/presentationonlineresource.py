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
from recensio.contenttypes.content.schemata import PresentationSchema



PresentationOnlineResourceSchema = CommonReviewSchema.copy() + \
                                   PresentationSchema.copy() + \
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
            label=_(u"Organisations"),
            format="checkbox",
        ),
    ),
    atapi.StringField(
        'documenttypes_cooperation',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('cooperations_and_communication_values'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Web Services and Communication"),
            format="checkbox",
        ),
    ),
    atapi.StringField(
        'documenttypes_referenceworks',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('reference_values'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Factual Reference Works"),
            format="checkbox",
        ),
    ),
    atapi.StringField(
        'documenttypes_bibliographical',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('bibliographic_source_values'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Bibliographies, Catalogues, Directories"),
            format="checkbox",
        ),
    ),
    atapi.StringField(
        'documenttypes_fulltexts',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('fulltexts_public_domain'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Fulltexts (public domain)"),
            format="checkbox",
        ),
    ),
    atapi.StringField(
        'documenttypes_periodicals',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('periodicals_journals_magazines'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Periodicals (Journals, Magazines)"),
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
    languageReviewedText = atapi.ATFieldProperty('languageReviewedText')
    recensioID = atapi.ATFieldProperty('recensioID')
    subject = atapi.ATFieldProperty('subject')
    pdf = atapi.ATFieldProperty('pdf')
    doc = atapi.ATFieldProperty('doc')
    review = atapi.ATFieldProperty('review')
    customCitation = atapi.ATFieldProperty('customCitation')
    uri = atapi.ATFieldProperty('uri')


    # Common
    ddcPlace = atapi.ATFieldProperty('ddcPlace')
    ddcSubject = atapi.ATFieldProperty('ddcSubject')
    ddcTime = atapi.ATFieldProperty('ddcTime')

    # Presentation
    isLicenceApproved = atapi.ATFieldProperty('isLicenceApproved')

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
    documenttypes_periodicals = \
                         atapi.ATFieldProperty('documenttypes_periodicals')
    documenttypes_fulltexts = \
                         atapi.ATFieldProperty('documenttypes_fulltexts')

    # Reorder the fields as required
    ordered_fields = ["title", "uri", "pdf", "doc", "review",
                      "customCitation", "reviewAuthorHonorific",
                      "reviewAuthorLastname", "reviewAuthorFirstname",
                      "reviewAuthorEmail", "institution",
                      "documenttypes_institution",
                      "documenttypes_cooperation",
                      "documenttypes_referenceworks",
                      "documenttypes_bibliographical",
                      "documenttypes_fulltexts",
                      "documenttypes_periodicals",
                      "languageReviewedText", "languageReview",
                      "ddcSubject", "ddcTime", "ddcPlace", "subject",
                      "description", "isLicenceApproved"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view
    metadata_fields = ["title", "institution", "uri",
                      "documenttypes_institution",
                      "documenttypes_cooperation",
                      "documenttypes_referenceworks",
                      "documenttypes_bibliographical",
                      "documenttypes_fulltexts",
                      "documenttypes_periodicals",
                      "languageReviewedText", "languageReview",
                      "recensioID", "ddcSubject", "ddcTime",
                      "ddcPlace", "subject"]

    # Präsentator, presentation of: Titel, URL Ressource, URL recensio.
    citation_template =  u"{reviewAuthorLastname}, {text_presentation_of} "+\
                        "{title}, {uri}"

atapi.registerType(PresentationOnlineResource, PROJECTNAME)
