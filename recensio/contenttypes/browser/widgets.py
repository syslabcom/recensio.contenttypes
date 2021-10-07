from AccessControl import ClassSecurityInfo
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from archetypes.referencebrowserwidget.browser.view import ReferenceBrowserPopup
from Products.Archetypes import atapi
from Products.Archetypes.Registry import registerPropertyType
from Products.Archetypes.Registry import registerWidget
from Products.CMFPlone.PloneBatch import Batch
from zope.component import getMultiAdapter


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


class GNDReferenceBrowserPopup(ReferenceBrowserPopup):

    @property
    def wildcardable_indexes(self):
        return super(GNDReferenceBrowserPopup, self).wildcardable_indexes + ["SearchableText"]

    def getResult(self):
        assert self._updated
        result = []

        # turn search string into a wildcard search if relevant, so if
        # wild_card_search is True and if current index is a ZCTextIndex
        if self.search_text and self.widget.use_wildcard_search and self.search_index in self.wildcardable_indexes:
            # only append a '*' if not already ending with a '*' and not surrounded
            # by " ", this is the case if user want to search exact match
            if not self.search_text.endswith('*') and \
               not (self.search_text.startswith('"') and self.search_text.endswith('"')):
                self.request[self.search_index] = "{0}*".format(self.search_text)

        qc = getMultiAdapter((self.context, self.request),
                             name='refbrowser_querycatalog')
        if self.widget.show_results_without_query or self.search_text:
            result = (self.widget.show_results_without_query or
                self.search_text) and \
                qc(search_catalog=self.widget.search_catalog)

            self.has_queryresults = bool(result)

        elif self.widget.allow_browse:
            ploneview = getMultiAdapter((self.context, self.request),
                                        name="plone")
            folder = ploneview.getCurrentFolder()
            self.request.form['path'] = {
                'query': '/'.join(folder.getPhysicalPath()),
                'depth': 1}
            self.request.form['portal_type'] = []
            if 'sort_on' in self.widget.base_query:
                self.request.form['sort_on'] = self.widget.base_query['sort_on']
            else:
                self.request.form['sort_on'] = 'getObjPositionInParent'

            result = qc(search_catalog=self.widget.search_catalog)

        else:
            result = []

        b_size = int(self.request.get('b_size', 20))
        b_start = int(self.request.get('b_start', 0))
        return Batch(self._prepareResults(result), b_size, b_start, orphan=1)


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
