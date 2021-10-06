# -*- coding: utf-8 -*-
from plone import api
from plone.app.form._named import named_template_adapter
from plone.i18n.normalizer.interfaces import IURLNormalizer
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from recensio.contenttypes.interfaces import IPerson
from zope.component import getUtility


popup_template = named_template_adapter(ViewPageTemplateFile("templates/popup.pt"))


class GNDView(BrowserView):
    def __init__(self, *args, **kw):
        super(GNDView, self).__init__(*args, **kw)

    def _getPersonTitle(self, firstname=None, lastname=None):
        names = [name for name in [lastname, firstname] if name]
        title = ", ".join(names)
        return title

    def getContainer(self, title):
        gnd_folder = api.portal.get().get("gnd")
        normalizer = getUtility(IURLNormalizer)
        container_id = normalizer.normalize(title)[0].lower()
        if container_id not in gnd_folder:
            container = api.content.create(
                type="Folder",
                title=container_id,
                id=container_id,
                container=gnd_folder,
            )
            with api.env.adopt_roles(["Manager"]):
                api.user.revoke_roles(
                    obj=container, user=api.user.get_current(), roles=["Owner"]
                )
        else:
            container = gnd_folder[container_id]
        return container

    def createPerson(self, firstname=None, lastname=None):
        """Create a person with the provided lastname and optionally firstname."""
        if not (firstname or lastname):
            raise ValueError("Person must have a name")
        title = self._getPersonTitle(firstname=firstname, lastname=lastname)
        container = self.getContainer(title)
        person = api.content.create(
            type="Person",
            container=container,
            title=title,
            firstname=firstname,
            lastname=lastname,
            language="",
        )
        with api.env.adopt_roles(["Manager"]):
            api.user.revoke_roles(
                obj=person, user=api.user.get_current(), roles=["Owner"]
            )
        return person

    def get(self, gnd):
        catalog = api.portal.get_tool("portal_catalog")
        query = dict(gnd=gnd)
        results = catalog(query)
        if results:
            return results[0]

    def getByUID(self, uid):
        catalog = api.portal.get_tool("portal_catalog")
        query = dict(
            UID=uid,
            object_provides=IPerson.__identifier__,
        )
        res = catalog(query)
        if len(res) > 0:
            return res[0]

    def find(self, search_term=None, firstname=None, lastname=None, solr=True):
        if not search_term:
            search_term = self._getPersonTitle(firstname=firstname, lastname=lastname)
        catalog = api.portal.get_tool("portal_catalog")
        # XXX general interface, IGND?
        query = dict(
            SearchableText=search_term,
            object_provides=IPerson.__identifier__,
            sort_on="sortable_title",
        )
        if not solr:
            results = catalog.search(query)
        else:
            results = catalog(query)
        return results

    def list(self):
        catalog = api.portal.get_tool("portal_catalog")
        b_start = 0
        b_size = 500
        while True:
            brains = catalog(
                object_provides=IPerson.__identifier__,
                b_start=b_start,
                b_size=b_size,
                sort_on="sortable_title",
                fl=["UID", "Title", "path_string"],
            )
            for brain in brains[b_start : b_start + b_size]:
                yield brain
            b_start = b_start + b_size
            if b_start >= len(brains):
                break

    def count(self):
        catalog = api.portal.get_tool("portal_catalog")
        return len(catalog(portal_type="Person", b_size=0))
