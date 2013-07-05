# -*- coding: utf-8 -*-
"""Definition of the Presentation Online Resource content type
"""
from cgi import escape
from zope.interface import implements
from zope.i18nmessageid import Message

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATVocabularyManager import NamedVocabulary
from Products.Archetypes import atapi
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column

from recensio.contenttypes.interfaces import IPresentationOnlineResource
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import (
    BasePresentationNoMagic, BaseReview)
from recensio.contenttypes.content.schemata import (
    CommonReviewSchema, PresentationSchema, finalize_recensio_schema)


PresentationOnlineResourceSchema = CommonReviewSchema.copy() + \
                                   PresentationSchema.copy() + \
                                   atapi.Schema((
# v1001 'institution' field, use upgradeStep to migrate
#    DataGridField(
#        'institution',
#        storage=atapi.AnnotationStorage(),
#        columns=("lastname", "firstname"),
#        default=[{'lastname':'', 'firstname':''}],
#        widget=DataGridWidget(
#            label=_(
#        u'description_institution',
#        default=u"Provider of presented resource (name/institution)"
#                ),
#            description=_(u"Institution"),
#            columns = {"lastname" : Column(_(u"Last name")),
#                       "firstname" : Column(_(u"First name")),
#                       },
#            ),
#        ),
    DataGridField(
        'institution',
        storage=atapi.AnnotationStorage(),
        columns=("name",),
        default=[{'name':'',}],
        widget=DataGridWidget(
            label=_(
        u'description_institution',
        default=u"Provider of presented resource (name/institution)"
                ),
            description=_(u"Institution"),
            columns = {"name" : Column(""),
                       },
            ),
        ),
    atapi.StringField(
        'labelwidget_categories',
        widget=atapi.LabelWidget(
            label=_(
    u"label_online_resource_categories",
    default=(u"Please use the following menu to describe the contents and "
             "services of the resource. In each menu you can choose several "
             "categories.")
    )
            ),
        ),
    atapi.LinesField(
        'documenttypes_institution',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('institution_values'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Institutions"),
                        description=_(
    u'description_documenttypes_institution',
    default=(u"Classify here (if applicable) the institution supplying the "
             "resource")
    ),

            format="checkbox",
        ),
    ),
    atapi.LinesField(
        'documenttypes_cooperation',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('cooperations_and_communication_values'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Web Services and Communication"),
            description=_(
    u'description_documenttypes_cooperation',
    default=u"Type of presented resource"
    ),

            format="checkbox",
        ),
    ),
    atapi.LinesField(
        'documenttypes_referenceworks',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('reference_values'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Factual Reference Works"),
            description=_(
    u'description_documenttypes_referenceworks',
    default=u"Choose here (if applicable) the type of reference works supplied."
    ),

            format="checkbox",
        ),
    ),
    atapi.LinesField(
        'documenttypes_bibliographical',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('bibliographic_source_values'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Bibliographies, Catalogues, Directories"),
            description=_(
    u'description_documenttypes_bibliographical',
    default=(u"Choose here (if applicable) the types of bibliographies, "
             "catalogues, directories supplied.")
    ),
            format="checkbox",
        ),
    ),
    atapi.LinesField(
        'documenttypes_fulltexts',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('fulltexts_public_domain'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Fulltexts (public domain)"),
            description=_(
    u'description_documenttypes_fulltexts',
    default=u"Describe here (if applicable) the full texts and data supplied."
    ),

            format="checkbox",
        ),
    ),
    atapi.LinesField(
        'documenttypes_periodicals',
        storage=atapi.AnnotationStorage(),
        vocabulary=NamedVocabulary('periodicals_journals_magazines'),
        widget=atapi.MultiSelectionWidget(
            label=_(u"Periodicals (Journals, Magazines)"),
            description=_(
    u'description_documenttypes_periodicals',
    default=u"Are there any periodicals supplied in full text?"
    ),

            format="checkbox",
        ),
    ),
))

PresentationOnlineResourceSchema['title'].widget.label = _(u"Name of resource")
PresentationOnlineResourceSchema['title'].storage = atapi.AnnotationStorage()
PresentationOnlineResourceSchema['ddcSubject'].widget.description = _(
    u'description_presentation_online_resource_subject',
    default=(u"Please classify what the online resource provides concerning "
             "subjects, time and area")
    )
PresentationOnlineResourceSchema['uri'].widget.description = u""
PresentationOnlineResourceSchema['review'].widget.label = _(
    u'label_presentation_online_resource_review',
    default=(u"Description"))
PresentationOnlineResourceSchema['review'].widget.description = _(
    u'description_presentation_online_resource_review',
    default=(u"What does the online resource provide? Please outline briefly "
             "and clearly what kind of contents and services the online "
             "resource you are presenting has got to offer. You can increase "
             "the number of characters available for your own presentation "
             "from 2000 to 3000 by commenting on an already existing "
             "review/presentation on recensio.net. Please note that both "
             "comments and presentations will be checked by the editorial "
             "team before being published in order to prevent misuse. "
             "Because of this texts will be availabe online at the earliest "
             "after three working days. ")
    )

PresentationOnlineResourceSchema["canonical_uri"].widget.visible = {'edit': 'invisible', 'view': 'invisible'}

finalize_recensio_schema(PresentationOnlineResourceSchema,
                         review_type="presentation_online")


class PresentationOnlineResource(BaseReview):
    """Presentation Online Resource"""
    implements(IPresentationOnlineResource)

    meta_type = "PresentationOnlineResource"
    schema = PresentationOnlineResourceSchema

    title = atapi.ATFieldProperty('title')
    # Common = Base +

    # Base
    reviewAuthorHonorific = atapi.ATFieldProperty('reviewAuthorHonorific')
    reviewAuthors = atapi.ATFieldProperty('reviewAuthors')
    reviewAuthorEmail = atapi.ATFieldProperty('reviewAuthorEmail')
    reviewAuthorPersonalUrl = atapi.ATFieldProperty('reviewAuthorPersonalUrl')
    languageReview = atapi.ATFieldProperty(
        'languageReview')
    languageReviewedText = atapi.ATFieldProperty('languageReviewedText')
    recensioID = atapi.ATFieldProperty('recensioID')
    subject = atapi.ATFieldProperty('subject')
    review = atapi.ATFieldProperty('review')
    uri = atapi.ATFieldProperty('uri')
    urn = atapi.ATFieldProperty('urn')


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
    ordered_fields=[
        # Presented Resource
        "title",
        "uri",
        "institution",
        "labelwidget_categories",
        "documenttypes_institution",
        "documenttypes_cooperation",
        "documenttypes_referenceworks",
        "documenttypes_bibliographical",
        "documenttypes_fulltexts",
        "documenttypes_periodicals",
        "languageReviewedText",
        "ddcSubject",
        "ddcTime",
        "ddcPlace",
        "subject",

        # Presentation
        "review",
        'labelPresentationAuthor',
        "reviewAuthorHonorific",
        "reviewAuthors",
        "reviewAuthorEmail",
        'reviewAuthorPersonalUrl',
        "languageReview",
        "isLicenceApproved",
        "canonical_uri",
        "urn",
        "bv",
    ]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view

    metadata_fields = ["metadata_review_type_code",
                       "metadata_presentation_author",
                       "languageReview", "title",
                       "uri", "urn", "institution",
                       "languageReviewedText", "documenttypes_institution",
                       "documenttypes_cooperation",
                       "documenttypes_referenceworks",
                       "documenttypes_bibliographical",
                       "documenttypes_fulltexts",
                       "documenttypes_periodicals", "ddcSubject",
                       "ddcTime", "ddcPlace", "subject",
                       "metadata_recensioID"]

    def getDecoratedTitle(self):
        return PresentationOnlineResourceNoMagic(self).getDecoratedTitle()

    def get_citation_string(self):
        return PresentationOnlineResourceNoMagic(self).get_citation_string()

    def getLicense(self):
        return PresentationOnlineResourceNoMagic(self).getLicense()

    def getLicenseURL(self):
        return PresentationOnlineResourceNoMagic(self).getLicenseURL()

class PresentationOnlineResourceNoMagic(BasePresentationNoMagic):

    def getDecoratedTitle(real_self):
        """
        #commented out, because it is unmaintained
        # >>> from mock import Mock
        # >>> at_mock = Mock()
        # >>> at_mock.customCitation = ''
        # >>> at_mock.title = 'Homepage of SYSLAB.COM GmbH'
        # >>> presentation = PresentationOnlineResourceNoMagic(at_mock)
        # >>> presentation.getDecoratedTitle()
        # u'Homepage of SYSLAB.COM GmbH'

        # Original Specification

        # [Titel online resource] ()

        # perspectivia.net – Publikationsplattform für die Geisteswissenschaften
        """
        self = real_self.magic
        rezensent_string = getFormatter(' ')(self.reviewAuthors[0]["firstname"],
                                             self.reviewAuthors[0]["lastname"])
        if rezensent_string:
            rezensent_string = "(%s)" % real_self.directTranslate(
                Message(u"presented_by", "recensio",
                        mapping={u"review_authors": rezensent_string}))
        full_citation = getFormatter(' ')
        return full_citation(
            self.title.decode('utf-8'),
            rezensent_string)

    def get_citation_string(real_self):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.reviewAuthors = [{'firstname' : 'Manuel♥', 'lastname'  : 'Reinhard♥'}]
        >>> at_mock.title = 'Homepage of SYSLAB.COM GmbH♥'
        >>> at_mock.portal_url = lambda :'http://www.syslab.com'
        >>> at_mock.UID = lambda :'12345'
        >>> at_mock.uri = 'http://www.syslab.com/home♥'
        >>> presentation = PresentationOnlineResourceNoMagic(at_mock)
        >>> presentation.directTranslate = lambda m: m.default
        >>> presentation.get_citation_string()
        u'Reinhard\u2665, Manuel\u2665: presentation of: Homepage of SYSLAB.COM GmbH\u2665, http://www.syslab.com/home\u2665, <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'


        Original Specification

        [Präsentator Nachname], [Präsentator Vorname]: presentation of: [Titel online resource], [URL online resource], URL recensio.

        Meier, Hans: presentation of:  perspectivia.net – Publikationsplattform für die Geisteswissenschaften, www.perspectivia.net, www.recensio.net/##
        """
        self = real_self.magic
        args = {
            'presentation_of' : real_self.directTranslate(Message(
                    u"text_presentation_of", "recensio",
                    default="presentation of:")),
            'in'              : real_self.directTranslate(Message(
                    u"text_in", "recensio", default="in:")),
            'page'            : real_self.directTranslate(Message(
                    u"text_pages", "recensio", default="p.")),
            ':'               : real_self.directTranslate(Message(
                    u"text_colon", "recensio", default=":")),
               }
        rezensent = getFormatter(u', ')
        item = getFormatter(u', ', u', ')
        full_citation = getFormatter(u'%(:)s %(presentation_of)s ' % args)
        rezensent_string = rezensent(self.reviewAuthors[0]["lastname"],
                                     self.reviewAuthors[0]["firstname"])
        item_string = item(escape(self.title), escape(self.uri),
                           real_self.getUUIDUrl())
        return full_citation(escape(rezensent_string), item_string)

atapi.registerType(PresentationOnlineResource, PROJECTNAME)
