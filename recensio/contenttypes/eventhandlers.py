import logging
from recensio.contenttypes import interfaces

log = logging.getLogger('recensio.contenttypes/eventhandlers.py')

def review_pdf_updated_eventhandler(obj, evt):
    """
    Re-generate the pdf version of the review, then update the swf
    version and cover image of the pdf.
    """
    obj.update_generated_pdf()
    obj.update_swf()
    interfaces.IReviewPDF(obj).generateImage()
