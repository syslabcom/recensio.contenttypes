from Products.PortalTransforms.transforms.safe_html import scrubHTML
#-*- coding: utf-8 -*-
"""Definition of the Presentation Monograph content type
"""
from cgi import escape
from zope.app.component.hooks import getSite
from zope.i18n import translate
from zope.i18nmessageid import Message
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column
from Products.CMFCore.utils import getToolByName

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.adapter.metadataformat import BaseMetadataFormat
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import (
    BaseReview, BasePresentationNoMagic)
from recensio.contenttypes.content.schemata import (
    BookReviewSchema, CoverPictureSchema, EditorialSchema,
    PagecountSchema, PresentationSchema, ReferenceAuthorsSchema,
    SerialSchema, finalize_recensio_schema)
from recensio.contenttypes.helperutilities import translate_message
from recensio.contenttypes.interfaces import IMetadataFormat
from recensio.contenttypes.interfaces import IPresentationMonograph
from recensio.theme.browser.views import editorTypes
from zope.component import getMultiAdapter

PresentationMonographSchema = BookReviewSchema.copy() + \
                              CoverPictureSchema.copy() + \
                              EditorialSchema.copy() + \
                              PagecountSchema.copy() + \
                              PresentationSchema.copy() + \
                              ReferenceAuthorsSchema.copy() + \
                              SerialSchema.copy() + \
                              atapi.Schema((
    atapi.TextField(
        'tableOfContents',
        schemata="presentation text",
        storage=atapi.AnnotationStorage(),
        widget=atapi.TextAreaWidget(
            label=_(u"Table of contents of the monograph you are presenting"),
            rows=9,
            ),
        ),

    DataGridField(
        'existingOnlineReviews',
        schemata=u"presentation",
        storage=atapi.AnnotationStorage(),
        columns=("name", "url"),
        default=[{'name':'', 'url':''}],
        widget=DataGridWidget(
            label = _(u"Existing online reviews"),
            description=_(
    u'description_existing_online_reviews',
    default=(u"Are there reviews on your text which are already available "
             "online?")
    ),
            columns = {"name" : Column(_(
    u"Name of journal/newspaper/yearbook")),
                       "url" : Column(_(u"URL")),
                       }
            ),
        ),
    DataGridField(
        'publishedReviews',
        schemata="presentation",
        storage=atapi.AnnotationStorage(),
        columns=("details",),
        default=[{'details':''}],
        widget=DataGridWidget(
            label=_(u"Existing print reviews"),
            description=_(
    u'description_pubished_reviews',
    default=(u"Insert here the place of publication of reviews on your text "
             "that have already been published in print.")
    ),
            columns = {"details" :
                       Column(_(
    u"label_published_reviews",
    default=(u"Name of journal/newspaper/yearbook with volume, year and number "
             "of pages")
    ))
                       }
            ),
        ),
))

PresentationMonographSchema['title'].storage = atapi.AnnotationStorage()
PresentationMonographSchema['authors'].widget.label = _(
    u"Author(s) of presented monograph")
PresentationMonographSchema['authors'].widget.description = _(
    u'description_presentation_monograph_authors',
    default=u"Author(s) of presented monograph"
    )
PresentationMonographSchema["uri"].widget.label = _(
    u'description_presentation_uri',
    default=(u"Is the monograph you are presenting available free of "
             "charge online?")
    )
PresentationMonographSchema["uri"].widget.description = _(u"URL")
PresentationMonographSchema["coverPicture"].widget.label = _(
    u"Upload of cover picture")
PresentationMonographSchema["review"].widget.description = _(
    u'description_presentation_monograph_review',
    default=(u"Please give a brief and clear outline of your thesis "
             "statements, your methodology and/or your discussion of "
             "existing research approaches. We would kindly ask you "
             "to avoid a mere summary of your text. Don't be shy, "
             "however, of wording your statements in a provocative "
             "way. By separating out paragraphs you will make your "
             "statement more readable. You can increase the number of "
             "characters available for your own presentation from 4000 "
             "to 6000 by commenting on an already existing "
             "review/presentation on recensio.net. Please note that "
             "both comments and presentations will be checked by the "
             "editorial team before being published in order to "
             "prevent misuse. Because of this texts will be available "
             "online at the earliest after three working days."
             )
    )
PresentationMonographSchema["referenceAuthors"].widget.description = _(
    u'description_reference_authors',
    default=(u"Which scholarly author's work have you mainly engaged with in "
             "your monograph? Please give us the most detailed information "
             "possible on the &raquo;contemporary&laquo; names amongst them as "
             "the recensio.net editorial team will usually try to inform these "
             "authors of the existence of your monograph, your presentation, "
             "and the chance to comment on it. Only the reference author's "
             "name will be visible to the public. Please name historical "
             "reference authors (e.g. Aristotle, Charles de Gaulle) further "
             "below as subject heading.")
    )

PresentationMonographSchema["canonical_uri"].widget.visible = {'edit': 'invisible', 'view': 'invisible'}

finalize_recensio_schema(PresentationMonographSchema,
                         review_type="presentation")


class PresentationMonograph(BaseReview):
    """Presentation Monograph"""
    implements(IPresentationMonograph)

    metadata_type = "PresentationMonograph"
    schema = PresentationMonographSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    # Book = Printed + Authors +
    # Printed = Common +
    # Common = Base +

    # Base
    reviewAuthorHonorific = atapi.ATFieldProperty('reviewAuthorHonorific')
    reviewAuthors = atapi.ATFieldProperty('reviewAuthors')
    reviewAuthorEmail = atapi.ATFieldProperty('reviewAuthorEmail')
    reviewAuthorPersonalUrl = atapi.ATFieldProperty('reviewAuthorPersonalUrl')
    languageReview = atapi.ATFieldProperty('languageReview')
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

    #Editorial
    editorial = atapi.ATFieldProperty('editorial')

    # Printed
    subtitle = atapi.ATFieldProperty('subtitle')
    yearOfPublication = atapi.ATFieldProperty('yearOfPublication')
    placeOfPublication = atapi.ATFieldProperty('placeOfPublication')
    publisher = atapi.ATFieldProperty('publisher')
    idBvb = atapi.ATFieldProperty('idBvb')

    # Authors
    authors = atapi.ATFieldProperty('authors')

    # Book
    isbn = atapi.ATFieldProperty('isbn')

    tableOfContents = atapi.ATFieldProperty('tableOfContents')

    # Cover Picture
    coverPicture = atapi.ATFieldProperty('coverPicture')

    # Presentation
    isLicenceApproved = atapi.ATFieldProperty('isLicenceApproved')

    # Reference authors
    referenceAuthors = atapi.ATFieldProperty('referenceAuthors')

    # Pagecount
    pages = atapi.ATFieldProperty('pages')

    # Serial
    series = atapi.ATFieldProperty('series')
    seriesVol = atapi.ATFieldProperty('seriesVol')

    # Presentation Monograph
    existingOnlineReviews = atapi.ATFieldProperty('existingOnlineReviews')
    publishedReviews = atapi.ATFieldProperty('publishedReviews')

    # Reorder the fields as required
    ordered_fields = [
        # Presented text
        "isbn",
        "uri",
        "tableOfContents",
        "coverPicture",
        'help_authors_or_editors',
        "authors",
        "editorial",
        "languageReviewedText",
        'heading_presented_work',
        "title",
        "subtitle",
        "yearOfPublication",
        "placeOfPublication",
        "publisher",
        "series",
        "seriesVol",
        "pages",
        "ddcSubject",
        "ddcTime",
        "ddcPlace",
        "subject",
        "idBvb",

        # Presentation
        "review",
        "existingOnlineReviews",
        "publishedReviews", # Name, url
        'labelPresentationAuthor',
        "reviewAuthorHonorific",
        "reviewAuthors",
        "reviewAuthorEmail",
        'reviewAuthorPersonalUrl',
        "languageReview",
        "referenceAuthors",
        "isLicenceApproved",
        "canonical_uri",
        "urn",
        "bv",
        ]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view

    metadata_fields = [
        "metadata_review_type_code", "metadata_presentation_author",
        "languageReview", "languageReviewedText", "authors",
        "editorial", "title", "subtitle", "yearOfPublication",
        "placeOfPublication", "publisher", "series", "seriesVol",
        "pages", "isbn", "ddcSubject", "ddcTime", "ddcPlace",
        "subject", "urn", "metadata_recensioID", "idBvb"]

    def editorTypes(self):
        return editorTypes()

    def getDecoratedTitle(self):
        metadata_format = getMultiAdapter((self, self.REQUEST), IMetadataFormat)
        return metadata_format.getDecoratedTitle(self)

    def get_citation_string(self):
        return PresentationMonographNoMagic(self).get_citation_string()

    def getLicense(self):
        return PresentationMonographNoMagic(self).getLicense()

    def getLicenseURL(self):
        return PresentationMonographNoMagic(self).getLicenseURL()

class PresentationMonographNoMagic(BasePresentationNoMagic):

    def get_citation_string(real_self):
        """
        I think the in... part does not make sense for this content type
        Either return the custom citation or the generated one
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.get = lambda x: None
        >>> at_mock.formatted_authors_editorial() = u"Gerken\u2665, Patrick\u2665 / Pilz, Alexander"
        >>> at_mock.title = "Plone 4.0♥?"
        >>> at_mock.subtitle = "Das Benutzerhandbuch♥"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian♥', 'lastname'  : 'de Roiste♥'}]
        >>> at_mock.yearOfPublication = '2009♥'
        >>> at_mock.publisher = 'SYSLAB.COM GmbH♥'
        >>> at_mock.placeOfPublication = 'München♥'
        >>> at_mock.portal_url = lambda :'http://www.syslab.com'
        >>> at_mock.UID = lambda :'12345'
        >>> presentation = PresentationMonographNoMagic(at_mock)
        >>> presentation.directTranslate = lambda m: m.default
        >>> presentation.get_citation_string()
        u'de Roiste\u2665, Cillian\u2665: presentation of: Gerken\u2665, Patrick\u2665 / Pilz, Alexander, Plone 4.0\u2665? Das Benutzerhandbuch\u2665, M\\xfcnchen\u2665: SYSLAB.COM GmbH\u2665, 2009\u2665, <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'


        [Präsentator Nachname], [Präsentator Vorname]: presentation of: [Werkautor Nachname], [Werkautor Vorname], [Werktitel]. [Werk-Untertitel], [Erscheinungsort]: [Verlag], [Jahr], URL recensio.

        Big chunk removed, since it is not a review from a mag in: [Zs-Titel], [Nummer], [Heftnummer (gezähltes Jahr/Erscheinungsjahr)],

        Meier, Hans: presentation of: Meier, Hans, Geschichte des Abendlandes. Ein Abriss, München: Oldenbourg, 2010, in: Zeitschrift für Geschichte, 39, 3 (2008/2009), www.recensio.net/##

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
        if self.title[-1] in '!?:;.,':
            title_subtitle = getFormatter(u' ')
        else:
            title_subtitle = getFormatter(u'. ')

        item = getFormatter(u', ', u', ', u'%(:)s ' % args, u', ')
        mag_number_and_year = getFormatter(u', ', u', ', u' ')
        if False:
            _("presentation of")
        full_citation_inner = getFormatter(
            u'%(:)s %(presentation_of)s ' % args, u', ')
        rezensent_string = rezensent(
            self.reviewAuthors[0]["lastname"],
            self.reviewAuthors[0]["firstname"])
        authors_string = self.formatted_authors_editorial()
        title_subtitle_string = title_subtitle(self.title, self.subtitle)
        item_string = item(
            authors_string, title_subtitle_string,
            self.placeOfPublication, self.publisher,
            self.yearOfPublication)
        return full_citation_inner(
            escape(rezensent_string), escape(item_string),
            real_self.getUUIDUrl())

atapi.registerType(PresentationMonograph, PROJECTNAME)


class MetadataFormat(BaseMetadataFormat):

    def getDecoratedTitle(self, obj):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.formatted_authors_editorial() = "Patrick Gerken / Alexander Pilz"
        >>> at_mock.punctuated_title_and_subtitle = "Plone 4.0. Das Benutzerhandbuch"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian', 'lastname'  : 'de Roiste'}]
        >>> review = PresentationMonographNoMagic(at_mock)
        >>> review.directTranslate = lambda a: a
        >>> review.getDecoratedTitle()
        u'Patrick Gerken / Alexander Pilz: Plone 4.0. Das Benutzerhandbuch (presented_by)'

        Original Specification

        [Werkautor Vorname] [Werkautor Nachname]: [Werktitel]. [Werk-Untertitel]

        Hans Meier: Geschichte des Abendlandes. Ein Abriss
        """
        rezensent_string = getFormatter(' ')(
            obj.reviewAuthors[0]["firstname"], obj.reviewAuthors[0]["lastname"])
        if rezensent_string:
            rezensent_string = "(%s)" % translate_message(
                Message(u"presented_by", "recensio", mapping={u"review_authors": rezensent_string}))
        full_citation = getFormatter(': ', ' ')
        return full_citation(
            obj.formatted_authors_editorial(),
            obj.punctuated_title_and_subtitle,
            rezensent_string,
        )
