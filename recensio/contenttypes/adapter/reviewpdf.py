import logging
import os
import subprocess
import tempfile

from zope import interface
from zope import component

from recensio.contenttypes import interfaces
from recensio.contenttypes.helperutilities import RunSubprocess
from recensio.contenttypes.helperutilities import SubprocessException

logger = logging.getLogger('recensio.contenttypes.adapter.reviewpdf.py')

class ReviewPDF(object):
    """ Adapter to generate a cover image from a review's PDF data
    """
    interface.implements(interfaces.IReviewPDF)
    component.adapts(interfaces.IReview)

    def __init__(self, context):
        self.context = context

    def __str__(self):
        return '<recensio.contenttypes %s title=%s>' % (
            self.__class__.__name__, self.context.Title())
    __repr__ = __str__

    def _getAllPageImages(self, size=(320,452)):
        # Get the pdf
        pdf = self.context.get_review_pdf()
        if pdf:
            pdf_data = pdf["blob"].open().read()
        if not pdf or not pdf_data:
            return "%s has no pdf" %(
                self.context.absolute_url), None
        else:
            # Split the pdf, one file per page
            split_pdf_pages = RunSubprocess(
                "pdftk",
                output_params="burst output")
            split_pdf_pages.create_tmp_input(suffix=".pdf", data=pdf_data)
            split_pdf_pages.create_tmp_output_dir()
            split_pdf_pages.output_path = os.path.join(
                split_pdf_pages.tmp_output_dir,
                "%04d.pdf")
            split_pdf_pages.run()

            msg = ""
            if split_pdf_pages.errors != "":
                msg = ("Message from split_pdf_pages:"
                       "\n%s\n" % split_pdf_pages.errors)

            # Convert the pages to .gifs
            pdfs_to_images = RunSubprocess(
                "convert",
                input_params="-density 250",
                input_path=split_pdf_pages.tmp_output_dir+"/*.pdf",
                output_params="-resize %sx%s" % (size[0], size[1]))
            pdfs_to_images.output_path = os.path.join(
                split_pdf_pages.tmp_output_dir,
                "%04d.gif")
            pdfs_to_images.run()

            imgfiles = [gif for gif
                        in os.listdir(split_pdf_pages.tmp_output_dir)
                        if os.path.splitext(gif)[1] == '.gif']
            imgfiles.sort()

            pages = []
            for img in imgfiles:
                img = open(os.path.join(
                        split_pdf_pages.tmp_output_dir, img),
                             "r")
                img_data = img.read()
                pages.append(img_data)
                img.close()

            if pdfs_to_images.errors != "":
                msg = ("Message from pdfs_to_images:"
                       "\n%s\n" % pdfs_to_images.errors)

            # Remove temporary files
            split_pdf_pages.clean_up()
            pdfs_to_images.clean_up()

            return msg, pages

    def generatePageImages(self):
        """
        generate an image for each page of the pdf
        """
        result = ''
        i = 1
        pages = []
        status = 1
        try:
            result, pageimages = self._getAllPageImages((800,1131))
        except SubprocessException, e:
            result = "Missing converter? -> " + str(e)
            pageimages = None
        if result:
            logger.warn("popen: %s" % (result))
            if 'Error:' in result:
                status = 0
        if pageimages:
            setattr(self.context, 'pagePictures', pageimages)

        return status
