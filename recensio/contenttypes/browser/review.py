from DateTime import DateTime
from os import fstat
from webdav.common import rfc1123_date
import recensio.theme
from ZODB.blob import Blob

from plone.app.blob.download import handleRequestRange
from plone.app.blob.iterators import BlobStreamIterator
from plone.app.blob.utils import openBlob
import plone.app.blob

from Products.Archetypes.utils import contentDispositionHeader
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from recensio.contenttypes import contenttypesMessageFactory as _


class View(BrowserView):
    """Moderation View
    """
    template = ViewPageTemplateFile('review.pt')
    review_journal_fields = {
        "get_publication_title": _("Publication Title"),
        "get_volume_title": _("Volume Title"),
        "get_issue_title": _("Issue Title")
        }

    def get_review_type_code(self):
        """ Return the short Review Type code
        """
        rev_type_map = {
            "ReviewMonograph":"rm",
            "ReviewJournal":"rj",
            "PresentationMonograph":"pm",
            "PresentationCollection":"paev",
            "PresentationArticleReview":"paj",
            "PresentationOnlineResource":"por",
            }
        meta_type = self.context.meta_type
        if rev_type_map.has_key(meta_type):
            return rev_type_map[meta_type]
        else:
            return ""

    def get_review_author(self):
        lastname = self.context.reviewAuthorLastname
        firstname = self.context.reviewAuthorFirstname
        return "%s, %s" %(lastname, firstname)

    def list_rows(self, rows, *keys):
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
        return _(fields[field].widget.label)

    def get_metadata(self):
        context = self.context
        fields = self.context.Schema()._fields
        meta = {}
        for field in context.metadata_fields:
            is_macro = False
            if field.startswith("get_"):
                label = self.review_journal_fields[field]
                value = context[field]()
            elif field == "metadata_review_author":
                label = _("label_metadata_review_author")
                value = self.get_review_author()
            elif field == "metadata_presentation_author":
                label = _("label_metadata_presentation_author")
                value = self.get_review_author()
            elif field == "authors":
                label = self.get_label(fields, field, context.meta_type)
                value = self.list_rows(context[field], "lastname", "firstname")
            elif field == "editorsCollectedEdition":
                label = self.get_label(fields, field, context.meta_type)
                value = self.list_rows(context[field], "lastname", "firstname")
            elif field == "metadata_review_type_code":
                label = _("metadata_review_type_code")
                value = self.get_review_type_code()
            elif field == "referenceAuthors":
                label = _("label_metadata_reference_authors")
                value = self.list_rows(context.referenceAuthors,
                                       "lastname", "firstname")
            elif field == "metadata_recensioID":
                label = _("metadata_recensio_id")
                value = context.UID()
            elif field == 'canonical':
                label = self.get_label(fields, field, context.meta_type)
                value = '<a rel="canonical" href="%s">URL</a>'\
                        % context.canonical
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

    def has_coverpicture(self):
        if "coverPicture" in self.context.ordered_fields:
            coverPicture = self.context.getCoverPicture()
            return coverPicture and coverPicture.get_size() > 0 or False
        else:
            return False

    def __call__(self):
        return self.template()
