from AccessControl import ClassSecurityInfo
from Acquisition import aq_inner
from archetypes.referencebrowserwidget import ReferenceBrowserWidget
from archetypes.referencebrowserwidget import utils
from archetypes.referencebrowserwidget.browser.view import QueryCatalogView
from archetypes.referencebrowserwidget.browser.view import ReferenceBrowserPopup
from plone import api
from Products.Archetypes import atapi
from Products.Archetypes.Registry import registerPropertyType
from Products.Archetypes.Registry import registerWidget
from Products.CMFPlone.PloneBatch import Batch
from zope.component import getMultiAdapter
import re


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


class GNDQueryCatalogView(QueryCatalogView):

    def __call__(self, show_all=0,
                 quote_logic=0,
                 quote_logic_indexes=['SearchableText'],
                 search_catalog=None):

        results = []
        catalog = utils.getSearchCatalog(aq_inner(self.context),
                                         search_catalog)
        indexes = catalog.indexes() + quote_logic_indexes
        query = {}
        show_query = show_all
        second_pass = {}

        purl_tool = api.portal.get_tool('portal_url')
        portal_path = purl_tool.getPortalPath()

        for k, v in self.request.items():
            if v and k in indexes:
                if type(v) == str and v.strip().lower().startswith('path:'):
                    # Searching for exact path enabled! This will return the
                    # item on the specified path and all items in its subtree
                    # NOTE: Multiple spaces, slashes and/or a trailing slash in
                    # the path, while easily overlooked by users, might cause
                    # no results to be found. Let's take care of this for the
                    # convenience of the user. Besides, we need to strip
                    # 'path:' from the path string.
                    path = re.sub("/{2,}", "/", v.strip()[5:]).rstrip("/")

                    if not path.startswith("/"):
                        path = "/" + path

                    # Since we might be in a virtual-hosting environment, we
                    # need to prepend the portal path if not present yet
                    if not path.startswith(portal_path):
                        path = portal_path + path

                    d = {"path": {"query": path}}
                else:
                    if quote_logic and k in quote_logic_indexes:
                        v = utils.quotequery(v)
                    d = {k: v}
                query.update(d)
                show_query = 1

            elif k.endswith('_usage'):
                key = k[:-6]
                param, value = v.split(':')
                second_pass[key] = {param: value}
            elif k in ('sort_on', 'sort_order', 'sort_limit'):
                query.update({k: v})
            elif k in ("fq", "fl", "facet", "b_start", "b_size") or k.startswith("facet."):
                query[k] = v

        for k, v in second_pass.items():
            qs = query.get(k)
            if qs is None:
                continue
            query[k] = q = {'query': qs}
            q.update(v)

# doesn't normal call catalog unless some field has been queried
# against. if you want to call the catalog _regardless_ of whether
# any items were found, then you can pass show_all=1.

        if show_query:
            results = catalog(**query)

        return results


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
        b_size = int(self.request.get('b_size', 20))
        b_start = int(self.request.get('b_start', 0))
        if "b_size" not in self.request.form:
            self.request.form["b_size"] = b_size
        if "b_start" not in self.request.form:
            self.request.form["b_start"] = b_start
        if "path" not in self.request.form:
            self.request.form["path"] = "/".join(api.portal.get().getPhysicalPath())

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

        return Batch(self._prepareResults(result), b_size, b_start, orphan=1)

    def _prepareResults(self, result):
        items_with_info = []
        for item in result:
            if not item:
                items_with_info.append(None)
                continue
            browse = self.isBrowsable(item)
            ref = self.isReferencable(item)
            if self.allowed_types:
                # we only show allowed_types and objects needed for browsing
                if not (ref or browse or not self.isNotSelf(item)):
                    continue

            items_with_info.append(dict(
                item=item,
                browsable=browse,
                referenceable=ref,
                ))

        return items_with_info


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
