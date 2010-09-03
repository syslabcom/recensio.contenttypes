import logging
from recensio.contenttypes import interfaces

log = logging.getLogger('recensio.contenttypes/eventhandlers.py')

def review_pdf_updated_eventhandler(obj, evt):
    """
    Re-generate the pdf version of the review, then update the swf
    version and, if necessary, cover image of the pdf.
    """
    obj.update_generated_pdf()
    obj.update_swf()
    if obj.REQUEST.get('pdf_file'):
        interfaces.IReviewPDF(obj).generatePageImages()
        if not obj.REQUEST.get('coverPicture_file'):
            interfaces.IReviewPDF(obj).generateImage()
