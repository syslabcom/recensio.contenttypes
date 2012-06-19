import logging
from recensio.contenttypes import interfaces
from Products.Archetypes.interfaces.event import IObjectInitializedEvent
from Products.CMFCore.utils import getToolByName

log = logging.getLogger('recensio.contenttypes/eventhandlers.py')

def review_pdf_updated_eventhandler(obj, evt):
    """Re-generate the pdf version of the review, then update the
    cover image of the pdf if necessary.
    """
    if not obj.REQUEST.get('pdf_file'):
        obj.update_generated_pdf()

    interfaces.IReviewPDF(obj).generatePageImages()

def notify_reference_authors_if_changed(obj, evt):
    """Check if reference authors have been changed, if yes: notify added ones"""
    rtool = getToolByName(obj, 'portal_repository')
    wftool = getToolByName(obj, 'portal_workflow')

    if not wftool.getInfoFor(obj, 'review_state') == 'published':
        return

    skip = []
    try:
        history = rtool.getHistory(obj)
        if len(history) > 1:
            prev_version = history[0].object
            for refauth in obj.referenceAuthors:
                if refauth['email'] in map(lambda x: x['email'], prev_version.referenceAuthors):
                    mail = refauth.get('email', None)
                    if mail:
                        log.debug('skipping %s' % mail)
                        skip.append(mail)
    except:
        # XXX Temporary only
        log.warning('No previous object version found. Not comparing reference authors')
    log.warning("Here are the ignored users: %s" % str(skip))

    notify_view = obj.restrictedTraverse('@@mail_new_presentation')
    if notify_view:
        notify_view(skip_addrs=skip)
