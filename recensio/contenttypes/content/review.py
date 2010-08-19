# -*- coding: utf-8 -*-
import re
from string import Formatter
from os import fstat

from zope.interface import implements

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.PortalTransforms.transforms.safe_html import scrubHTML

from plone.app.blob.utils import openBlob

from recensio.contenttypes.interfaces.review import IReview

import logging
log = logging.getLogger('recensio.contentypes/content/review.py')

class BaseReview(base.ATCTContent):
    implements(IReview)

    def listSupportedLanguages(self):
        return self.portal_languages.listSupportedLanguages()

    def setIsLicenceApproved(self, value):
        """
        The user needs to check the box every time they change the
        review to ensure they approve of the licence, so we don't want
        to save the value.
        """
        pass

    def translate(self, msgid):
        return msgid

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
                citation_dict[key] = self.translate(key)
            elif key.startswith("get_"):
                citation_dict[key] = self[key]().decode("utf-8")
            else:
                value = ""
                try:
                    value = self.getField(key).getAccessor(self)()
                except Exception, e:
                    log.error("Error with citation %s" ,e)
                    import pdb; pdb.set_trace()
                if isinstance(value, tuple):
                    if value == ():
                        value = ""
                    else:
                        if isinstance(value[0], dict):
                            # DataGridField
                            value = ", ".join(value[0])
                        else:
                            value = ", ".join(value)
                citation_dict[key] = value.decode("utf-8")
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
        relevant_fields = ['authors', 'reviewAuthorEmail', \
    'reviewAuthorFirstname', 'reviewAuthorLastname', 'reviewAuthorHonorific', 
    'referenceAuthors', 'creators', 'contributors']
        retval = []
        for field_name in relevant_fields:
            field_value = getattr(self, field_name, None)
            if field_value:
                retval.extend(self._getAllAuthorData(field_value))

        return retval

    def _getAllAuthorData(self, data):
        retval = []
        if hasattr(data, 'values'):
            for value in data.values():
                retval.extend(self._getAllAuthorData(value))
        elif hasattr(data, '__iter__'):
            for value in data:
                retval.extend(self._getAllAuthorData(value))
        else:
            if isinstance(data, str):
                data = data.decode('utf-8')
            retval = [data]
        return retval
