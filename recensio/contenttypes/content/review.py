# -*- coding: utf-8 -*-
import re

from zope.interface import implements
from zope.pagetemplate.pagetemplatefile import PageTemplateFile

from Products.ATContentTypes.content import base

from recensio.contenttypes.interfaces.review import IReview

import logging
log = logging.getLogger('recensio.contentypes/content/review.py')

class BaseReview(base.ATCTContent):
    implements(IReview)

    # Override the template for each content type
    citation_template = u"%(reviewAuthor)s, review of: %(authors)s,"+\
                        u"%(title)s%(titel_divider)s%(subtitle)s, "+\
                        u"%(placeOfPublication)s: %(publisher)s "+\
                        u"%(yearOfPublication)s, in: %(series)s, "+\
                        u"%(seriesVol)s, p. %(pages)s, %(absolute_url)s"

    # "Review einer Monographie": u"%(reviewAuthor)s, review of:
    # %(authors)s, %(title)s%(titel_divider)s%(subtitle)s,
    # %(placeOfPublication)s: %(publisher)s %(yearOfPublication)s, in:
    # %(series)s, %(seriesVol)s, p. %(pages)s, %(absolute_url)s",
    # "Review einer Zeitschrift": u"%(reviewAuthor)s, review of:
    # %(shortnameJournal)s, %(volume)s, %(number)s,
    # (%(yearOfPublication)s/%(officialYearOfPublication)s,
    # %(absolute_url)s", "Praesentationen von Monographien":
    # u"%(authors)s, presentation of: %(authors)s,
    # %(title)s%(titel_divider)s%(subtitle)s, %(placeOfPublication)s:
    # %(publisher)s %(yearOfPublication)s, %(absolute_url)s",


    def listSupportedLanguages(self):
        return self.portal_languages.listSupportedLanguages()

    def setIsLicenceApproved(self, value):
        """
        The user needs to check the box every time they change the
        review to ensure they approve of the licence, so we don't want
        to save the value.
        """
        pass

    def get_citation_string(review):
        metadata_fields = map(lambda f: f.getName(),
                              review.schema.getSchemataFields('default'))
        # [ 'reviewAuthor', 'authors', 'title', 'subtitle',
        # 'placeOfPublication', 'publisher', 'yearOfPublication',
        # 'series', 'seriesVol', 'pages', ]

        metadata_dict = dict()
        metadata_dict['pages'] = '123-456'
        for field in metadata_fields:
            log.debug('getting field %s' % field)
            metadata_dict[field] = review.getField(field).getAccessor(review)()
            if isinstance(metadata_dict[field], (tuple,list)):
                strval = ''
                for val in metadata_dict[field]:
                    strval += val + ', '
                metadata_dict[field] = strval[:-2]
            if metadata_dict[field] and \
                   not isinstance(metadata_dict[field], unicode):
                try:
                    metadata_dict[field] = metadata_dict[field].decode('utf8')
                except AttributeError:
                    log.warn('AttributeError while trying to decode %s (%s)' % (field, metadata_dict[field]))
        metadata_dict['titel_divider'] = u'. ' if metadata_dict['subtitle'] else u''
        metadata_dict['absolute_url'] = unicode(review.absolute_url())
        log.debug(metadata_dict)
        return citation_templates[review.portal_type] % metadata_dict

    def clean_citation(self, citation_dict):
        """
        Clean up the citation, decode as utf-8, remove empty
        punctuation sections
        """
        for key in citation_dict.keys():
            citation_dict[key] = citation_dict[key].decode("utf-8")
        citation = self.template % citation_dict
        citation = re.sub("^[,.:]", "", citation)
        citation = re.sub(" [,.:]", "", citation)
        citation = citation.replace("Page(s) /,", "")
        return citation

class simpleZpt(PageTemplateFile):
    """
    Use simple PageTemplateFiles for formatting the citation
    """
    def pt_getContext(self, args=(), options={}, **kw):
        rval = PageTemplateFile.pt_getContext(self, args=args)
        options.update(rval)
        return options
