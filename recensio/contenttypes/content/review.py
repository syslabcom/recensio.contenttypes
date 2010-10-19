# -*- CODING: utf-8 -*-
""" BaseReview is a base class all Recensio Review and Presentation
content types inherit from.
"""
from DateTime import DateTime
from os import fstat
from string import Formatter
import cStringIO as StringIO
import logging
import re

import ho.pisa

import Acquisition
from ZODB.blob import Blob
from zope.app.component.hooks import getSite
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implements

from plone.app.blob.utils import openBlob

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.Archetypes import atapi
from Products.Archetypes.utils import DisplayList
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.Portal import PloneSite
from Products.PortalTransforms.transforms.safe_html import scrubHTML

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.helperutilities import SimpleZpt
from recensio.contenttypes.helperutilities import wvPDF
from recensio.contenttypes.interfaces.review import IReview


log = logging.getLogger('recensio.contentypes/content/review.py')

class BaseReview(base.ATCTMixin, HistoryAwareMixin, atapi.BaseContent):
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

    def get_citation_translation(self, msgid, language):
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
        return translate(_(msgid), target_language=language)

    def get_citation_dict(self, citation_template, language=''):
        """
        Parse the citation_template and using the create a dict the
        values to be substituted, including translation
        """
        if not language:
            plt = getToolByName(self, 'portal_languages')
            language = plt.getPreferredLanguage()
        formatter = Formatter()
        # Get the keys from the citation_template string i.e. words inside {}
        keys = set([i[1] for i in formatter.parse(citation_template)])
        if None in keys:
            keys.remove(None)
        citation_dict = {}
        for key in keys:
            # First translate the necessary strings
            if key.startswith("text_"):
                citation_dict[key] = self.get_citation_translation(key, language)
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

    def get_citation_string(self, language=''):
        """
        If there's a custom one, return that, otherwise:
        Clean up the citation, removing empty sections
        """
        if self.get("customCitation"):
            return scrubHTML(self.customCitation)
        else:
            citation_dict = self.get_citation_dict(self.citation_template,
                                                   language)
            citation = self.citation_template.format(**citation_dict)
            # TODO replace all empty translation strings from text_*
            citation = citation.replace("Page(s) /", "")
            citation = re.sub("^[,.:]", "", citation)
            # In French, we have a space before the colon, so don't remove it
            citation = re.sub(" [,.]", "", citation)
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
            doc = None
            if hasattr(self, "doc"):
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

    def get_review_pdf(self):
        """ Return the uploaded pdf if that doesn't exist return the
        generatedPdf Blob object otherwise return None

        Also return the size since it is not easy to get this from the
        blob directly
        """
        pdf = {}
        if hasattr(self, "pdf"):
            size = self.pdf.get_size()
            if size > 0:
                pdf["size"] = size
                pdf["blob"] = self.pdf.blob
        elif hasattr(self, "generatedPdf"):
            generated_pdf = self.generatedPdf
            pdf_blob = openBlob(generated_pdf)
            size = fstat(pdf_blob.fileno()).st_size
            pdf_blob.close()
            if size > 0:
                pdf["size"] = size
                pdf["blob"] = generated_pdf
        if pdf == {}:
            return None
        else:
            return pdf

    def get_page_image(self, no=1):
        """
        Return a page of the review text
        """
        images = getattr(self, 'pagePictures', None)
        if images is None:
            return None
        if no > len(images):
            no = 0
        self.REQUEST.RESPONSE.setHeader('Content-Type', 'image/gif')
        self.REQUEST.RESPONSE.setHeader('Content-Length', len(images[no - 1]))
        
        return images[no - 1]

    def get_no_pages(self):
        """
        Return the number of pages that are stored as images
        See get_page_image()
        """
        pagePictures = getattr(self, 'pagePictures', None)
        return pagePictures and len(pagePictures) or 0


    def getAllAuthorData(self):
        retval = []
        field_values = list(getattr(self, 'authors', [])) + \
                       list(getattr(self, 'referenceAuthors', []))
        for data in field_values:
            retval.append(('%s %s' % (data['firstname'], data['lastname'])).decode('utf-8').encode('utf-8'))
        try:
           review_author = ('%s %s' % (\
               self.reviewAuthorFirstname
              ,self.reviewAuthorLastname
              )).decode('utf-8').encode('utf-8')
           if review_author.strip():
               retval.append(review_author.strip())
        except AttributeError:
            pass
        return retval

    def getAllAuthorDataFulltext(self):
        authors = " ".join(self.getAllAuthorData())
        return authors.decode('utf-8')

    def Language(self):
        """ Reviews are NOT translatable. As such, they must remain neutral """
        return ''

    def get_title_from_parent_of_type(self, meta_type):
        """
        Return the title of the first object of a particular type
        which is a parent of the current object.
        """
        obj = self.get_parent_object_of_type(meta_type)
        if obj:
            return obj.Title()
        return ''

    def get_parent_object_of_type(self, meta_type):
        """ Return the object of a particular type which is
        the parent of the current object."""
        obj = Acquisition.aq_inner(self)
        while not isinstance(obj, PloneSite):
            obj = Acquisition.aq_parent(obj)
            if obj.meta_type == meta_type:
                return obj
        return None

    # The following get_user_... methods are used as default_methods
    # for various fields
    def get_user_property(self, property):
        portal = getSite()
        pm = portal.portal_membership
        user = pm.getAuthenticatedMember()
        return user.getProperty(property)

    def get_user_lastname(self):
        return self.get_user_property("lastname")

    def get_user_firstname(self):
        return self.get_user_property("firstname")

    def get_user_email(self):
        return self.get_user_property("email")

    def get_user_home_page(self):
        return self.get_user_property("home_page")
