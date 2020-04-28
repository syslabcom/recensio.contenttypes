import datetime
import glob
import logging
import os
import subprocess
import tempfile

import pytz
from plone.app.async.interfaces import IAsyncService
from plone.app.blob.field import ImageField
from recensio.contenttypes import interfaces
from recensio.contenttypes.helperutilities import RunSubprocess
from recensio.contenttypes.helperutilities import SubprocessException
from zope import component
from zope import interface

logger = logging.getLogger("recensio.contenttypes.adapter.reviewpdf.py")


def _getAllPageImages(context, size=(320, 452)):
    """ Generate the preview images for a pdf """
    pdf = context.get_review_pdf()
    #    import pdb; pdb.set_trace()
    if pdf:
        pdf_data = pdf["blob"].open().read()
    if not pdf or not pdf_data:
        return "%s has no pdf" % (context.absolute_url()), None
    else:
        # Split the pdf, one file per page
        try:
            split_pdf_pages = RunSubprocess("pdftk", output_params="burst output")
        except SubprocessException, e:
            return e
        split_pdf_pages.create_tmp_input(suffix=".pdf", data=pdf_data)
        split_pdf_pages.create_tmp_output_dir()
        split_pdf_pages.output_path = os.path.join(
            split_pdf_pages.tmp_output_dir, "%04d.pdf"
        )
        split_pdf_pages.run()

        msg = tuple()
        if split_pdf_pages.errors != "":
            msg += ("Message from split_pdf_pages:" "\n%s\n" % split_pdf_pages.errors,)

        # Convert the pages to .gifs
        # rewritten to have one converter step per page as we have seen process
        # sizes larger than 2GB for 60 pages in a batch
        for filename in glob.glob(split_pdf_pages.tmp_output_dir + "/*.pdf"):
            pdf_to_image = RunSubprocess(
                "convert",
                input_params="-density 250",
                input_path=filename,
                output_params="-resize %sx%s -background white -flatten"
                % (size[0], size[1]),
            )
            outputname = ".".join(filename.split("/")[-1].split(".")[:-1]) + ".gif"
            pdf_to_image.output_path = os.path.join(
                split_pdf_pages.tmp_output_dir, outputname
            )
            pdf_to_image.run()
            if pdf_to_image.errors != "":
                msg += ("Message from pdfs_to_images:" "\n%s\n" % pdf_to_image.errors,)

            pdf_to_image.clean_up()

        imgfiles = [
            gif
            for gif in os.listdir(split_pdf_pages.tmp_output_dir)
            if os.path.splitext(gif)[1] == ".gif"
        ]
        imgfiles.sort()

        pages = []
        for img in imgfiles:
            img = open(os.path.join(split_pdf_pages.tmp_output_dir, img), "r")
            img_data = img.read()
            pages.append(img_data)
            img.close()

        # Remove temporary files
        split_pdf_pages.clean_up()

        if pages:
            imgfields = []
            for img in pages:
                IF = ImageField()
                IF.set(context, img)
                imgfields.append(IF)
            setattr(context, "pagePictures", imgfields)

        return msg or "Successfully converted %s pages" % len(pages)


class ReviewPDF(object):
    """ Adapter to generate a cover image from a review's PDF data
    """

    interface.implements(interfaces.IReviewPDF)
    component.adapts(interfaces.IReview)

    def __init__(self, context):
        self.context = context

    def __str__(self):
        return "<recensio.contenttypes %s title=%s>" % (
            self.__class__.__name__,
            self.context.Title(),
        )

    __repr__ = __str__

    def generatePageImages(self, later=True):
        """
        generate an image for each page of the pdf
        """
        result = ""
        status = 1
        # make this asyncronous
        async = component.getUtility(IAsyncService)
        async_args = (self.context, (800, 1131))
        when = datetime.datetime.now(pytz.UTC) + datetime.timedelta(seconds=600)
        try:
            if later:
                async.queueJobWithDelay(None, when, _getAllPageImages, *async_args)
            else:
                apply(_getAllPageImages, async_args)
        except (component.ComponentLookupError, KeyError):
            logger.error("Could not setup async job, running synchronous")
            apply(_getAllPageImages, async_args)
        #        try:
        #            result, pageimages = self._getAllPageImages((800,1131))
        #        except SubprocessException, e:
        #            result = "Missing converter? -> " + str(e)
        #            pageimages = None
        if result:
            logger.warn("popen: %s" % (result))
            if "Error:" in result:
                status = 0
        #        if pageimages:
        #            imgfields = []
        #            for img in pageimages:
        #                IF = ImageField()
        #                IF.set(self.context, img)
        #                imgfields.append(IF)
        #            setattr(self.context, 'pagePictures', imgfields)
        return status
