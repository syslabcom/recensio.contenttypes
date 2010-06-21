"""Definition of the Rezension einer Zeitschrift content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.interfaces import IRezensioneinerZeitschrift
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.schemata import JournalRezensionSchema

RezensioneinerZeitschriftSchema = JournalRezensionSchema.copy() + atapi.Schema((
    atapi.StringField(
        'herausgeber',
        storage=atapi.AnnotationStorage(),
        widget=atapi.StringWidget(
            label=_(u"Herausgeber"),
            ),
        ),
))

RezensioneinerZeitschriftSchema['title'].storage = atapi.AnnotationStorage()
RezensioneinerZeitschriftSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

schemata.finalizeATCTSchema(RezensioneinerZeitschriftSchema,
                            moveDiscussion=False)


class RezensioneinerZeitschrift(base.ATCTContent):
    """Rezension einer Zeitschrift"""
    implements(IRezensioneinerZeitschrift)

    meta_type = "RezensioneinerZeitschrift"
    schema = RezensioneinerZeitschriftSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    # Journal = Printed + Authors +
    # Printed = Common +
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

    # Printed
    untertitel = atapi.ATFieldProperty('untertitel')
    erscheinungsjahr = atapi.ATFieldProperty('erscheinungsjahr')
    erscheinungsort = atapi.ATFieldProperty('erscheinungsort')
    verlag = atapi.ATFieldProperty('verlag')
    verbundID = atapi.ATFieldProperty('verbundID')
    trefferdaten = atapi.ATFieldProperty('trefferdaten')

    # Authors
    authors = atapi.ATFieldProperty('authors')

    # Journal
    issn = atapi.ATFieldProperty('issn')
    heftnummer = atapi.ATFieldProperty('heftnummer') 
    kuerzelZeitschrift = atapi.ATFieldProperty('kuerzelZeitschrift')
    nummer = atapi.ATFieldProperty('nummer')
    gezaehltesJahr = atapi.ATFieldProperty('gezaehltesJahr')

    # RezensioneinerZeitschrift
    herausgeber = atapi.ATFieldProperty('herausgeber')

atapi.registerType(RezensioneinerZeitschrift, PROJECTNAME)
