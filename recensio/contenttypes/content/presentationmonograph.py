#-*- coding: utf-8 -*-
"""Definition of the Presentation Monograph content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.DataGridField import DataGridField, DataGridWidget
from Products.DataGridField.Column import Column

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.interfaces import IPresentationMonograph
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.review import BaseReview
from recensio.contenttypes.content.schemata import BookReviewSchema
from recensio.contenttypes.content.schemata import CoverPictureSchema

from recensio.contenttypes.content.schemata import PagecountSchema
from recensio.contenttypes.content.schemata import PresentationSchema
from recensio.contenttypes.content.schemata import ReferenceAuthorsSchema
from recensio.contenttypes.content.schemata import SerialSchema

PresentationMonographSchema = BookReviewSchema.copy() + \
                              CoverPictureSchema.copy() + \
                              PagecountSchema.copy() + \
                              PresentationSchema.copy() + \
                              ReferenceAuthorsSchema.copy() + \
                              SerialSchema.copy() + \
                              atapi.Schema((
    DataGridField(
        'existingOnlineReviews',
        storage=atapi.AnnotationStorage(),
        required=True,
        columns=("name", "url"),
        widget=DataGridWidget(
            label = _(u"Existing online reviews"),
            columns = {"name" : Column(_(u"Name of the Journal")),
                       "url" : Column(_(u"URL")),
                       }
            ),
        ),
        atapi.StringField(
        'publishedReviews',
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.StringWidget(
            label=_(u"Published Reviews"),
            rows=3,
            ),
        ),
))

PresentationMonographSchema['title'].storage = atapi.AnnotationStorage()
PresentationMonographSchema['description'].storage = atapi.AnnotationStorage()
PresentationMonographSchema['authors'].widget.label = _(
    u"Autor(en) der präsentierten Monographie")

# Setting the descriptions like this throws an encoding error. When we
# have the translations we can use the English text here instead, or
# replace it with a proper msgid

# PresentationMonographSchema['review'].widget.description=_(
#     u"Bitte formulieren Sie hier kurz und übersichtlich die von Ihnen"+\
#     u"erarbeiteten Thesen, Ihre Methodik und/oder Ihre"+\
#     u"Auseinandersetzung mit bestehenden Forschungsansätzen.  Durch das"+\
#     u"Einfügen von Absätzen erhöhen Sie die Lesbarkeit Ihrer"+\
#     u"Ausführungen.  Durch das Kommentieren einer bereits vorhandenen"+\
#     u"Rezension/Präsentation auf recensio.net erhöhen Sie die für Ihre"+\
#     u"eigene Präsentation zur Verfügung stehende Zeichenzahl von 3000"+\
#     u"auf 4000.")
# PresentationMonographSchema['referenceAuthors'].widget.description=_(
#     u"Mit welchen wissenschaftlichen Autoren haben Sie sich in Ihrer"+\
#     u"Monographie verstärkt auseinandergesetzt?  Wir bitten Sie um"+\
#     u"möglichst detaillierte Angaben zu den darunter befindlichen"+\
#     u"„zeitgenössischen“ Namen, da die recensio.net-Redaktion"+\
#     u"i.d.R. versuchen wird, diese Autoren über die Existenz Ihrer"+\
#     u"Monographie, Ihrer Präsentation und über die Kommentarmöglichkeit"+\
#     u"zu informieren.  Lediglich der Name des Bezugsautors wird"+\
#     u"öffentlich sichtbar sein."+\
#     u"Historische Bezugspersonen (Bsp.: Aristoteles, Charles de Gaulle)"+\
#     u"bitten wir Sie, weiter unten als Schlagwörter zu vergeben.")

schemata.finalizeATCTSchema(PresentationMonographSchema,
                            moveDiscussion=False)

# finalizeATCTSchema moves 'subject' into "categorization" which we
# don't want
PresentationMonographSchema.changeSchemataForField('subject', 'default')


class PresentationMonograph(BaseReview):
    """Presentation Monograph"""
    implements(IPresentationMonograph)

    meta_type = "PresentationMonograph"
    schema = PresentationMonographSchema

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
    languageReview = atapi.ATFieldProperty('languageReview')
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
    ordered_fields = ["isbn", "uri", "pdf", "doc", "review",
                      "existingOnlineReviews", "publishedReviews",
                      "customCitation", "coverPicture",
                      "reviewAuthorHonorific", "reviewAuthorLastname",
                      "reviewAuthorFirstname", "reviewAuthorEmail",
                      "authors", "languageReviewedText",
                      "languageReview", "referenceAuthors", "title",
                      "subtitle", "yearOfPublication",
                      "placeOfPublication", "publisher", "series",
                      "seriesVol", "pages", "ddcSubject",
                      "ddcTime","ddcPlace", "subject", "description",
                      "isLicenceApproved"]

    for i, field in enumerate(ordered_fields):
        schema.moveField(field, pos=i)

    # An ordered list of fields used for the metadata area of the view
    metadata_fields = ["authors", "languageReviewedText",
                       "languageReview", "referenceAuthors",
                       "recensioID", "uri", "idBvb", "authors",
                       "title", "subtitle", "yearOfPublication",
                       "placeOfPublication", "publisher", "series",
                       "seriesVol", "pages", "isbn", "ddcSubject",
                       "ddcTime", "ddcPlace", "subject"]

    # Citation:
    # Präsentator, presentation of: Autor, Titel. Untertitel,
    # Erscheinungsort: Verlag Jahr, in: Zs-Titel, Nummer, Heftnummer
    # (gezähltes Jahr/Erscheinungsjahr), Seite von/bis, URL recensio.

    # NOTE: PresentationMonograph doesn't have:
    # officialYearOfPublication, pageStart, pageEnd
    citation_template =  (u"{reviewAuthorLastname}, {text_presentation_of} "
                          "{authors}, {title}, {subtitle}, "
                          "{placeOfPublication}: {yearOfPublication}, "
                          "{text_in} {publisher}, {series}, {seriesVol}"
                          "({yearOfPublication}), {text_pages} {pages}")

atapi.registerType(PresentationMonograph, PROJECTNAME)
