from AccessControl import ClassSecurityInfo
from Products.Archetypes import atapi
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Registry import registerPropertyType


class StringFallbackWidget(atapi.StringWidget):
    _properties = atapi.StringWidget._properties.copy()
    _properties.update({
        'label_fallback_value': 'Fallback',
        'macro': 'widget_string_fallback',
    })

    security = ClassSecurityInfo()

    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        value = form.get(field.getName(), empty_marker)
        if value == '':
            value = form.get(field.getName() + '_fallback', empty_marker)
        if value is empty_marker:
            return empty_marker
        if emptyReturnsMarker and value == '':
            return empty_marker
        return value, {}

registerWidget(StringFallbackWidget,
               title='String with Fallback',
               description=('Accepts a line of text. Falls back to default if '
                            'empty.'),
               used_for=('Products.Archetypes.Field.StringField',)
               )

registerPropertyType('label_fallback_value', 'string', StringFallbackWidget)
