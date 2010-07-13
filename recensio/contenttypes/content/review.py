# -*- coding: utf-8 -*-
import re
from string import Formatter

from zope.interface import implements

from Products.ATContentTypes.content import base

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
                citation_dict[key] = self[key]()
            else:
                value = ""
                try:
                    value = self.getField(key).getAccessor(self)()
                except exception, e:
                    log.error("Error with citation %s" ,e)
                if isinstance(value, tuple):
                    if isinstance(value[0], dict):
                        # DataGridField
                        value = ", ".join(value[0])
                    else:
                        value = ", ".join(value)
                citation_dict[key] = value.decode("utf-8")
        return citation_dict

    def get_citation_string(self):
        """
        Clean up the citation, removing empty sections
        """
        citation_dict = self.get_citation_dict(self.citation_template)
        citation = self.citation_template.format(**citation_dict)
        citation = citation.replace("Page(s) /", "")
        citation = re.sub("^[,.:]", "", citation)
        citation = re.sub(" [,.:]", "", citation)
        citation = re.sub("[,.:]\ *$", "", citation)
        citation = citation + "."
        return citation
