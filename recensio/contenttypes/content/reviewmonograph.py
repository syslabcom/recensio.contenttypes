#-*- coding: utf-8 -*-
from Products.PortalTransforms.transforms.safe_html import scrubHTML
"""Definition of the Review Monograph content type
"""

from cgi import escape
from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview, BaseReviewNoMagic
from recensio.contenttypes.content.schemata import BookReviewSchema
from recensio.contenttypes.content.schemata import CoverPictureSchema
from recensio.contenttypes.content.schemata import PageStartEndSchema
from recensio.contenttypes.content.schemata import PagecountSchema
from recensio.contenttypes.content.schemata import ReviewSchema
from recensio.contenttypes.content.schemata import SerialSchema
from recensio.contenttypes.content.schemata import finalize_recensio_schema
from recensio.contenttypes.interfaces import IReviewMonograph
from recensio.contenttypes.citation import getFormatter


ReviewMonographSchema = BookReviewSchema.copy() + \
                        CoverPictureSchema.copy() + \
                        PageStartEndSchema.copy() + \
                        PagecountSchema.copy() + \
                        ReviewSchema.copy() + \
                        SerialSchema.copy()

ReviewMonographSchema['title'].storage = atapi.AnnotationStorage()
ReviewMonographSchema['yearOfPublication'].required = True
finalize_recensio_schema(ReviewMonographSchema)


class ReviewMonograph(BaseReview):
    """Review Monograph"""
    implements(IReviewMonograph)

    meta_type = "ReviewMonograph"
    schema = ReviewMonographSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    # Book = Printed + Authors +
    # Printed = Common +
    # Common = Base +

    # Base
    reviewAuthorLastname = atapi.ATFieldProperty('reviewAuthorLastname')
    reviewAuthorFirstname = atapi.ATFieldProperty('reviewAuthorFirstname')
    languageReview = atapi.ATFieldProperty(
        'languageReview')
    languageReviewedText = atapi.ATFieldProperty('languageReviewedText')
    recensioID = atapi.ATFieldProperty('recensioID')
    subject = atapi.ATFieldProperty('subject')
    pdf = atapi.ATFieldProperty('pdf')
    doc = atapi.ATFieldProperty('doc')
    review = atapi.ATFieldProperty('review')
    customCitation = atapi.ATFieldProperty('customCitation')
    canonical_uri = atapi.ATFieldProperty('canonical_uri')
    uri = atapi.ATFieldProperty('uri')
    urn = atapi.ATFieldProperty('urn')

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

    # Cover Picture
    coverPicture = atapi.ATFieldProperty('coverPicture')

    # PageStartEnd
    pageStart = atapi.ATFieldProperty('pageStart')
    pageEnd = atapi.ATFieldProperty('pageEnd')

    # Pagecount
    pages = atapi.ATFieldProperty('pages')

    # Serial
    series = atapi.ATFieldProperty('series')
    seriesVol = atapi.ATFieldProperty('seriesVol')

    # Reorder the fields as required for the edit view
    ordered_fields = [
        # Reviewed Text schemata
        "isbn",
        "urn",
        "languageReviewedText",
        "authors",
        "title",
        "subtitle",
        "yearOfPublication",
        "placeOfPublication",
        "publisher",
        "series",
        "seriesVol",
        "pages",
        "coverPicture",
        "ddcSubject",
        "ddcTime",
        "ddcPlace",
        "subject",
        "idBvb",

        # Review schemata
        "reviewAuthorLastname",
        "reviewAuthorFirstname",
        "languageReview",
        "pdf",
        "pageStart",
        "pageEnd",
        "doc",
        "review",
        "customCitation",
        "uri",
        ]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view

    metadata_fields = ["metadata_review_type_code",
                       "get_publication_title",
                       "metadata_review_author", "languageReview",
                       "languageReviewedText", "authors", "title",
                       "subtitle", "yearOfPublication",
                       "placeOfPublication", "publisher", "series",
                       "seriesVol", "pages", "isbn", "urn",
                       "ddcSubject", "ddcTime", "ddcPlace", "subject",
                       "metadata_recensioID", "idBvb",
                       "canonical_uri"]

    #  Rezensent, review of: Autor, Titel. Untertitel,
    # Erscheinungsort: Verlag Jahr, in: Zs-Titel, Nummer, Heftnummer
    # (gezähltes Jahr/Erscheinungsjahr), Seite von/bis, URL recensio.

    # NOTE: ReviewMonograph doesn't have:
    # officialYearOfPublication, pageStart, pageEnd
    citation_template =  (u"{reviewAuthorLastname}, {text_review_of} "
                          "{authors}, {title}, {subtitle}, "
                          "{placeOfPublication}: {yearOfPublication}, "
                          "{text_in} {publisher}, {series}, {seriesVol}"
                          "({yearOfPublication}), Pages {pages}")

    def get_publication_title(self):
        """ Equivalent of 'titleJournal'"""
        return self.get_title_from_parent_of_type("Publication")

    def get_publication_object(self):
        return self.get_parent_object_of_type("Publication")

    def get_volume_title(self):
        """ Equivalent of 'volume'"""
        return self.get_title_from_parent_of_type("Volume")

    def get_issue_title(self):
        """ Equivalent of 'issue'"""
        return self.get_title_from_parent_of_type("Issue")

    def getDecoratedTitle(self, lastName_first=False):
        return ReviewMonographNoMagic(self).getDecoratedTitle(lastName_first)

    def get_citation_string(self):
        return ReviewMonographNoMagic(self).get_citation_string()

    def getLicense(self):
        return ReviewMonographNoMagic(self).getLicense()

    def getFirstPublicationData(self):
        return ReviewMonographNoMagic(self).getFirstPublicationData()

class ReviewMonographNoMagic(BaseReviewNoMagic):

    def getDecoratedTitle(real_self, lastName_first=False):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.customCitation = ''
        >>> at_mock.authors = [{'firstname': x[0], 'lastname' : x[1]} for x in (('Patrick', 'Gerken'), ('Alexander', 'Pilz'))]
        >>> at_mock.title = "Plone 4.0"
        >>> at_mock.subtitle = "Das Benutzerhandbuch"
        >>> at_mock.reviewAuthorFirstname = 'Cillian'
        >>> at_mock.reviewAuthorLastname = 'de Roiste'
        >>> review = ReviewMonographNoMagic(at_mock)
        >>> review.directTranslate = lambda a: a
        >>> review.getDecoratedTitle()
        u'Patrick Gerken / Alexander Pilz: Plone 4.0. Das Benutzerhandbuch (reviewed by Cillian de Roiste)'

        Original Spec:
        [Werkautor Vorname] [Werkautor Nachname]: [Werktitel]. [Werk-Untertitel] (reviewed by [Rezensent Vorname] [Rezensent Nachname])

        Analog, Werkautoren kann es mehrere geben (Siehe Citation)

        Hans Meier: Geschichte des Abendlandes. Ein Abriss (reviewed by Klaus Müller)

        """
        self = real_self.magic
        if lastName_first:
            authors_string = ' / '.join([getFormatter(', ')(x['lastname'], x['firstname'])
                 for x in self.authors])
        else:
            authors_string = ' / '.join([getFormatter(' ')(x['firstname'], x['lastname'])
                 for x in self.authors])
        titles_string = getFormatter('. ')(self.title, self.subtitle)
        rezensent_string = getFormatter(' ')(self.reviewAuthorFirstname, \
                                     self.reviewAuthorLastname)
        rezensent_string = rezensent_string and "(" +\
             real_self.directTranslate('reviewed by') + " " +\
             rezensent_string + ")" or ""
        full_citation = getFormatter(': ', ' ')
        return full_citation(authors_string, titles_string, rezensent_string)

    def get_citation_string(real_self):
        """
        Either return the custom citation or the generated one
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.customCitation = ''
        >>> at_mock.get = lambda x: None
        >>> at_mock.authors = [{'firstname': x[0], 'lastname' : x[1]} for x in (('Patrick♥', 'Gerke♥n'), ('Alexander', 'Pilz'))]
        >>> at_mock.title = "Plone 4.0♥"
        >>> at_mock.subtitle = "Das Benutzerhandbuch♥"
        >>> at_mock.reviewAuthorFirstname = 'Cillian♥'
        >>> at_mock.reviewAuthorLastname = 'de Roiste♥'
        >>> at_mock.yearOfPublication = '2009♥'
        >>> at_mock.publisher = 'SYSLAB.COM GmbH♥'
        >>> at_mock.placeOfPublication = 'München♥'
        >>> at_mock.get_issue_title = lambda :'Open Source Mag 1♥'
        >>> at_mock.get_volume_title = lambda :'Open Source Mag Vol 1♥'
        >>> at_mock.get_publication_title = lambda :'Open Source♥'
        >>> at_mock.portal_url = lambda :'http://www.syslab.com'
        >>> at_mock.UID = lambda :'12345'
        >>> at_mock.canonical_uri = ''
        >>> review = ReviewMonographNoMagic(at_mock)
        >>> review.get_citation_string()
        u'de Roiste\u2665, Cillian\u2665: review of: Gerke\u2665n, Patrick\u2665 / Pilz, Alexander, Plone 4.0\u2665. Das Benutzerhandbuch\u2665, M\\xfcnchen\u2665: SYSLAB.COM GmbH\u2665, 2009\u2665, in: Open Source\u2665, Open Source Mag Vol 1\u2665, Open Source Mag 1\u2665 (2009\u2665), <a href="http://www.syslab.com/@@redirect-to-uuid/12345">http://www.syslab.com/@@redirect-to-uuid/12345...</a>'


        Original Spec:

        [Rezensent Nachname], [Rezensent Vorname]: review of: [Werkautor Nachname], [Werkautor Vorname], [Werktitel]. [Werk-Untertitel], [Erscheinungsort]: [Verlag], [Jahr], in: [Zs-Titel], [Nummer], [Heftnummer (Erscheinungsjahr)], URL recensio.

        Werkautoren kann es mehrere geben, die werden dann durch ' / ' getrennt alle aufgelistet.
        Note: gezähltes Jahr entfernt.
        Da es die Felder Zs-Titel, Nummer und Heftnummer werden die Titel der Objekte magazine, volume, issue genommen, in dem der Review liegt

        Müller, Klaus: review of: Meier, Hans, Geschichte des Abendlandes. Ein Abriss, München: Oldenbourg, 2010, in: Zeitschrift für Geschichte, 39, 3 (2008/2009), www.recensio.net/##

        """
        self = real_self.magic
        if self.customCitation:
            return scrubHTML(self.customCitation).decode('utf8')
        rezensent = getFormatter(u', ')
        item = getFormatter(u', ', u'. ', u', ', u': ', u', ')
        mag_number_and_year = getFormatter(u', ', u', ', u' ')
        full_citation_inner = getFormatter(u': review of: ', u', in: ', u', ')
        rezensent_string = rezensent(self.reviewAuthorLastname,
                                     self.reviewAuthorFirstname)
        authors_string = u' / '.join(
            [getFormatter(', ')(x['lastname'], x['firstname'])
             for x in self.authors]
                                     )
        item_string = item(authors_string,
                           self.title,
                           self.subtitle,
                           self.placeOfPublication,
                           self.publisher,
                           self.yearOfPublication)
        mag_year_string = self.yearOfPublication.decode('utf-8')
        mag_year_string = mag_year_string and u'(' + mag_year_string + u')' \
            or None
        mag_number_and_year_string = mag_number_and_year(
            self.get_publication_title(), self.get_volume_title(),
            self.get_issue_title(), mag_year_string)

        if getattr(self, "canonical_uri", False): #3102
            citation_string = full_citation_inner(
                escape(rezensent_string), escape(item_string),
                escape(mag_number_and_year_string),
                _(u"label_downloaded_via_recensio",
                  default = u"Downloaded from recensio.net")
                )
        else:
            citation_string = full_citation_inner(
                escape(rezensent_string), escape(item_string),
                escape(mag_number_and_year_string), real_self.getUUIDUrl())
        return citation_string

atapi.registerType(ReviewMonograph, PROJECTNAME)

