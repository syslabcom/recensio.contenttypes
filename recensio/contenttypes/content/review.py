# -*- CODING: utf-8 -*-
""" BaseReview is a base class all Recensio Review and Presentation
content types inherit from.
"""
from DateTime import DateTime
from cgi import escape
from os import fstat
from string import Formatter
from tempfile import NamedTemporaryFile
import cStringIO as StringIO
import logging
import re

import Acquisition
from ZODB.blob import Blob
from zope.app.component.hooks import getSite
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.component import getUtility
from zope.i18n import translate
from zope.interface import implements

from plone.app.blob.utils import openBlob
from plone.i18n.locales.languages import _languagelist

from Products.ATContentTypes.content import base
from Products.ATContentTypes.content import schemata
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.Archetypes import atapi
from Products.Archetypes.utils import DisplayList
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.Portal import PloneSite
from Products.PortalTransforms.transforms.safe_html import scrubHTML

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.helperutilities import SimpleZpt
from recensio.contenttypes.helperutilities import RunSubprocess
from recensio.contenttypes.helperutilities import SimpleSubprocess
from recensio.contenttypes.helperutilities import SubprocessException
from recensio.contenttypes.interfaces.review import IReview, IParentGetter
from recensio.policy.pdf_cut import cutPDF
from ZODB.POSException import ConflictError

from plone.app.discussion.interfaces import IConversation

log = logging.getLogger('recensio.contentypes/content/review.py')


class BaseNoMagic(object):
    def __init__(self, at_object):
        self.magic = at_object

    def directTranslate(self, msgid):
        site = getSite()
        language = getToolByName(site, \
            'portal_languages').getPreferredLanguage()
        return translate(msgid, target_language = language)

    def getUUIDUrl(real_self):
        self = real_self.magic
        base_url = self.portal_url()
        base_url += '/@@redirect-to-uuid/'
        base_url += self.UID()
        return '<a href="%s">%s</a>' % (base_url, base_url[:50] + "...")
        return base_url


class BaseReviewNoMagic(BaseNoMagic):
    def getLicense(real_self):
        self = real_self.magic
        publication = self.get_parent_object_of_type("Publication")
        publication_licence = ""
        if publication != None:
            publication_licence = getattr(publication, "licence", "")
        return True and publication_licence or _('license-note-review')

    def getFirstPublicationData(real_self):
        self = real_self.magic
        retval = []
        reference_mag = getFormatter(', ',  ', ')
        reference_mag_string = reference_mag(self.get_publication_title(), \
            self.get_volume_title(), self.get_issue_title())
        if self.canonical_uri:
            url = self.canonical_uri
            short_url = len(url) < 30 and url or url[:27] + "..."
            retval.append('<a href="%s">%s</a>'
                          % (url, short_url))

        elif reference_mag_string:
            retval.append(escape(reference_mag_string))
        return retval


class BasePresentationNoMagic(BaseNoMagic):
    def getLicense(real_self):
        self = real_self.magic
        return _('license-note-presentation')

    def getLicenseURL(real_self):
        self = real_self.magic
        return {'msg' : _('license-note-presentation-url-text'),
                'url' : _('license-note-presentation-url-url')}


class BaseBaseReviewNoMagic(object):
    def __init__(self, at_self):
        self.magic = at_self

    def listSupportedLanguages(real_self):
        self = real_self.magic
        util = getUtility(IVocabularyFactory,
            u"recensio.policy.vocabularies.available_content_languages")
        vocab = util(self)
        terms = [(x.value, _languagelist[x.value][u'native']) for x in vocab]
        return DisplayList(terms)


class BaseReview(base.ATCTMixin, HistoryAwareMixin, atapi.BaseContent):
    implements(IReview)

    def listSupportedLanguages(self):
        return BaseBaseReviewNoMagic(self).listSupportedLanguages()

    def setIsLicenceApproved(self, value):
        """
        The user needs to check the box every time they change the
        review to ensure they approve of the licence, so we don't want
        to save the value.
        """
        pass

    def update_generated_pdf(self):
        """
        If there isn't a custom pdf version of the review, generate
        the pdf from an Office document file, (anything supported by
        abiword). If there isn't an Office file then generate the pdf
        from the contents of the review text (html)
        """
        has_custom_pdf = hasattr(self, "pdf") and self.pdf.get_size() > 0
        if not has_custom_pdf:
            # Generate the pdf file and save it as a blob
            pdf_blob = Blob()
            doc = None
            try:
                create_pdf = RunSubprocess(
                    "abiword",
                    input_params="--plugin=AbiCommand -t pdf",
                    output_params="-o")
                create_pdf.create_tmp_ouput()
                if hasattr(self, "doc"):
                    doc = self.getDoc()
                if doc:
                    open_blob = doc.blob.open("r")
                    blob_path = open_blob.name
                    open_blob.close()
                    create_pdf.run(input_path=blob_path)
                else:
                    review = self.getReview()
                    # Insert the review into a template so we have a valid html file
                    pdf_template = SimpleZpt("../browser/templates/htmltopdf.pt")
                    data = pdf_template(context={"review":review}).encode("utf-8")
                    with NamedTemporaryFile() as tmp_input:
                        with NamedTemporaryFile() as tmp_output:
                            tmp_input.write(data)
                            tmp_input.flush()
                            try:
                                pass
    #                            SimpleSubprocess('/usr/bin/tidy', '-o', tmp_output.name, tmp_input.name, exitcodes=[0,1])
    #                            tmp_output.seek(0)
    #                            data = tmp_output.read()
                            except RuntimeError:
                                log.error("Tidy was unable to tidy the html for %s" % self.absolute_url())
                        create_pdf.create_tmp_input(suffix=".pdf", data=data)
                    try:
                        create_pdf.run()
                    except RuntimeError:
                        log.error("Abiword was unable to generate a pdf for %s and created an error pdf" % self.absolute_url())
                        create_pdf.create_tmp_input(suffix=".pdf", data="Could not create PDF")
                        create_pdf.run()

                pdf_file = open(create_pdf.output_path, "r")
                pdf_data = pdf_file.read()
                pdf_blob.open("w").writelines(pdf_data)
                pdf_file.close()
                create_pdf.clean_up()

                self.generatedPdf = pdf_blob
            except SubprocessException:
                log.error("The application Abiword does not seem to be available")

    def get_review_pdf(self):
        """ Return the uploaded pdf if that doesn't exist return the
        generatedPdf Blob object otherwise return None

        Also return the size since it is not easy to get this from the
        blob directly
        """
        pdf = {}
        size = 0
        if hasattr(self, "pdf"):
            size = self.pdf.get_size()
            if size > 0:
                pdf["size"] = size
                pdf["blob"] = self.pdf.blob
        if size == 0 and hasattr(self, "generatedPdf"):
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

    def listAuthors(self, listEditors = False):
        if not getattr(self, 'getAuthors', None):
            return []
        retval = []
        for author in self.getAuthors():
            if author['lastname'] or author['firstname']:
                retval.append(u'%s, %s' % (
                        author['lastname'].decode('utf-8'),
                        author['firstname'].decode('utf8')
                        )
                              )
        if listEditors:
            if not getattr(self, 'getEditorsCollectedEdition', None):
                return retval
            for editor in self.getEditorsCollectedEdition():
                if editor['lastname'] or editor['firstname']:
                    retval.append(u'%s, %s' % (
                            editor['lastname'].decode('utf8'),
                            editor['firstname'].decode('utf-8')
                            )
                                  )
        return retval


    def getAllAuthorData(self):
        retval = []
        field_values = list(getattr(self, 'authors', [])) + \
                       list(getattr(self, 'referenceAuthors', []))
        for data in field_values:
            if data['lastname'] or data['firstname']:
                retval.append(('%s, %s' % (
                            data['lastname'],
                            data['firstname'])).decode('utf-8').encode('utf-8')
                              )
        try:
           review_author = ('%s, %s' % (\
              self.reviewAuthorLastname,
              self.reviewAuthorFirstname
              )).decode('utf-8').encode('utf-8')
           if review_author.strip() != ',':
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
        return IParentGetter(self).get_title_from_parent_of_type(meta_type)

    def get_parent_object_of_type(self, meta_type):
        """ Return the object of a particular type which is
        the parent of the current object."""
        return IParentGetter(self).get_parent_object_of_type(meta_type)

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

    def processForm(self, data=1, metadata=0, REQUEST=None, values=None):
        pdf, start, end = [self.REQUEST.get(x, None) for x in \
            ['pdf_file', 'pageStart', 'pageEnd']]
        if all((pdf, start != 0, end)):
            new_file_upload = cutPDF(pdf, start, end)
            new_file_upload.filename = pdf.filename
            self.REQUEST.set('pdf_file', new_file_upload)
            self.REQUEST.form['pdf_file'] = new_file_upload
        return super(BaseReview, self).processForm(data, metadata, REQUEST, \
            values)

    def SearchableText(self):
        data = super(BaseReview, self).SearchableText()

        # get text from pdf
        datastream = ""
        pdfdata = ""
        pdf = self.get_review_pdf()
        if pdf:
            f = pdf['blob'].open().read()
            transforms = getToolByName(self, 'portal_transforms')
            try:
                datastream = transforms.convertTo(
                    "text/plain",
                    str(f),
                    mimetype = 'application/pdf',
                    )
            except (ConflictError, KeyboardInterrupt):
                raise
            except Exception, e:
                log("Error while trying to convert file contents to 'text/plain' "
                    "in %r.getIndexable(): %s" % (self, e))
            pdfdata = str(datastream)
        value = " ".join([data, pdfdata])

        # get text from comments
        conversation = IConversation(self)
        # wf = getToolByName(self, 'portal_workflow')
        for comment in conversation.getComments():
            # if wf.getInfoFor(comment, 'review_state') == 'published':
                value = " ".join([data, comment.getText().encode('utf8')])

        return value
