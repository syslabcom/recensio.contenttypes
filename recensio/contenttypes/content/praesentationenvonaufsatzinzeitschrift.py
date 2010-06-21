"""Definition of the Praesentationen von Aufsatz in Zeitschrift content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.interfaces import IPraesentationenvonAufsatzinZeitschrift
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.schemata import JournalRezensionSchema
from recensio.contenttypes.content.schemata import BezugsautorenSchema
from recensio.contenttypes.content.schemata import InternetSchema
from recensio.contenttypes.content.schemata import ZeitenzahlSchema


PraesentationenvonAufsatzinZeitschriftSchema = \
                                             JournalRezensionSchema.copy() + \
                                             BezugsautorenSchema.copy() + \
                                             InternetSchema.copy() + \
                                             ZeitenzahlSchema.copy()

PraesentationenvonAufsatzinZeitschriftSchema['title'].storage = \
                                                       atapi.AnnotationStorage()
PraesentationenvonAufsatzinZeitschriftSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PraesentationenvonAufsatzinZeitschriftSchema,
                            moveDiscussion=False)


class PraesentationenvonAufsatzinZeitschrift(base.ATCTContent):
    """Praesentationen von Aufsatz in Zeitschrift"""
    implements(IPraesentationenvonAufsatzinZeitschrift)

    meta_type = "PraesentationenvonAufsatzinZeitschrift"
    schema = PraesentationenvonAufsatzinZeitschriftSchema

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

    # Bezugsautoren
    bezugsautoren = atapi.ATFieldProperty('bezugsautoren')

    # Internet
    url = atapi.ATFieldProperty('url')

    # Zeitenzahl
    zeitenzahl = atapi.ATFieldProperty('zeitenzahl')

atapi.registerType(PraesentationenvonAufsatzinZeitschrift, PROJECTNAME)
