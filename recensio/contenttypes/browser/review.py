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
            "PresentationCollection":"pace",
            "PresentationArticleReview":"paj",
            "PresentationOnlineResource":"por",
            }
        meta_type = self.context.meta_type
        if rev_type_map.has_key(meta_type):
            return rev_type_map[meta_type]
        else:
            return ""

    def get_metadata(self):
        context = self.context
        fields = self.context.Schema()._fields
        meta = {}
        for field in context.metadata_fields:
            if field.startswith("get_"):
                label = self.review_journal_fields[field]
                value = context[field]()
                is_macro = False
            elif field == "review_type_code":
                label = _("label_review_type_code")
                value = self.get_review_type_code()
                is_macro = False
            elif field == "recensioID":
                label = _("label_recensio_id")
                value = "<a href='%s'>URL</a>" %context.absolute_url()
                is_macro = False
            else:
                label = fields[field].widget.label
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
