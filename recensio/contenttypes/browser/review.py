from DateTime import DateTime
from os import fstat
from webdav.common import rfc1123_date
import recensio.theme
from ZODB.blob import Blob
from zope.app.component.hooks import getSite
from ZTUtils import make_query

from plone.app.blob.download import handleRequestRange
from plone.app.blob.iterators import BlobStreamIterator
from plone.app.blob.utils import openBlob
import plone.app.blob

from Products.Archetypes.utils import contentDispositionHeader
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from recensio.contenttypes import contenttypesMessageFactory as _
from recensio.contenttypes.content.review import get_formatted_names

class View(BrowserView):
    """Moderation View
    """
    template = ViewPageTemplateFile('templates/review.pt')
    custom_metadata_field_labels = {
        "get_publication_title": _("Publication Title"),
        "get_journal_title": _("heading_metadata_journal"),
        "get_volume_title": _("Volume Title"),
        "get_issue_title": _("Issue Title")
        }

    openurl_terms = {
        'title':                'rft.btitle',
        'issn':                 'rft.issn',
        'isbn':                 'rft.isbn',
        'publisher':            'rft.pub',
        'authors':              'rft.au',
        'placeOfPublication':   'rft.place',
        'yearOfPublication':    'rft.date',
        'series':               'rft.series',
        'pageStartOfReviewInJournal': 'rft.spage',
        'pageEndOfReviewInJournal': 'rft.epage',
        'get_journal_title':    'rft.jtitle',
        'pages':                'rft.pages',
        }

    def get_metadata_review_author(self):
        return get_formatted_names(u' <br/> ', ', ', self.context.reviewAuthors,
                                   lastname_first=True)

    def list_rows(self, rows, *keys):
        # Archetypes is nasty sometimes,
        # and for fields with multiple values it can happen that if
        # there is no value set, one gets list with one element that
        # is completely empty
        filter_rule = lambda x: ("".join([x[key] for key in keys])).strip()
        rows = filter(filter_rule, rows)
        if rows:
            rows_ul = "<ul class='rows_list'>"
            for row in rows:
                rows_ul += "<li>%s</li>" %(
                    ", ".join([row[key] for key in keys])
                    )
            rows_ul += "</ul>"
            return rows_ul
        else:
            return ""

    def get_label(self, fields, field, meta_type):
        """ Return the metadata label for a field of a particular
        portal_type
        """

        if field == "officialYearOfPublication":
                return _(u"label_metadata_official_year_of_publication",
                         default=u"Official year of publication")

        if meta_type.startswith("Review"):
            if field == "languageReview":
                return _(u"label_metadata_language_review",
                         default=u"Language (review)")
        elif meta_type.startswith("Presentation"):
            if field == "languageReview":
                return _(u"label_metadata_language_presentation",
                         default=u"Language (presentation)")
        if meta_type in ["ReviewMonograph", "PresentationMonograph"]:
            if field == "languageReviewedText":
                return _(u"label_metadata_language_monograph",
                         default=u"Language (monograph)")
            if field == "authors":
                return _(u"Author (monograph)",
                         default=u"Author (monograph)")
        elif meta_type in ["PresentationArticleReview",
                           "PresentationCollection"]:
            if field == "languageReviewedText":
                return _(u"label_metadata_language_article",
                         default=u"Language (article)")
            if field == "authors":
                return _(u"label_metadata_author_article",
                         default=u"Author (article)")
            if field == "title":
                return _(u"label_metadata_title_article",
                         default=u"Title (article)")
            if field == "titleCollectedEdition":
                return _(u"label_metadata_title_edited_volume",
                         default=u"Title (edited volume)")
        elif meta_type == "PresentationOnlineResource":
            if field == "title":
                return _(u"label_metadata_name_resource",
                         default=u"Name (Internet resource)")
            if field == "languageReviewedText":
                return _(u"label_metadata_language_internet_resource",
                         default=u"Language (Internet resource)")
        elif meta_type == "ReviewJournal":
            if field == "languageReviewedText":
                return _(u"label_metadata_language_review_journal",
                         default=u"Language (Journal)")
            if field == "editor":
                return _(u"label_metadata_editor",
                         default=u"Editor")

        return _(fields[field].widget.label)

    def get_metadata(self):
        context = self.context
        fields = self.context.Schema()._fields
        meta = {}
        value = False # A field is only displayed if it has a value
        for field in context.metadata_fields:
            is_macro = False
            if field.startswith("get_"):
                label = self.custom_metadata_field_labels[field]
                value = context[field]()
            elif field == "authors_editorial":
                label = _("Author (monograph)")
                value = "<br/>".join(context.list_authors_editorial())
            elif field == "metadata_start_end_pages":
                label = _("metadata_pages")
                value = context.page_start_end_in_print
            elif field == "metadata_review_author":
                label = _("label_metadata_review_author")
                value = self.list_rows(
                    context["reviewAuthors"], "lastname", "firstname")
            elif field == "metadata_presentation_author":
                label = _("label_metadata_presentation_author")
                value = self.list_rows(
                    context["reviewAuthors"], "lastname", "firstname")
            elif field == "authors":
                label = self.get_label(fields, field, context.meta_type)
                value = self.list_rows(context[field], "lastname", "firstname")
            elif field == "editorsCollectedEdition":
                label = self.get_label(fields, field, context.meta_type)
                value = self.list_rows(context[field], "lastname", "firstname")
            elif field == "metadata_review_type_code":
                label = _("metadata_review_type_code")
                value = context.translate(context.portal_type)
            elif field == "referenceAuthors":
                label = _("label_metadata_reference_authors")
                value = self.list_rows(context[field],
                                       "lastname", "firstname")
            elif field == "institution":
                label = _("label_metadata_institution")
                value = self.list_rows(context[field], "lastname", "firstname")
            elif field == "metadata_recensioID":
                label = _("metadata_recensio_id")
                value = context.UID()
            elif field == 'canonical_uri':
                url = context.canonical_uri
                if url:
                    label = self.get_label(fields, field, context.meta_type)
                    value = ('<a rel="canonical_uri" href="%s">%s</a>'
                             % (url, url))
            elif field == 'uri':
                url = context.uri
                if url:
                    label = self.get_label(fields, field, context.meta_type)
                    value = ('<a href="%s">%s</a>'
                             % (url, url))
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
                value = context[field] and True or False
                is_macro = True
            meta[field] = {'label': label,
                           'value': value,
                           'is_macro': is_macro}
        return meta

    def get_metadata_context_object(self):
        context = self.context
        metadata = self.get_metadata()

        terms = {}
        introstr = 'ctx_ver=Z39.88-2004&rft_val_fmt=info%3Aofi%2Ffmt%3Akev%3Amtx%3Abook'

        for field in context.metadata_fields:
            if field in self.openurl_terms:
                name = self.openurl_terms[field]

                if field == 'authors':
                    terms.update(
                        {name: ["%s %s" %(au['firstname'], au['lastname'])
                                for au in context[field]]})
                elif field == "pages":
                    value = self.context.page_start_end_in_print
                    terms.update({name: value})
                else:
                    value = context[field]
                    if callable(value):
                        value = value()
                    terms.update({name: value})

        return introstr + '&' + make_query(terms)

    def get_online_review_urls(self):
        existing_online_review_urls = []
        if "existingOnlineReviews" in self.context.ordered_fields:
            existingOnlineReviewUrls = self.context.getExistingOnlineReviews()
            if existingOnlineReviewUrls != () \
                    and existingOnlineReviewUrls != (
                {'name': '', 'url': ''},):
                existing_online_review_urls = [
                    url for url in existingOnlineReviewUrls
                    if url["name"].strip() != ""
                    and url["url"].strip() != ""]
        return existing_online_review_urls

    def get_published_reviews(self):
        published_reviews = []
        if "publishedReviews" in self.context.ordered_fields:
            publishedReviews = self.context.getPublishedReviews()
            if publishedReviews != () \
                    and publishedReviews != ({'details': ''},):
                published_reviews = [
                    review for review in publishedReviews
                    if review["details"].strip() != ""]
        return published_reviews

    def has_coverpicture(self):
        if "coverPicture" in self.context.ordered_fields:
            coverPicture = self.context.getCoverPicture()
            return coverPicture and coverPicture.get_size() > 0 or False
        else:
            return False

    def get_preview_img_url(self):
        """Return cover picture or first page """
        context = self.context
        if self.has_coverpicture():
            return context.absolute_url()+"/coverPicture"
        else:
            return context.absolute_url()+"/get_page_image?no:int=1"

    @property
    def do_visit_canonical_uri(self):
        url = getattr(self.context, "canonical_uri", "")
        return "www.perspectivia.net/content/publikationen/francia" in url

    def __call__(self):
        return self.template()
