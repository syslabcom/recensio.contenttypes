from zope.component import getMultiAdapter
from zope.interface import implements
from zope.formlib import form

from plone.memoize.instance import memoize
from plone.memoize.compress import xhtml_compress
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider

from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from recensio.policy import recensioMessageFactory as _
from recensio.contenttypes.adapter.parentgetter import ParentGetter

class ICompletePdfsPortlet(IPortletDataProvider):
    pass

class Assignment(base.Assignment):
    implements(ICompletePdfsPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        return _(u"Complete PDFs")

class CompletePdfsPortlet(base.Renderer):
    _template = ViewPageTemplateFile('templates/completepdfs.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        context = aq_inner(self.context)
        plone_tools = getMultiAdapter((context, self.request), name=u'plone_tools')
        self.catalog = plone_tools.catalog()        

    def render(self):
        return xhtml_compress(self._template())

    def _maketitle(self, ob):
        vol = getattr(ParentGetter(ob).get_parent_object_of_type("Volume"), 'title', None)
        issue = getattr(ParentGetter(ob).get_parent_object_of_type("Issue"), 'title', None)
        return "%s - %s" % (vol, issue)

    def _data(self):
        results = self.catalog(path='/'.join(self.context.getPhysicalPath()[:-1]), 
                               Title='issue.pdf',
                               sort_on='effective')
        objs = [x.getObject() for x in results[:1]]
        info = [dict(title=self._maketitle(ob),
                     link=ob.absolute_url()) 
                     for ob in objs]
        return info

    def complete_pdfs(self):
        return self._data()

    @property
    def available(self):
        return len(self.complete_pdfs()) and self.context.portal_type == 'Document' and ParentGetter(self.context).get_parent_object_of_type("Publication")

class AddForm(base.AddForm):
    form_fields = form.Fields(ICompletePdfsPortlet)
    label = _(u"Add Complete PDFs Portlet")
    description = _(u"This portlet displays complete issue PDFs.")

    def create(self, data):
        return Assignment()

class EditForm(base.EditForm):
    form_fields = form.Fields(ICompletePdfsPortlet)
    label = _(u"Edit Complete PDFs Portlet")
    description = _(u"This portlet displays complete issue PDFs.")