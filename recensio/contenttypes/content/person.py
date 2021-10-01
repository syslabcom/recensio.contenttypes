from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.config import PROJECTNAME
from recensio.contenttypes.interfaces import IPerson
from zope.interface import implements


PersonSchema = schemata.ATContentTypeSchema.copy() + atapi.Schema(
    (
        atapi.StringField(
            "firstname",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"First name"),
            ),
        ),
        atapi.StringField(
            "lastname",
            required=True,
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"Last name"),
            ),
        ),
        atapi.StringField(
            "gnd",
            storage=atapi.AnnotationStorage(),
            widget=atapi.StringWidget(
                label=_(u"GND"),
            ),
        ),
    )
)


# PersonSchema["title"].storage = None
PersonSchema["title"].required = False
PersonSchema["title"].widget.condition = "python:False"

schemata.finalizeATCTSchema(PersonSchema, folderish=False)


class Person(base.ATCTMixin, atapi.BaseContent):
    implements(IPerson)

    meta_type = "Person"
    schema = PersonSchema

    firstname = atapi.ATFieldProperty("firstname")
    lastname = atapi.ATFieldProperty("lastname")
    gnd = atapi.ATFieldProperty("gnd")

    @property
    def title(self):
        names = [name for name in [self.lastname, self.firstname] if name]
        return ", ".join(names)

    @title.setter
    def title(self, value):
        return

    def getTitle(self):
        return self.title

    def setTitle(self, value):
        return


atapi.registerType(Person, PROJECTNAME)
