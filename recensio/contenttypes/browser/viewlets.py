from plone.app.layout.viewlets import common
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class OAISuggestionsViewlet(common.ViewletBase):

    render = ViewPageTemplateFile("templates/oaisuggestions.pt")

    def show(self):
        # XXX Find a better solution for determining if we're in edit mode
        # or not
        elems = self.request.get("PATH_INFO", "").split("/")
        return elems[-1] == "edit"

    def getDdcPlace(self):
        voctool = getToolByName(self.context, "portal_vocabularies")
        region_values_bsb = voctool.get("region_values_bsb")

        if region_values_bsb:
            return region_values_bsb.getDisplayList(region_values_bsb).items()
        region_values = voctool.get("region_values")

        if region_values:
            return region_values.getDisplayList(region_values).items()

        return []
