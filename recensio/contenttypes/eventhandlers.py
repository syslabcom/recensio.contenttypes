import logging
from recensio.contenttypes import interfaces
from Products.Archetypes.interfaces.event import IObjectInitializedEvent

log = logging.getLogger('recensio.contenttypes/eventhandlers.py')

def review_pdf_updated_eventhandler(obj, evt):
    """Re-generate the pdf version of the review, then update the
    cover image of the pdf if necessary.
    """
    obj.update_generated_pdf()
    if obj.REQUEST and obj.REQUEST.get('pdf_file'):
        start = obj.REQUEST.get('pageStart', '0')
        end = obj.REQUEST.get('pageEnd', '0')
        try:
            start = int(start)
        except:
            start = 0
        try:
            end = int(end)
        except:
            end = 0
        
        interfaces.IReviewPDF(obj).generatePageImages(start=start, end=end)
        if not obj.REQUEST.get('coverPicture_file'):
            status = interfaces.IReviewPDF(obj).generateImage()
            if status == 0:
                log.warn('No cover picture could be generated for %s' % obj.getId())
