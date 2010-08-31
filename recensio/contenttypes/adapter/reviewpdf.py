import logging
import os
import tempfile
from zope import interface
from zope import component
from recensio.contenttypes import interfaces

logger = logging.getLogger('recensio.contenttypes.adapter.reviewpdf.py')

class ReviewPDF(object):
    """ Adapter to generate a cover image from a review's PDF data
    """
    interface.implements(interfaces.IReviewPDF)
    component.adapts(interfaces.IReview)

    def __init__(self, context):
        self.context = context

    def __str__(self):
        return '<recensio.contenttypes %s title=%s>' % (self.__class__.__name__, self.context.Title())
    __repr__ = __str__

    def generateImage(self):
        """
        try safely to generate the cover image if pdftk and imagemagick are present
        """
        tmp_pdfin = tmp_pdfout = tmp_gifin = None
        try:
            mainpub = self.context
            pdf = mainpub.get_review_pdf()
            data = pdf.open().read()
            if not data:
                return 0
            tmp_pdfin = tempfile.mkstemp(suffix='.pdf')
            tmp_pdfout = tempfile.mkstemp(suffix='.pdf')
            tmp_gifin = tempfile.mkstemp(suffix='.gif')
            fhout = open(tmp_pdfout[1], "w")
            fhimg = open(tmp_gifin[1], "r")
            fhout.write(data)
            fhout.seek(0)
            cmd = "pdftk %s cat 1 output %s" %(tmp_pdfout[1], tmp_pdfin[1])
            logger.info(cmd)
            res = os.popen(cmd)
            result = res.read()
            if result:
                logger.warn("popen-1: %s" % (result))
            cmd = "convert %s -resize 320x452 %s" %(tmp_pdfin[1], tmp_gifin[1])
            res = os.popen(cmd)
            result = res.read()
            if result:
                logger.warn("popen-2: %s" % (result))
            #fhimg.seek(0)
            coverdata = fhimg.read()
            self.context.getField('coverPicture').getMutator(self.context)(coverdata)
            status = 1
        except Exception, e:
            logger.warn("generateImage: Could not autoconvert! %s: %s" % (e.__class__.__name__, e) )
            status = 0

        # try to clean up
        if tmp_pdfin is not None:
            try: os.remove(tmp_pdfin[1])
            except: pass
        if tmp_pdfout is not None:
            try: os.remove(tmp_pdfout[1])
            except: pass
        if tmp_gifin is not None:
            try: os.remove(tmp_gifin[1])
            except: pass

        return status


