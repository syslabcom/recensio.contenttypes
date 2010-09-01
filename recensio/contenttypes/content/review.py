# -*- CODING: utf-8 -*-
from os import fstat
from string import Formatter
import cStringIO as StringIO
import ho.pisa
import re
from DateTime import DateTime

from ZODB.blob import Blob
from zope.interface import implements
from zope.component import getUtility
from zope.i18n import translate

from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.CMFCore.utils import getToolByName
from Products.PortalTransforms.transforms.safe_html import scrubHTML
from zope.app.schema.vocabulary import IVocabularyFactory
from Products.Archetypes.utils import DisplayList

from plone.app.blob.utils import openBlob

from wc.pageturner.views import pdf2swf_subprocess
from wc.pageturner.settings import Settings
from wc.pageturner.interfaces import IPageTurnerSettings

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.helperutilities import SimpleZpt
from recensio.contenttypes.helperutilities import wvPDF
from recensio.contenttypes.interfaces.review import IReview

import logging
log = logging.getLogger('recensio.contentypes/content/review.py')

class BaseReview(base.ATCTMixin, atapi.BaseContent):
    implements(IReview)

    def listSupportedLanguages(self):
        util = getUtility(IVocabularyFactory,
            u"recensio.policy.vocabularies.available_content_languages")
        vocab = util(self)
        terms = [(x.value, x.title) for x in vocab]
        return DisplayList(terms)

    def setIsLicenceApproved(self, value):
        """
        The user needs to check the box every time they change the
        review to ensure they approve of the licence, so we don't want
        to save the value.
        """
        pass

    def get_citation_translation(self, msgid):
        """Returns a list of translation strings which can be used in citations

        This is partially to ensure that the relevant msgids are
        exported correctly when we generate the .pot file with
        i18nexport, and also to ensure that we notice if new msgids are
        needed by writing to the error log.
        """
        # Explicitly referring to the package message factory here is
        # enough for i18nextract to work
        citation_messages = [_("text_in"), _("text_presentation_of"),
            _("text_review_of"), _("text_pages")]
        if _(msgid) not in citation_messages:
            log.error("Translation for %s is not available" %msgid)
        # We've logged the error, but we will still return a
        # default translation
        return translate(_(msgid))

    def get_citation_dict(self, citation_template):
        """
        Parse the citation_template and using the create a dict the
        values to be substituted, including translation
        """
        formatter = Formatter()
        # Get the keys from the citation_template string i.e. words inside {}
        keys = set([i[1] for i in formatter.parse(citation_template)])
        if None in keys:
            keys.remove(None)
        citation_dict = {}
        for key in keys:
            # First translate the necessary strings
            if key.startswith("text_"):
                citation_dict[key] = self.get_citation_translation(key)
            elif key.startswith("get_"):
                citation_dict[key] = self[key]().decode("utf-8")
            else:
                value = ""
                try:
                    value = self.getField(key).getAccessor(self)()
                except Exception, e:
                    log.error("Error with citation %s" %e)
                if isinstance(value, tuple):
                    if value == ():
                        value = ""
                    else:
                        if isinstance(value[0], dict):
                            # DataGridField
                            value = ", ".join(value[0].values())
                        else:
                            value = ", ".join(value)
                if isinstance(value, str):
                    value = value.decode("utf-8")
                citation_dict[key] = value
        return citation_dict

    def get_citation_string(self):
        """
        If there's a custom one, return that, otherwise:
        Clean up the citation, removing empty sections
        """
        if self.customCitation:
            return scrubHTML(self.customCitation)
        else:
            citation_dict = self.get_citation_dict(self.citation_template)
            citation = self.citation_template.format(**citation_dict)
            # TODO replace all empty translation strings from text_*
            citation = citation.replace("Page(s) /", "")
            citation = re.sub("^[,.:]", "", citation)
            citation = re.sub(" [,.:]", "", citation)
            citation = re.sub("[,.:]\ *$", "", citation)
            citation = citation + "."
            return citation

    def update_generated_pdf(self):
        """
        If there isn't a custom pdf version of the review, generate
        the pdf from an MS Word .doc file. If there isn't an MS Word
        doc generate the pdf from the contents of the review text (html)

        We could implement odf to pdf too, but it sounds like we would
        need to run openoffice as a service:
        http://www.artofsolving.com/opensource/pyodconverter
        #1720
        """
        has_custom_pdf = hasattr(self, "pdf") and self.pdf.get_size() > 0
        if not has_custom_pdf:
            doc = self.getDoc()
            if doc:
                pdf_blob = Blob()
                pdf_blob.open("w").writelines(wvPDF(doc.data))
                self.generatedPdf = pdf_blob
            else:
                # Generate the pdf from the content of the review
                review = self.getReview()
                # Insert the review into a template
                pdf_template = SimpleZpt("../browser/templates/htmltopdf.pt")
                pdf_html = pdf_template(context={"review":review})
                # Generate the pdf file and save it as a blob
                pdf_blob = Blob()
                pdf_blob_writer = pdf_blob.open("w")
                pdf = ho.pisa.pisaDocument(
                    StringIO.StringIO(pdf_html.encode("UTF-8")),
                    pdf_blob_writer)
                pdf_blob_writer.close()
                if not pdf.err:
                    self.generatedPdf = pdf_blob

    def update_swf(self):
        """
        Update the swf version of the pdf version of the review
        """
        pdf_blob = self.get_review_pdf()
        if pdf_blob:
            settings = Settings(self)
            if DateTime(settings.last_updated) < \
                   DateTime(self.ModificationDate()):
                swf = None
                try:
                    pdf = openBlob(pdf_blob)
                    pdf2swf = pdf2swf_subprocess()
                    swf = pdf2swf.convert(pdf.read())
                    pdf.close()
                    log.info("Converted pdf for %s" %self.absolute_url())
                except Exception, e:
                    log.error("Error converting pdf for %s : %s" \
                         %(self.absolute_url(), e))
                if swf:
                    blob = Blob()
                    blob.open("w").writelines(swf)
                    settings.data = blob
                    settings.last_updated = DateTime().pCommonZ()
                    settings.successfully_converted = True

    def get_review_pdf(self):
        """
        Return the uploaded pdf or if that doesn't exist return the
        generatedPdf Blob object otherwise return None
        """
        pdf = None
        if hasattr(self, "pdf"):
            if self.pdf.get_size() > 0:
                pdf = self.pdf.blob
            elif hasattr(self, "generatedPdf"):
                generated_pdf = self.generatedPdf
                pdf_blob = openBlob(generated_pdf)
                size = fstat(pdf_blob.fileno()).st_size
                pdf_blob.close()
                if size > 0:
                    pdf = generated_pdf
        return pdf

    def getAllAuthorData(self):
        retval = []
        field_values = list(getattr(self, 'authors', [])) + \
                       list(getattr(self, 'referenceAuthors', []))
        for data in field_values:
            retval.append(('%s %s' % (data['firstname'], data['lastname'])).decode('utf-8').encode('utf-8'))
        review_author = ('%s %s %s' % (\
            getattr(self, 'reviewAuthorHonorific', '')
           ,getattr(self, 'reviewAuthorFirstname', '')
           ,getattr(self, 'reviewAuthorLastname', ''))).decode('utf-8').encode('utf-8')
        if review_author.strip():
            retval.append(review_author.strip())
        return retval

    def getAllAuthorDataFulltext(self):
        authors = " ".join(self.getAllAuthorData())
        return authors.decode('utf-8')

    def Language(self):
        """ Reviews are NOT translatable. As such, they must remain neutral """
        return ''
