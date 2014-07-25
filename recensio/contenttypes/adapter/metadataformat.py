#-*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.helperutilities import get_formatted_names
from recensio.contenttypes.helperutilities import translate_message
from recensio.contenttypes.interfaces import IMetadataFormat
from recensio.theme.browser.views import recensioTranslate
from zope import interface
from zope.i18nmessageid import Message


class BaseMetadataFormat(object):
    interface.implements(IMetadataFormat)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getDecoratedTitle(self, obj, lastname_first=False):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.customCitation = ''
        >>> at_mock.formatted_authors_editorial() = "Patrick Gerken / Alexander Pilz"
        >>> at_mock.punctuated_title_and_subtitle = "Plone 4.0. Das Benutzerhandbuch"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian', 'lastname'  : 'de Roiste'}]
        >>> review = ReviewMonographNoMagic(at_mock)
        >>> review.directTranslate = lambda a: a
        >>> review.getDecoratedTitle()
        u'Patrick Gerken / Alexander Pilz: Plone 4.0. Das Benutzerhandbuch (reviewed_by)'

        Original Spec:
        [Werkautor Vorname] [Werkautor Nachname]: [Werktitel]. [Werk-Untertitel] (reviewed by [Rezensent Vorname] [Rezensent Nachname])

        Analog, Werkautoren kann es mehrere geben (Siehe Citation)

        Hans Meier: Geschichte des Abendlandes. Ein Abriss (reviewed by Klaus Müller)

        """
        name_part_separator = " "
        if lastname_first:
            name_part_separator = ", "
        authors_string = obj.formatted_authors_editorial()

        rezensent_string = get_formatted_names(
            u' / ', ' ', obj.reviewAuthors, lastname_first=lastname_first)
        if rezensent_string:
            rezensent_string = "(%s)" % translate_message(
                Message(u"reviewed_by", "recensio",
                        mapping={u"review_authors": rezensent_string}))

        full_citation = getFormatter(': ', ' ')
        return full_citation(
            authors_string, obj.punctuated_title_and_subtitle, rezensent_string)

    def formatted_authors_editorial(self, obj):
        """ #3111
        PMs and RMs have an additional field for editors"""
        authors_list = []
        for author in obj.getAuthors():
            if author['lastname'] or author['firstname']:
                author_name = u'%s %s' % (
                    safe_unicode(author['firstname']), safe_unicode(author['lastname']))
                authors_list.append(author_name.strip())
        authors_str = u" / ".join(authors_list)

        editor_str = ""
        result = ""
        if hasattr(obj, "editorial"):
            editorial = obj.getEditorial()
            label_editor = ""
            if len(editorial) > 0 and editorial != (
                    {'lastname': '', 'firstname': ''}):
                if len(editorial) == 1:
                    label_editor = recensioTranslate(u"label_abbrev_editor")
                    editor = editorial[0]
                    editor_name = u'%s %s' % (
                        safe_unicode(editor['firstname']), safe_unicode(editor['lastname']))
                    editor_str = editor_name.strip()
                else:
                    label_editor = recensioTranslate(u"label_abbrev_editors")
                    editors = []
                    for editor in editorial:
                        editor_name = u'%s %s' % (
                            safe_unicode(editor['firstname']), safe_unicode(editor['lastname']))
                        editors.append(editor_name.strip())
                    editor_str = u" / ".join(editors)

                if editor_str != "":
                    result = editor_str + " " + label_editor
                    if authors_str != "":
                        result = result + ": " + authors_str

        if result == "" and authors_str != "":
            result = authors_str

        return result
