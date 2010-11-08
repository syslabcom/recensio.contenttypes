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
        logger.debug("Calling external tools for page image generation:")
        try:
            mainpub = self.context
            pdf = mainpub.get_review_pdf()["blob"]
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
            logger.debug(cmd)
            _, _, res = os.popen3(cmd)
            result = res.read()
            if result:
                logger.warn("popen: %s" % (result))
            cmd = "convert %s -resize %ix%i %s" %(tmp_pdfin[1], size[0], size[1], tmp_gifin[1])
            logger.debug(cmd)
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

    def _getAllPageImages(self, size=(320,452), start=0, end=0):
        tmp_pdfin = tmp_pdfout = tmp_gifin = None
        result = ''
        pageimg = None
        pages = []
        logger.debug("Calling external tools for page image generation:")
        try:
            mainpub = self.context
            pdf = mainpub.get_review_pdf()["blob"]
            data = pdf.open().read()
            if not data:
                return 0
            tmp_pdfin = tempfile.mkdtemp()
            tmp_pdfout = tempfile.mkstemp(suffix='.pdf')
            tmp_pdfpart = tempfile.mkstemp(suffix='.pdf')
            fhout = open(tmp_pdfout[1], "w")
            fhout.write(data)
            fhout.close()
            tmp_prefix = os.path.join(tmp_pdfin, os.path.splitext(os.path.basename(tmp_pdfout[1]))[0])
            if start or end:
                if not start:
                    start = 1
                if end:
                    cmd = "pdftk %s cat %d-%d output %s" % (tmp_pdfout[1], start, end, tmp_pdfpart[1])
                else:
                    cmd = "pdftk %s cat %d-end output %s" % (tmp_pdfout[1], start, tmp_pdfpart[1])
                
                logger.debug(cmd)
                _, _, res = os.popen3(cmd)
                result = res.read()
                if result:
                    logger.warn("popen: %s" % (result))
            else:
                tmp_pdfpart = tmp_pdfout
            cmd = "pdftk %s burst output %s_%%04d.pdf" %(tmp_pdfpart[1], tmp_prefix)
            logger.debug(cmd)
            _, _, res = os.popen3(cmd)
            result = res.read()
            if result:
                logger.warn("popen: %s" % (result))
            cmd = "convert -density 400 %s_*.pdf -resize %ix%i %s_%%04d.gif" %(tmp_prefix, size[0], size[1], tmp_prefix)
            logger.debug(cmd)
            _, _, res = os.popen3(cmd)
            result2 = res.read()
            result += result2
            imgfiles = [gif for gif in os.listdir(tmp_pdfin) if os.path.splitext(gif)[1] == '.gif']
            imgfiles.sort()
            for img in imgfiles:
                fhimg = open(os.path.join(tmp_pdfin, img), "r")
                pageimg = fhimg.read()
                pages.append(pageimg)
                fhimg.close()
        except Exception, e:
            logger.warn("generateImage: Could not autoconvert! %s: %s" % (e.__class__.__name__, e) )

        # try to clean up
        if tmp_pdfin is not None:
            for img in [gif for gif in os.listdir(tmp_pdfin)]:
                try: os.remove(os.path.join(tmp_pdfin, img))
                except: pass
            try: os.removedirs(tmp_pdfin)
            except: pass
        if tmp_pdfout is not None:
            try: os.remove(tmp_pdfout[1])
            except: pass
            try: os.remove(tmp_pdfpart[1])
            except: pass
        
        return result, pages

    def generateImage(self):
        """
        try safely to generate the cover image if pdftk and imagemagick are present
        """
        coverPicture = self.context.getField('coverPicture')
        if not coverPicture:
            return 0
        result, coverdata = self._getPageImage(1)
        status = 1
        if result:
            logger.warn("popen: %s" % (result))
            if 'Error:' in result:
                status = 0
        #fhimg.seek(0)
        coverPicture.getMutator(self.context)(coverdata)

        return status

    def generatePageImages(self, start=0, end=0):
        """
        generate an image for each page of the pdf
        """
        result = ''
        i = 1
        pages = []
        status = 1
        result, pageimages = self._getAllPageImages((800,1131), start=start, end=end)
        if result:
            logger.warn("popen: %s" % (result))
            if 'Error:' in result:
                status = 0
        if pageimages:
            setattr(self.context, 'pagePictures', pageimages)

        return status

