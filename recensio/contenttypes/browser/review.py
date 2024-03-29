# -*- coding: utf-8 -*-
from AccessControl.SecurityManagement import getSecurityManager
from cgi import escape
from DateTime import DateTime
from os import fstat
from plone import api
from plone.app.blob.download import handleRequestRange
from plone.app.blob.iterators import BlobStreamIterator
from plone.app.blob.utils import openBlob
from Products.Archetypes.utils import contentDispositionHeader
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.browser.canonical import CanonicalURLHelper
from recensio.contenttypes.content.review import get_formatted_names
from recensio.contenttypes.interfaces import IParentGetter
from webdav.common import rfc1123_date
from ZODB.blob import Blob
from zope.component.hooks import getSite
from ZTUtils import make_query

import plone.app.blob
import recensio.theme


class View(BrowserView, CanonicalURLHelper):
    """Moderation View"""

    template = ViewPageTemplateFile("templates/review.pt")
    custom_metadata_field_labels = {
        "get_publication_title": _("Publication Title"),
        "get_journal_title": _("heading_metadata_journal"),
        "get_volume_title": _("Volume Title"),
        "get_issue_title": _("Issue Title"),
    }

    openurl_terms = {
        "title": "rft.btitle",
        "issn": "rft.issn",
        "isbn": "rft.isbn",
        "publisher": "rft.pub",
        "metadata_review_author": "rft.au",
        "placeOfPublication": "rft.place",
        "yearOfPublication": "rft.date",
        "series": "rft.series",
        "pageStartOfReviewInJournal": "rft.spage",
        "pageEndOfReviewInJournal": "rft.epage",
        "get_journal_title": "rft.jtitle",
        "pages": "rft.pages",
    }

    def get_metadata_review_author(self):
        return get_formatted_names(
            u" <br/> ", ", ", self.context.reviewAuthors, lastname_first=True
        )

    def _get_gnd_link(self, gnd_id):
        return (
            u'&nbsp;<span class="gnd-link">'
            u'<a href="https://d-nb.info/gnd/%s" title="%s" target="_blank">'
            u'<img src="++resource++recensio.theme.images/gnd.svg"'
            u'class="gnd" alt="GND" />'
            u'</a>'
            u'</span>'
            ) % (
                gnd_id,
                self.context.translate(
                    _("Person in the Integrated Authority File")
                )
            )

    def list_rows(self, rows, *keys):
        rows = [row for row in rows if any([row[key] for key in keys])]
        if rows:
            rows_ul = u"<ul class='rows_list'>"
            for row in rows:
                inner = u", ".join(
                    [safe_unicode(escape(row[key])) for key in keys if row[key]]
                )
                if hasattr(row, "UID"):
                    inner = (
                        u'<a title="%s" href="%s/search?authorsUID:list='
                        u'%s&amp;advanced_search:boolean=True&amp;'
                        u'use_navigation_root:boolean=True">%s</a>'
                    ) % (
                        self.context.translate(_("label_search")),
                        api.portal.get().absolute_url(),
                        row.UID(),
                        inner,
                    )
                rows_ul += u"<li>%s%s</li>" % (
                    inner,
                    self._get_gnd_link(row.getGndId())
                    if getattr(row, "gndId", None) else u""
                )
            rows_ul += u"</ul>"
            return rows_ul
        else:
            return u""

    def get_label(self, fields, field, meta_type):
        """Return the metadata label for a field of a particular
        portal_type
        """

        if field == "officialYearOfPublication":
            return _(
                u"label_metadata_official_year_of_publication",
                default=u"Official year of publication",
            )

        if meta_type.startswith("Review"):
            if field == "languageReview":
                return _(u"label_metadata_language_review", default=u"Language (review)")
        elif meta_type.startswith("Presentation"):
            if field == "languageReview":
                return _(
                    u"label_metadata_language_presentation",
                    default=u"Language (presentation)",
                )
        if meta_type in ["ReviewMonograph", "PresentationMonograph"]:
            if field == "languageReviewedText":
                return _(
                    u"label_metadata_language_monograph",
                    default=u"Language (monograph)",
                )
            if field == "authors":
                return _(u"Author (monograph)", default=u"Author (monograph)")
            if field == "editorial":
                return _(u"Editor (monograph)", default=u"Editor (monograph)")
        elif meta_type in ["PresentationArticleReview", "PresentationCollection"]:
            if field == "languageReviewedText":
                return _(
                    u"label_metadata_language_article", default=u"Language (article)"
                )
            if field == "authors":
                return _(u"label_metadata_author_article", default=u"Author (article)")
            if field == "editorial":
                return _(u"label_metadata_editor_article", default=u"Editor (article)")
            if field == "title":
                return _(u"label_metadata_title_article", default=u"Title (article)")
            if field == "titleCollectedEdition":
                return _(
                    u"label_metadata_title_edited_volume",
                    default=u"Title (edited volume)",
                )
        elif meta_type == "PresentationOnlineResource":
            if field == "title":
                return _(
                    u"label_metadata_name_resource", default=u"Name (Internet resource)"
                )
            if field == "languageReviewedText":
                return _(
                    u"label_metadata_language_internet_resource",
                    default=u"Language (Internet resource)",
                )
        elif meta_type == "ReviewJournal":
            if field == "languageReviewedText":
                return _(
                    u"label_metadata_language_review_journal",
                    default=u"Language (Journal)",
                )
            if field == "editor":
                return _(u"label_metadata_editor", default=u"Editor")
        elif meta_type.startswith("ReviewArticle"):
            if field == "languageReviewedText":
                return _(
                    u"label_metadata_language_article", default=u"Sprache (Aufsatz)"
                )
            elif field == "authors":
                return _(u"label_metadata_authors_article", default=u"Autor (Aufsatz)")
            elif field in ["editor", "editorial"]:
                if meta_type == "ReviewArticleCollection":
                    return _(
                        u"label_metadata_editor_edited_volume",
                        default=u"Editor (edited volume)",
                    )
                elif meta_type == "ReviewArticleJournal":
                    return _(
                        u"label_metadata_editor_journal", default=u"Editor (journal)"
                    )
            elif field == "title":
                return _(u"label_metadata_title_article", default=u"Title (article)")
            elif field == "subtitle":
                return _(
                    u"label_metadata_subtitle_article",
                    default=u"Subtitle (Article)",
                )
            elif field == "titleEditedVolume":
                return _(
                    u"label_metadata_title_edited_volume",
                    default=u"Title (edited volume)",
                )
            elif field == "subtitleEditedVolume":
                return _(
                    u"label_metadata_subtitle_edited_volume",
                    default=u"Subtitle (edited volume)",
                )
            elif field == "metadata_start_end_pages":
                return _(u"metadata_pages_review", default=u"Pages (review)")
            elif field == "translatedTitle":
                return _(
                    u"label_metadata_translated_title_article",
                    default=u"Übersetzter Titel (Aufsatz)",
                )
            elif field == "url_monograph":
                return _(
                    u"label_metadata_url_edited_volume",
                    default=u"URL (Sammelband)",
                )
            elif field == "urn_monograph":
                return _(
                    u"label_metadata_urn_edited_volume",
                    default=u"URN (Sammelband)",
                )
            elif field == "doi_monograph":
                return _(
                    u"label_metadata_doi_edited_volume",
                    default=u"DOI (Sammelband)",
                )

        return _(fields[field].widget.label)

    def get_doi_url_if_active(self):
        context = self.context
        try:
            doi_active = self.context.isDoiRegistrationActive()
        except AttributeError:
            doi_active = False
        # If DOI registration is not active and the object has only the
        # auto-generated DOI, i.e. the user has not supplied their own,
        # then we don't want to show the DOI. See #12126-86
        if not doi_active and context.getDoi() == context.generateDoi():
            return False
        else:
            return "http://dx.doi.org/%s" % (context.getDoi(),)
        return False

    def get_metadata(self):
        context = self.context
        fields = self.context.Schema()._fields
        meta = {}
        for field in context.metadata_fields:
            value = False  # A field is only displayed if it has a value
            is_macro = False
            if field.startswith("get_"):
                label = self.custom_metadata_field_labels[field]
                value = getattr(context, field)()
            elif field == "metadata_start_end_pages":
                if "metadata_start_end_pages_article" in context.metadata_fields:
                    label = _("metadata_pages_review")
                else:
                    label = _("metadata_pages")
                value = context.page_start_end_in_print
            elif field == "metadata_start_end_pages_article":
                label = _("metadata_pages_article")
                value = context.page_start_end_in_print_article
            elif field == "metadata_review_author":
                label = _("label_metadata_review_author")
                value = self.list_rows(context.reviewAuthors, "lastname", "firstname")
            elif field == "metadata_presentation_author":
                label = _("label_metadata_presentation_author")
                value = self.list_rows(context.reviewAuthors, "lastname", "firstname")
            elif field == "authors":
                label = self.get_label(fields, field, context.meta_type)
                value = self.list_rows(getattr(context, field), "lastname", "firstname")
            elif field == "editorial":
                label = self.get_label(fields, field, context.meta_type)
                value = self.list_rows(getattr(context, field), "lastname", "firstname")
            elif field == "editorsCollectedEdition":
                label = self.get_label(fields, field, context.meta_type)
                value = self.list_rows(getattr(context, field), "lastname", "firstname")
            elif field == "curators":
                label = self.get_label(fields, field, context.meta_type)
                value = self.list_rows(getattr(context, field), "lastname", "firstname")
            elif field in ["exhibiting_institution", "exhibiting_organisation"]:
                label = self.get_label(fields, field, context.meta_type)
                value = self.list_rows(getattr(context, field), "name")
            elif field == "metadata_review_type_code":
                label = _("metadata_review_type_code")
                value = context.translate(context.portal_type)
            elif field == "referenceAuthors":
                label = _("label_metadata_reference_authors")
                value = self.list_rows(getattr(context, field), "lastname", "firstname")
            elif field == "institution":
                label = _("label_metadata_institution")
                value = self.list_rows(getattr(context, field), "name")
            elif field == "metadata_recensioID":
                label = _("metadata_recensio_id")
                value = context.UID()
            elif field == "canonical_uri":
                url = context.canonical_uri
                if url:
                    label = self.get_label(fields, field, context.meta_type)
                    value = '<a rel="canonical_uri" href="%s" title="%s">%s</a>' % (
                        url,
                        url,
                        url,
                    )
            elif field in [
                "uri", "url_monograph", "url_journal", "url_article", "url_exhibition",
                "urn", "urn_monograph", "urn_journal", "urn_article"
            ]:
                url = getattr(context, field, None)
                if url:
                    label = self.get_label(fields, field, context.meta_type)
                    value = '<a href="%s" title="%s">%s</a>' % (url, url, url)
            elif field == "doi":
                doi_url = self.get_doi_url_if_active()
                if doi_url:
                    value = '<a rel="doi" href="%s" title="%s">%s</a>' % (
                        doi_url,
                        doi_url,
                        context.getDoi(),
                    )
                    label = self.get_label(fields, field, context.meta_type)
                else:
                    label = None
            elif field in [
                "doi_monograph", "doi_journal", "doi_article", "doi_exhibition"
            ]:
                doi = getattr(context, field, None)
                if doi:
                    doi_url = "http://dx.doi.org/%s" % (doi,)
                    value = '<a rel="doi" href="%s" title="%s">%s</a>' % (
                        doi_url,
                        doi_url,
                        doi,
                    )
                    label = self.get_label(fields, field, context.meta_type)
                else:
                    label = None
            elif field == "title":
                label = self.get_label(fields, field, context.meta_type)
                titles = [context.title]
                if "additionalTitles" in context.schema:
                    titles.extend(
                        [
                            additional["title"]
                            for additional in context.getAdditionalTitles()
                        ]
                    )
                value = " / ".join(titles)
            elif field == "subtitle":
                label = self.get_label(fields, field, context.meta_type)
                subtitles = [context.subtitle]
                if "additionalTitles" in context.schema:
                    subtitles.extend(
                        [
                            additional["subtitle"]
                            for additional in context.getAdditionalTitles()
                            if additional["subtitle"]
                        ]
                    )
                value = " / ".join(subtitles)
            elif field == "dates":
                label = self.get_label(fields, field, context.meta_type)
                values = getattr(context, field)
                if context.isPermanentExhibition:
                    permanent_ex = _(u"Dauerausstellung").encode("utf-8")
                    values = [
                        {
                            "place": value["place"],
                            "runtime": " ".join([permanent_ex, value["runtime"]]),
                        }
                        for value in values
                    ]
                value = self.list_rows(values, "place", "runtime")
            elif field == "effectiveDate":
                label = _("label_metadata_recensio_date")
                ploneview = api.content.get_view(
                    context=context, request=self.request, name="plone"
                )
                value = ploneview.toLocalizedTime(context[field], long_format=False)
            else:
                if field == "ddcSubject":
                    label = _("Subject classification")
                elif field == "ddcTime":
                    label = _("Time classification")
                elif field == "ddcPlace":
                    label = _("Regional classification")
                else:
                    label = self.get_label(fields, field, context.meta_type)
                # The macro is used in the template, the value is
                # used to determine whether to display that row or not
                value = getattr(context, field) and True or False
                is_macro = True
            meta[field] = {"label": label, "value": value, "is_macro": is_macro}
        return meta

    def get_metadata_context_object(self):
        context = self.context

        terms = {}
        introstr = "ctx_ver=Z39.88-2004&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook"

        for field in context.metadata_fields:
            if field in self.openurl_terms:
                name = self.openurl_terms[field]

                if field == "metadata_review_author":
                    terms.update(
                        {
                            name: [
                                "%s %s" % (au["firstname"], au["lastname"])
                                for au in context.reviewAuthors
                            ]
                        }
                    )
                elif field == "title":
                    authors = ", ".join(
                        [
                            "%s %s" % (au["firstname"], au["lastname"])
                            for au in getattr(context, "authors", [])
                        ]
                    )
                    terms.update({name: "%s: %s" % (authors, getattr(context, field))})
                elif field == "pages":
                    value = self.context.page_start_end_in_print
                    terms.update({name: value})
                else:
                    value = getattr(context, field)
                    if callable(value):
                        value = value()
                    terms.update({name: value})
        new_terms = {}
        for key, value in terms.items():
            if isinstance(value, unicode):
                new_terms[key] = value.encode("utf-8")
            elif isinstance(value, list):
                new_value = []
                for inner_value in value:
                    if isinstance(inner_value, unicode):
                        new_value.append(inner_value.encode("utf-8"))
                    else:
                        new_value.append(inner_value)
                new_terms[key] = new_value
            else:
                new_terms[key] = value
        return introstr + "&" + make_query(new_terms)

    def get_online_review_urls(self):
        existing_online_review_urls = []
        if "existingOnlineReviews" in self.context.ordered_fields:
            existingOnlineReviewUrls = self.context.getExistingOnlineReviews()
            if existingOnlineReviewUrls != () and existingOnlineReviewUrls != (
                {"name": "", "url": ""},
            ):
                existing_online_review_urls = [
                    url
                    for url in existingOnlineReviewUrls
                    if url["name"].strip() != "" and url["url"].strip() != ""
                ]
        return existing_online_review_urls

    def get_published_reviews(self):
        published_reviews = []
        if "publishedReviews" in self.context.ordered_fields:
            publishedReviews = self.context.getPublishedReviews()
            if publishedReviews != () and publishedReviews != ({"details": ""},):
                published_reviews = [
                    review
                    for review in publishedReviews
                    if review["details"].strip() != ""
                ]
        return published_reviews

    def has_coverpicture(self):
        if "coverPicture" in self.context.ordered_fields:
            coverPicture = self.context.getCoverPicture()
            return coverPicture and coverPicture.get_size() > 0 or False
        else:
            return False

    def get_preview_img_url(self):
        """Return cover picture or first page"""
        context = self.context
        if self.has_coverpicture():
            return context.absolute_url() + "/coverPicture"
        else:
            return context.absolute_url() + "/get_page_image?no:int=1"

    @property
    def do_visit_canonical_uri(self):
        url = getattr(self.context, "canonical_uri", "")
        return "www.perspectivia.net/content/publikationen/francia" in url

    def show_dara_update(self):
        sm = getSecurityManager()
        if not sm.checkPermission("Manage portal", self.context):
            return False
        try:
            return self.context.isDoiRegistrationActive()
        except AttributeError:
            return False

    def is_url_shown_in_citation_note(self):
        is_external_fulltext = getattr(
            self.context, "isUseExternalFulltext", lambda: False
        )()
        is_url_shown_via_review = getattr(
            self.context, "isURLShownInCitationNote", lambda: True
        )()
        return not is_external_fulltext and is_url_shown_via_review

    def __call__(self):
        canonical_url = self.get_canonical_url()
        if (
            not self.request["HTTP_HOST"].startswith("admin.")
            and canonical_url != self.request["ACTUAL_URL"]
        ):
            return self.request.response.redirect(canonical_url, status=301)
        return self.template()
