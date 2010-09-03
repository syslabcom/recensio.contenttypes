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

    def _getPageImage(self, n, size=(320,452)):
        tmp_pdfin = tmp_pdfout = tmp_gifin = None
        result = ''
        pageimg = None
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
            fhout.close()
            cmd = "pdftk %s cat %i output %s" %(tmp_pdfout[1], n, tmp_pdfin[1])
            logger.info(cmd)
            _, _, res = os.popen3(cmd)
            result = res.read()
            if result:
                logger.warn("popen: %s" % (result))
            cmd = "convert %s -resize %ix%i %s" %(tmp_pdfin[1], size[0], size[1], tmp_gifin[1])
            _, _, res = os.popen3(cmd)
            result2 = res.read()
            result += result2
            pageimg = fhimg.read()
            fhimg.close()
        except Exception, e:
            logger.warn("generateImage: Could not autoconvert! %s: %s" % (e.__class__.__name__, e) )

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
        
        return result, pageimg


    def generateImage(self):
        """
        try safely to generate the cover image if pdftk and imagemagick are present
        """
        result, coverdata = self._getPageImage(1)
        status = 1
        if result:
            logger.warn("popen: %s" % (result))
            if 'Error:' in result:
                status = 0
        #fhimg.seek(0)
        self.context.getField('coverPicture').getMutator(self.context)(coverdata)

        return status

    def generatePageImages(self):
        """
        generate an image for each page of the pdf
        """
        result = ''
        i = 1
        pages = []
        status = 1
        while not 'Error:' in result and i < 12:
            result, pageimg = self._getPageImage(i, (800,1131))
            if result and not 'Page number:' in result:
                logger.warn("popen: %s" % (result))
                if 'Error:' in result:
                    status = 0
            if pageimg:
                pages.append(pageimg)
            i = i + 1
        if pages:
            setattr(self.context, 'pagePictures', pages)

        return status

