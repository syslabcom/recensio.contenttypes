from AccessControl import ClassSecurityInfo
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from Products.Archetypes import atapi
from Products.Archetypes.Registry import registerPropertyType
from Products.Archetypes.Registry import registerWidget


class StringFallbackWidget(atapi.StringWidget):
    _properties = atapi.StringWidget._properties.copy()
    _properties.update(
        {
            "label_fallback_value": "Fallback",
            "label_fallback_unavailable": "N/A",
            "macro": "widget_string_fallback",
        }
    )

    security = ClassSecurityInfo()

    security.declarePublic("process_form")

    def process_form(
        self,
        instance,
        field,
        form,
        empty_marker=None,
        emptyReturnsMarker=False,
        validating=True,
    ):
        value = form.get(field.getName(), empty_marker)
        if value == "":
            value = form.get(field.getName() + "_fallback", empty_marker)
        if value is empty_marker:
            return empty_marker
        if emptyReturnsMarker and value == "":
            return empty_marker
        return value, {}


registerWidget(
    StringFallbackWidget,
    title="String with Fallback",
    description=("Accepts a line of text. Falls back to default if " "empty."),
    used_for=("Products.Archetypes.Field.StringField",),
)

registerPropertyType("label_fallback_value", "string", StringFallbackWidget)
registerPropertyType("label_fallback_unavailable", "string", StringFallbackWidget)


class GNDReferenceBrowserWidget(ReferenceBrowserWidget):
    _properties = ReferenceBrowserWidget._properties.copy()
    _properties.update(
        {
            "helper_js": (
                "referencebrowser.js",
                "referencebrowser-gnd.js",
            ),
            "popup_name": "gnd_popup",
            "allow_browse": 0,
            "allow_create": 1,
            "allow_sorting": 1,
            "base_query": {"sort_on": "sortable_title"},
        }
    )

    security = ClassSecurityInfo()


registerWidget(
    GNDReferenceBrowserWidget,
    title="GND aware reference browser",
    description=("Pick a GND entity for use in a reference field"),
    used_for=("Products.Archetypes.Field.ReferenceField",),
)
