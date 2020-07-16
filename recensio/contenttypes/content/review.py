# -*- CODING: utf-8 -*-
""" BaseReview is a base class all Recensio Review and Presentation
content types inherit from.
"""
import logging
from cgi import escape
from os import fstat
from string import Formatter
from tempfile import NamedTemporaryFile

from plone import api
from plone.app.blob.utils import openBlob
from plone.app.discussion.interfaces import IConversation
from plone.registry.interfaces import IRegistry
from Products.Archetypes import atapi
from Products.ATContentTypes.content import base
from Products.ATContentTypes.lib.historyaware import HistoryAwareMixin
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.eventhandlers import review_pdf_updated_eventhandler
from recensio.contenttypes.helperutilities import RunSubprocess
from recensio.contenttypes.helperutilities import SimpleSubprocess
from recensio.contenttypes.helperutilities import SimpleZpt
from recensio.contenttypes.helperutilities import SubprocessException
from recensio.contenttypes.interfaces.review import IParentGetter
from recensio.contenttypes.interfaces.review import IReview
from recensio.imports.pdf_cut import cutPDF
from recensio.policy.indexer import isbn
from recensio.policy.interfaces import IRecensioSettings
from recensio.theme.browser.views import listAvailableContentLanguages
from recensio.theme.browser.views import listRecensioSupportedLanguages
from recensio.theme.browser.views import recensioTranslate
from ZODB.blob import Blob
from ZODB.POSException import ConflictError
from zope.component import getUtility
from zope.component.hooks import getSite
from zope.i18n import translate
from zope.i18nmessageid import Message
from zope.interface import implements
from zope.intid.interfaces import IIntIds

log = logging.getLogger("recensio.contentypes/content/review.py")


def get_formatted_names(
    full_name_separator, name_part_separator, names, lastname_first=False
):
    name_part1 = "firstname"
    name_part2 = "lastname"
    if lastname_first:
        name_part1 = "lastname"
        name_part2 = "firstname"
    return escape(
        full_name_separator.join(
            [
                getFormatter(name_part_separator)(x[name_part1], x[name_part2])
                for x in names
            ]
        )
    )


class BaseNoMagic(object):
    def __init__(self, at_object):
        self.magic = at_object

    def directTranslate(self, msgid):
        site = getSite()
        language = getToolByName(site, "portal_languages").getPreferredLanguage()
        return translate(msgid, target_language=language)

    def getUUIDUrl(real_self):
        self = real_self.magic
        base_url = self.portal_url()
        if base_url.startswith("http://www."):
            base_url = base_url.replace("http://www.", "http://")
        base_url += "/r/"
        base_url += self.UID()
        return '<a href="%s">%s</a>' % (base_url, base_url)
        return base_url


class BaseReviewNoMagic(BaseNoMagic):
    def getLicense(real_self):
        self = real_self.magic
        publication = self.get_parent_object_of_type("Publication")
        publication_licence = ""
        current = self
        if publication is not None:
            while current != publication.aq_parent:
                if hasattr(current, "getLicence_ref"):
                    licence_obj = current.getLicence_ref()
                else:
                    licence_obj = None
                if licence_obj:
                    licence_translated = licence_obj.getTranslation()
                    publication_licence = licence_translated.getText()
                else:
                    publication_licence = getattr(current.aq_base, "licence", "")
                if publication_licence:
                    break
                current = current.aq_parent
        return True and publication_licence or _("license-note-review")

    def getFirstPublicationData(real_self):
        self = real_self.magic
        retval = []
        reference_mag = getFormatter(", ", ", ")
        reference_mag_string = reference_mag(
            self.get_publication_title(),
            self.get_volume_title(),
            self.get_issue_title(),
        )
        if self.canonical_uri:
            url = self.canonical_uri
            short_url = len(url) < 60 and url or url[:57] + "..."
            retval.append('<a href="%s">%s</a>' % (url, short_url))

        elif reference_mag_string:
            retval.append(escape(reference_mag_string))
        return retval

    def get_citation_location(real_self):
        self = real_self.magic
        location = []
        try:
            doi_active = self.isDoiRegistrationActive()
        except AttributeError:
            doi_active = False
        # If DOI registration is not active and the object has only the
        # auto-generated DOI, i.e. the user has not supplied their own,
        # then we don't want to show the DOI. See #12126-86
        has_doi = doi_active or self.getDoi() != self.generateDoi()
        has_canonical_uri = getattr(self, "canonical_uri", False)
        if has_doi:
            doi = self.getDoi()
            location.append(u'DOI: <a href="http://dx.doi.org/%s">%s</a>' % (doi, doi))
        if has_canonical_uri and not self.isUseExternalFulltext():  # 3102 #REC-984
            location.append(
                real_self.directTranslate(
                    Message(
                        u"label_downloaded_via_recensio",
                        "recensio",
                        mapping={"portal": api.portal.get().Title()},
                    )
                )
            )
        if not has_canonical_uri and not has_doi:
            location.append(real_self.getUUIDUrl())

        return u", ".join(location)


class BasePresentationNoMagic(BaseNoMagic):
    def getLicense(real_self):
        self = real_self.magic
        return _("license-note-presentation")

    def getLicenseURL(real_self):
        self = real_self.magic
        return {
            "msg": _("license-note-presentation-url-text"),
            "url": _("license-note-presentation-url-url"),
        }

    @property
    def punctuated_authors(real_self):
        self = real_self.magic
        return u" / ".join(
            [getFormatter(" ")(x["firstname"], x["lastname"]) for x in self.authors]
        )


class BaseReview(base.ATCTMixin, HistoryAwareMixin, atapi.BaseContent):
    implements(IReview)

    def listAvailableContentLanguages(self):
        return listAvailableContentLanguages()

    def listRecensioSupportedLanguages(self):
        return listRecensioSupportedLanguages()

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
                    output_params="-o",
                )
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
                    # Insert the review into a template so we have a
                    # valid html file
                    pdf_template = SimpleZpt("../browser/templates/htmltopdf.pt")
                    data = pdf_template(context={"review": review}).encode("utf-8")
                    with NamedTemporaryFile() as tmp_input:
                        with NamedTemporaryFile() as tmp_output:
                            tmp_input.write(data)
                            tmp_input.flush()
                            try:
                                SimpleSubprocess(
                                    "/usr/bin/tidy",
                                    "-utf8",
                                    "-numeric",
                                    "-o",
                                    tmp_output.name,
                                    tmp_input.name,
                                    exitcodes=[0, 1],
                                )
                                tmp_output.seek(0)
                                data = tmp_output.read()
                            except RuntimeError:
                                log.error(
                                    "Tidy was unable to tidy the html for %s",
                                    self.absolute_url(),
                                    exc_info=True,
                                )
                        create_pdf.create_tmp_input(suffix=".html", data=data)
                    try:
                        create_pdf.run()
                    except RuntimeError:
                        log.error(
                            "Abiword was unable to generate a pdf for %s and created an error pdf",
                            self.absolute_url(),
                            exc_info=True,
                        )
                        create_pdf.create_tmp_input(
                            suffix=".html", data="Could not create PDF"
                        )
                        create_pdf.run()

                pdf_file = open(create_pdf.output_path, "r")
                pdf_data = pdf_file.read()
                pdf_blob.open("w").writelines(pdf_data)
                pdf_file.close()
                create_pdf.clean_up()

                self.generatedPdf = pdf_blob
            except SubprocessException:
                log.error(
                    "The application Abiword does not seem to be available",
                    exc_info=True,
                )

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

    def get_page_image(self, no=1, refresh=False):
        """
        Return a page of the review text
        """
        images = getattr(self, "pagePictures", None)
        if images is None or refresh:
            review_pdf_updated_eventhandler(self, None)
            images = getattr(self, "pagePictures", None)
        if no > len(images):
            no = 0
        try:
            I = images[no - 1]
            I.get_size(self)
        except (TypeError, AttributeError):
            # 17.8.2012 Fallback if upgrade is not done yet
            review_pdf_updated_eventhandler(self, None)
            images = getattr(self, "pagePictures", None)

        I = images[no - 1]
        self.REQUEST.RESPONSE.setHeader("Content-Type", "image/gif")
        self.REQUEST.RESPONSE.setHeader("Content-Length", I.get_size(self))

        return I.getRaw(self).data

    def get_no_pages(self):
        """
        Return the number of pages that are stored as images
        See get_page_image()
        """
        pagePictures = getattr(self, "pagePictures", None)
        return pagePictures and len(pagePictures) or 0

    @property
    def page_start_end_in_print(self):
        """ See #2630
        PAJ/PAEV/RJ/RM have page start and end fields"""

        page_start = getattr(
            self,
            "pageStartOfPresentedTextInPrint",
            getattr(self, "pageStartOfReviewInJournal", ""),
        )

        page_end = getattr(
            self,
            "pageEndOfPresentedTextInPrint",
            getattr(self, "pageEndOfReviewInJournal", ""),
        )
        return self.format_page_start_end(page_start, page_end)

    @property
    def page_start_end_in_print_article(self):
        page_start = self.pageStartOfArticle
        page_end = self.pageEndOfArticle
        return self.format_page_start_end(page_start, page_end)

    def format_page_start_end(self, page_start, page_end):
        # page_start is set to 0 when it is left empty in the bulk
        # import spreadsheet #4054
        if page_start in (None, 0):
            page_start = ""
        page_start = str(page_start).strip()

        # page_end is set to 0 when it is left empty in the bulk
        # import spreadsheet #4054
        if page_end in (None, 0):
            page_end = ""
        page_end = str(page_end).strip()

        if page_start == page_end:
            # both the same/empty
            page_start_end = page_start
        elif page_start and page_end:
            page_start_end = "%s-%s" % (page_start, page_end)
        else:
            # one is not empty
            page_start_end = page_start or page_end
        return page_start_end

    def listAuthors(self, listEditors=False):
        if not getattr(self, "getAuthors", None):
            return []
        retval = []
        if listEditors and getattr(self, "getEditorial", None):
            for editor in self.getEditorial():
                if editor["lastname"] or editor["firstname"]:
                    retval.append(
                        u"%s, %s"
                        % (
                            safe_unicode(editor["lastname"]),
                            safe_unicode(editor["firstname"]),
                        )
                    )
        for author in self.getAuthors():
            if author["lastname"] or author["firstname"]:
                retval.append(
                    u"%s, %s"
                    % (
                        safe_unicode(author["lastname"]),
                        safe_unicode(author["firstname"]),
                    )
                )
        return retval

    def listAuthorsAndEditors(self):
        return self.listAuthors(listEditors=True)

    def listReviewAuthors(self):
        if not getattr(self, "getReviewAuthors", None):
            return []
        retval = []
        for author in self.getReviewAuthors():
            if author["lastname"] or author["firstname"]:
                retval.append(
                    u"%s, %s"
                    % (
                        safe_unicode(author["lastname"]),
                        safe_unicode(author["firstname"]),
                    )
                )
        return retval

    def listReviewAuthorsFirstnameFirst(self):
        if not getattr(self, "getReviewAuthors", None):
            return []
        retval = []
        for author in self.getReviewAuthors():
            retval.append(
                u"%s %s"
                % (safe_unicode(author["firstname"]), safe_unicode(author["lastname"]))
            )
        return retval

    def getAllAuthorData(self):
        retval = []
        field_values = list(getattr(self, "authors", []))
        field_values += list(getattr(self, "editorial", []))
        for data in field_values:
            if data["lastname"] or data["firstname"]:
                retval.append(
                    safe_unicode(
                        ("%s, %s" % (data["lastname"], data["firstname"]))
                    ).encode("utf-8")
                )
        review_author = get_formatted_names(
            u" / ", ", ", self.reviewAuthors, lastname_first=True
        )
        if review_author.strip() != ",":
            retval.append(safe_unicode(review_author).encode("utf-8"))
        return retval

    def getAllAuthorDataFulltext(self):
        authors = " ".join(self.getAllAuthorData())
        return safe_unicode(authors)

    def Language(self):
        """ Reviews are NOT translatable. As such, they must remain neutral """
        return ""

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

    def get_flag_with_override(self, field_name, override_value):
        return IParentGetter(self).get_flag_with_override(field_name, override_value)

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
        pdf, start, end = [
            self.REQUEST.get(x, None) for x in ["pdf_file", "pageStart", "pageEnd"]
        ]
        if all((pdf, start != 0, end)):
            new_file_upload = cutPDF(pdf, start, end)
            new_file_upload.filename = pdf.filename
            self.REQUEST.set("pdf_file", new_file_upload)
            self.REQUEST.form["pdf_file"] = new_file_upload
        return super(BaseReview, self).processForm(data, metadata, REQUEST, values)

    def SearchableText(self):
        data = super(BaseReview, self).SearchableText()

        if hasattr(self, "getSubtitle"):
            data = " ".join([data, self.getSubtitle()])
        if hasattr(self, "getAdditionalTitles"):
            for t in self.getAdditionalTitles():
                data = " ".join([data, t["title"], t["subtitle"],])
        data = " ".join([data, self.getReview()])

        data = " ".join([data, self.Creator()])
        if hasattr(self, "getYearOfPublication"):
            data = " ".join([data, self.getYearOfPublication()])
        if hasattr(self, "getPlaceOfPublication"):
            data = " ".join([data, self.getPlaceOfPublication()])
        data = " ".join([data] + isbn(self)())

        if hasattr(self, "getYearOfPublicationOnline"):
            data = " ".join([data, self.getYearOfPublicationOnline()])
        if hasattr(self, "getPlaceOfPublicationOnline"):
            data = " ".join([data, self.getPlaceOfPublicationOnline()])

        # get text from pdf
        datastream = ""
        pdfdata = ""
        pdf = self.get_review_pdf()
        if pdf:
            f = pdf["blob"].open().read()
            transforms = getToolByName(self, "portal_transforms")
            try:
                datastream = transforms.convertTo(
                    "text/plain", str(f), mimetype="application/pdf",
                )
            except (ConflictError, KeyboardInterrupt):
                raise
            except Exception as e:
                log(
                    "Error while trying to convert file contents to 'text/plain' "
                    "in %r.getIndexable(): %s" % (self, e)
                )
            pdfdata = str(datastream)
        data = " ".join([data, pdfdata])

        # get text from comments
        conversation = IConversation(self)
        # wf = getToolByName(self, 'portal_workflow')
        for comment in conversation.getComments():
            # if wf.getInfoFor(comment, 'review_state') == 'published':
            data = " ".join([data, comment.getText()])

        return data

    def format(self, title, subtitle):
        last_char = title[-1]
        if last_char in ["!", "?", ":", ";", ".", ","]:
            return getFormatter(" ")(title, subtitle)
        else:
            return getFormatter(". ")(title, subtitle)

    @property
    def punctuated_title_and_subtitle(self):
        """ #3129
        Note: all review types except for Presentation Online Resource
        have the subtitle field.
        titleProxy is used in Review Exhibition and can be empty, while title always has
        a value."""
        title = getattr(self, "titleProxy", self.title)
        subtitle = self.subtitle
        titles = [
            (title, subtitle),
        ]
        if "additionalTitles" in self.schema:
            titles = titles + [
                (additional["title"], additional["subtitle"])
                for additional in self.getAdditionalTitles()
            ]

        return " / ".join(
            [self.format(title, subtitle) for title, subtitle in titles if title]
        )

    @property
    def formatted_authors(self):
        authors_list = []
        for author in self.getAuthors():
            if author["lastname"] or author["firstname"]:
                authors_list.append(
                    (
                        u"%s %s"
                        % (
                            safe_unicode(author["firstname"]),
                            safe_unicode(author["lastname"]),
                        )
                    ).strip()
                )
        return u" / ".join(authors_list)

    @property
    def formatted_editorial(self):
        editor_str = ""
        result = ""
        if hasattr(self, "editorial"):
            editorial = self.getEditorial()
            label_editor = ""
            if len(editorial) > 0 and editorial != ({"lastname": "", "firstname": ""}):
                if len(editorial) == 1:
                    label_editor = recensioTranslate(u"label_abbrev_editor")
                    editor = editorial[0]
                    editor_str = (
                        u"%s %s"
                        % (
                            safe_unicode(editor["firstname"]),
                            safe_unicode(editor["lastname"]),
                        )
                    ).strip()
                else:
                    label_editor = recensioTranslate(u"label_abbrev_editors")
                    editors = []
                    for editor in editorial:
                        editors.append(
                            (
                                u"%s %s"
                                % (
                                    safe_unicode(editor["firstname"]),
                                    safe_unicode(editor["lastname"]),
                                )
                            ).strip()
                        )
                    editor_str = u" / ".join(editors)
                if editor_str != "":
                    result = editor_str + " " + label_editor
        return result

    @property
    def formatted_authors_editorial(self):
        """ #3111
        PMs and RMs have an additional field for editors"""
        authors_str = self.formatted_authors

        result = ""
        editor_str = self.formatted_editorial

        if editor_str != "":
            result = editor_str
            if authors_str != "":
                result = result + ": " + authors_str

        if result == "" and authors_str != "":
            result = authors_str

        return escape(result)

    def generateDoi(self):
        factorytool = getToolByName(self, "portal_factory", None)
        if factorytool is not None and factorytool.isTemporary(self):
            return ""
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IRecensioSettings)
        prefix = settings.doi_prefix
        intids = getUtility(IIntIds)
        obj_id = intids.register(self)
        return "{0}{1}".format(prefix, obj_id)

    def isUseExternalFulltext(self):
        """ If any parent has this activated then we also want it active here.
            FLOW-741
        """
        return self.get_flag_with_override("useExternalFulltext", True)

    def isURLShownInCitationNote(self):
        """ If any parent has this deactivated then we also want it inactive here.
            SCR-341
        """
        return self.get_flag_with_override("URLShownInCitationNote", False)
