import logging

log = logging.getLogger('recensio.contenttypes/eventhandlers.py')

def review_pdf_updated_eventhandler(obj, evt):
    """
    Re-generate the pdf version of the review, then update the swf
    version of the pdf.
    """
    obj.update_generated_pdf()
    obj.update_swf()
