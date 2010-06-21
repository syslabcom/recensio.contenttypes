"""Definition of the Praesentation von Aufsatz in Sammelband content type
"""

from zope.interface import implements

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata

from recensio.contenttypes.interfaces import \
     IPraesentationvonAufsatzinSammelband
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.content.schemata import BookRezensionSchema
from recensio.contenttypes.content.schemata import BezugsautorenSchema
from recensio.contenttypes.content.schemata import InternetSchema
from recensio.contenttypes.content.schemata import SerialSchema


PraesentationvonAufsatzinSammelbandSchema = BookRezensionSchema.copy() + \
                                            BezugsautorenSchema.copy() + \
                                            InternetSchema.copy() + \
                                            SerialSchema.copy() + \
                                            atapi.Schema((
    atapi.LinesField(
        'herausgeberSammelband',
        storage=atapi.AnnotationStorage(),
        required=True,
        widget=atapi.LinesWidget(
            label=_(u"Herausgeber Sammelband"),
            rows=3,
            ),
        ),
))

PraesentationvonAufsatzinSammelbandSchema['title'].storage = \
                                                       atapi.AnnotationStorage()
PraesentationvonAufsatzinSammelbandSchema['description'].storage = \
                                                       atapi.AnnotationStorage()

schemata.finalizeATCTSchema(PraesentationvonAufsatzinSammelbandSchema,
                            moveDiscussion=False)


class PraesentationvonAufsatzinSammelband(base.ATCTContent):
    """Praesentation von Aufsatz in Sammelband"""
    implements(IPraesentationvonAufsatzinSammelband)

    meta_type = "PraesentationvonAufsatzinSammelband"
    schema = PraesentationvonAufsatzinSammelbandSchema

    title = atapi.ATFieldProperty('title')
    description = atapi.ATFieldProperty('description')
    # Book = Printed + Authors +
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

    # Book
    isbn = atapi.ATFieldProperty('isbn')

    # Bezugsautoren
    bezugsautoren = atapi.ATFieldProperty('bezugsautoren')

    # Internet
    url = atapi.ATFieldProperty('url')

    # Serial
    reihe = atapi.ATFieldProperty('reihe')
    reihennummer = atapi.ATFieldProperty('reihennummer')

    # Praesentation von Aufsatz in Sammelband
    herausgeberSammelband = atapi.ATFieldProperty('herausgeberSammelband')

atapi.registerType(PraesentationvonAufsatzinSammelband, PROJECTNAME)
