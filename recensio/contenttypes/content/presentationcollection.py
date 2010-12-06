# -*- coding: utf-8 -*-
"""Definition of the Presentation Collection content type
"""
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import schemata
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column

from recensio.contenttypes.interfaces import \
     IPresentationCollection
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import BookReviewSchema
from recensio.contenttypes.content.schemata import PageStartEndSchema
from recensio.contenttypes.content.schemata import PagecountSchema
from recensio.contenttypes.content.schemata import PresentationSchema
from recensio.contenttypes.content.schemata import ReferenceAuthorsSchema
from recensio.contenttypes.content.schemata import SerialSchema
from recensio.contenttypes.content.schemata import finalize_recensio_schema

PresentationCollectionSchema = BookReviewSchema.copy() + \
                               PagecountSchema.copy() + \
                               PresentationSchema.copy() + \
                               ReferenceAuthorsSchema.copy() + \
                               PageStartEndSchema.copy() + \
                               SerialSchema.copy() + \
                               atapi.Schema((
    atapi.StringField(
        'titleCollectedEdition',
        schemata=_(u"presented text"),
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Title / Subtitle"),
            description=_(
    u'description_title_collected_edition',
    default=u"Information on the associated edited volume"
    ),
            ),
        ),

    DataGridField(
        'editorsCollectedEdition',
        storage=atapi.AnnotationStorage(),
        required=True,
        columns=("lastname", "firstname"),
        widget=DataGridWidget(
            label = _(u"Editor(s)"),
            columns = {"lastname" : Column(_(u"Last name")),
                       "firstname" : Column(_(u"First name")),
                       }
            ),
        ),
))

PresentationCollectionSchema['title'].storage = atapi.AnnotationStorage()
PresentationCollectionSchema["authors"].widget.label=_(
    "label_presentation_article_authors",
    default=u"Author(s) of presented article")
PresentationCollectionSchema["referenceAuthors"].widget.description = _(
    u'description_reference_authors',
    default=(u"Which scholarly author's work have you mainly engaged with in "
             "your article? Please give us the most detailed information "
             "possible on the &raquo;contemporary&laquo; names amongst them as "
             "the recensio.net editorial team will usually try to inform these "
             "authors of the existence of your article, your presentation, "
             "and the chance to comment on it. Only the reference author's "
             "name will be visible to the public. Please name historical "
             "reference authors (e.g. Aristotle, Charles de Gaulle) further "
             "below as subject heading.")
    )

finalize_recensio_schema(PresentationCollectionSchema,
                         review_type="presentation_collection")

class PresentationCollection(BaseReview):
    """Presentation Collection"""
    implements(IPresentationCollection)

    meta_type = "PresentationCollection"
    schema = PresentationCollectionSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    # Book = Printed + Authors +
    # Printed = Common +
    # Common = Base +

    # Base
    reviewAuthorHonorific = atapi.ATFieldProperty('reviewAuthorHonorific')
    reviewAuthorLastname = atapi.ATFieldProperty('reviewAuthorLastname')
    reviewAuthorFirstname = atapi.ATFieldProperty('reviewAuthorFirstname')
    reviewAuthorEmail = atapi.ATFieldProperty('reviewAuthorEmail')
    reviewAuthorPersonalUrl = atapi.ATFieldProperty('reviewAuthorPersonalUrl')
    languageReview = atapi.ATFieldProperty(
        'languageReview')
    languageReviewedText = atapi.ATFieldProperty('languageReviewedText')
    recensioID = atapi.ATFieldProperty('recensioID')
    subject = atapi.ATFieldProperty('subject')
    review = atapi.ATFieldProperty('review')
    uri = atapi.ATFieldProperty('uri')


    # Common
    ddcPlace = atapi.ATFieldProperty('ddcPlace')
    ddcSubject = atapi.ATFieldProperty('ddcSubject')
    ddcTime = atapi.ATFieldProperty('ddcTime')

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

    # Presentation 
    isLicenceApproved = atapi.ATFieldProperty('isLicenceApproved')

    # Reference authors
    referenceAuthors = atapi.ATFieldProperty('referenceAuthors')

    # Serial = PageStartEnd +
    pageStart = atapi.ATFieldProperty('pageStart')
    pageEnd = atapi.ATFieldProperty('pageEnd')

    # Pagecount
    pages = atapi.ATFieldProperty('pages')

    # Serial
    series = atapi.ATFieldProperty('series')
    seriesVol = atapi.ATFieldProperty('seriesVol')

    # Presentation Collection
    titleCollectedEdition = atapi.ATFieldProperty('titleCollectedEdition')
    editorsCollectedEdition = atapi.ATFieldProperty('editorsCollectedEdition')

    # Reorder the fields as required
    ordered_fields = [
        # Presented Text
        "isbn",
        "uri",
        "authors",
        "languageReviewedText",
        "title",
        "subtitle",
        "pageStart",
        "pageEnd",
        "titleCollectedEdition",
        "editorsCollectedEdition",
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
        'reviewAuthorPersonalUrl',
        'labelPresentationAuthor',
        "reviewAuthorHonorific",
        "reviewAuthorLastname",
        "reviewAuthorFirstname",
        "reviewAuthorEmail",
        "languageReview",
        "referenceAuthors",
        "isLicenceApproved"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view
    metadata_fields = ["metadata_review_type_code",
                       "metadata_review_author",
                       "languageReviewedText", "languageReview",
                       "authors", "authors", "title", "subtitle",
                       "pageStart", "pageEnd",
                       "editorsCollectedEdition",
                       "titleCollectedEdition", "yearOfPublication",
                       "placeOfPublication", "publisher", "series",
                       "seriesVol", "pages", "isbn", "ddcSubject",
                       "ddcTime", "ddcPlace", "subject",
                       "referenceAuthors", "uri",
                       "metadata_recensioID", "idBvb"]

    # Präsentator, presentation of: Autor, Titel. Untertitel, in:
    # Herausgeber, Titel. Untertitel, Erscheinungsort: Verlag Jahr,
    # URL recensio.
    citation_template =  (u"{reviewAuthorLastname}, {text_presentation_of} "
                          "{authors}, {title}, {subtitle}, {text_in} "
                          "{editorsCollectedEdition}, "
                          "{title}, {subtitle}, "
                          "{placeOfPublication}: {publisher} "
                          "{yearOfPublication}")

    def getDecoratedTitle(self):
        return PresentationCollectionNoMagic(self).getDecoratedTitle()

    def get_citation_string(self):
        return PresentationCollectionNoMagic(self).get_citation_string()

    def getLicense(self):
        return PresentationCollectionNoMagic(self).getLicense()

    def getLicenseURL(self):
        return PresentationCollectionNoMagic(self).getLicenseURL()

class PresentationCollectionNoMagic(object):
    def __init__(self, at_object):
        self.magic = at_object

    def getDecoratedTitle(real_self):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.customCitation = ''
        >>> at_mock.authors = [{'firstname': x[0], 'lastname' : x[1]} for x in (('Patrick', 'Gerken'), ('Alexander', 'Pilz'))]
        >>> at_mock.title = "Das neue Plone 4.0"
        >>> at_mock.subtitle = "Alles neu in 2010"
        >>> review = PresentationCollectionNoMagic(at_mock)
        >>> review.getDecoratedTitle()
        u'Patrick Gerken / Alexander Pilz: Das neue Plone 4.0. Alles neu in 2010'

        [Werkautor Vorname] [Werkautor Nachname]: [Werktitel]. [Werk-Untertitel]

        Hans Meier: Geschichte des Abendlandes. Ein Abriss
        """
        self = real_self.magic
        authors_string = u' / '.join([getFormatter(' ')(x['firstname'], x['lastname'])
             for x in self.authors])
        titles_string = getFormatter(u'. ')(self.title, self.subtitle)
        return u": ".join((authors_string, titles_string))

    def get_citation_string(real_self):
        """
        NOTE: There is no differentiation between title and subtitle of
        the collection book.
        Either return the custom citation or the generated one
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.customCitation = ''
        >>> at_mock.get = lambda x: None
        >>> at_mock.authors = [{'firstname': x[0], 'lastname' : x[1]} for x in (('Patrick', 'Gerken'), ('Alexander', 'Pilz'))]
        >>> at_mock.editorsCollectedEdition = [{'firstname': x[0], 'lastname' : x[1]} for x in (('Tina', 'Pecek'), ('Wolfgang', 'Thomas'))]
        >>> at_mock.title = "Plone 4.0 für Dummies"
        >>> at_mock.subtitle = "Plone 4 in 19 Tagen lernen!"
        >>> at_mock.titleCollectedEdition = 'Plone 4 komplett. ALLES zu Plone'
        >>> at_mock.reviewAuthorFirstname = 'Cillian'
        >>> at_mock.reviewAuthorLastname = 'de Roiste'
        >>> at_mock.yearOfPublication = '2010'
        >>> at_mock.publisher = 'SYSLAB.COM GmbH'
        >>> at_mock.placeOfPublication = u'München'
        >>> at_mock.issueNumber = '3'
        >>> at_mock.volumeNumber = '1'
        >>> at_mock.titleJournal = 'Open Source Mag'
        >>> at_mock.absolute_url = lambda :'http://www.syslab.com'
        >>> presentation = PresentationCollectionNoMagic(at_mock)
        >>> presentation.get_citation_string()
        u'de Roiste, Cillian: presentation of: Gerken, Patrick / Pilz, Alexander, Plone 4.0 f\\xfcr Dummies. Plone 4 in 19 Tagen lernen!, in: Pecek, Tina / Thomas, Wolfgang (ed.), Plone 4 komplett. ALLES zu Plone, M\\xc3\\xbcnchen, SYSLAB.COM GmbH, 2010, http://www.syslab.com'

        Original Specification

        [Präsentator Nachname], [Präsentator Vorname]: presentation of: [Werkautor Nachname], [Werkautor Vorname], [Werktitel]. [Werk-Untertitel], in: [Hrsg. Sammelband Nachname], [Hrsg. Sammelband Vorname] (ed.), [Titel Sammelband], [Erscheinungsort]: [Verlag], [Jahr], URL recensio.

        Hrsg.Sammelband Editoren kann es mehrere geben, die werden dann durch ' / ' getrennt alle aufgelistet.
        Note: Untertitel Sammelband entfernt, dieser wird in das Feld Titel Sammelband eingetragen
        Note: gezähltes Jahr entfernt.

        Meier, Hans: presentation of: Meier, Hans, Geschichte des Abendlandes. Ein Abriss, in: Müller, Hans (ed.), Geschichte des Morgen- und Abendlandes. Eine Übersicht, München: Oldenbourg, 2010, www.recensio.net/##
        """
        self = real_self.magic
        gf = getFormatter
        rezensent = getFormatter(u', ')
        item = getFormatter(u', ', u'. ')
        hrsg_person = getFormatter(', ')
        hrsg_company_year = getFormatter(', ')
        hrsg_book = getFormatter(', ', ', ', ': ')
        hrsg = getFormatter(' (ed.), ')
        full_citation = getFormatter(u': presentation of: ', u', in: ', u', ')
        rezensent_string = rezensent(self.reviewAuthorLastname, \
                                     self.reviewAuthorFirstname)
        authors_string = u' / '.join([getFormatter(', ')\
                                       (x['lastname'], x['firstname'])
                                    for x in self.authors])
        item_string = item(authors_string,
                           self.title,
                           self.subtitle)
        hrsg_person_string = u' / '.join([getFormatter(', ')\
                                        (x['lastname'], x['firstname'])
                                    for x in self.editorsCollectedEdition])
        hrsg_company_year_string = hrsg_company_year(self.publisher, \
                                                     self.yearOfPublication)
        hrsg_book_string = hrsg_book(self.titleCollectedEdition, \
                                     self.placeOfPublication, \
                                        hrsg_company_year_string)
        hrsg_string = hrsg(hrsg_person_string, hrsg_book_string)
        return full_citation(rezensent_string, item_string, \
            hrsg_string, self.absolute_url())

    def getLicense(real_self):
        self = real_self.magic
        return _('license-note-presentation')

    def getLicenseURL(real_self):
        self = real_self.magic
        return {'msg' : _('license-note-presentation-url-text'),
                'url' : _('license-note-presentation-url-url')}

atapi.registerType(PresentationCollection, PROJECTNAME)
