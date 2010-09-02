from plone.app.layout.viewlets import common
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class OAISuggestionsViewlet(common.ViewletBase):

    render = ViewPageTemplateFile('templates/oaisuggestions.pt')

    def show(self):
        # XXX Find a better solution for determining if we're in edit mode
        # or not
        elems = self.request.get('PATH_INFO', '').split('/')
        return elems[-1] == 'edit'
