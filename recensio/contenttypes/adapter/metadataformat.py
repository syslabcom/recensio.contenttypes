#-*- coding: utf-8 -*-
from Products.CMFPlone.utils import safe_unicode
from cgi import escape
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
        >>> at_mock.formatted_authors_editorial = lambda: "Patrick Gerken / Alexander Pilz"
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

    def get_citation_string(self, obj):
        """
        Either return the custom citation or the generated one
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.customCitation = ''
        >>> at_mock.get = lambda x: None
        >>> at_mock.formatted_authors_editorial = lambda: u"Gerken\u2665, Patrick\u2665 / Pilz, Alexander"
        >>> at_mock.title = "Plone 4.0♥?"
        >>> at_mock.subtitle = "Das Benutzerhandbuch♥"
        >>> at_mock.reviewAuthors = [{'firstname' : 'Cillian♥', 'lastname' : 'de Roiste♥'}]
        >>> at_mock.yearOfPublication = '2009♥'
        >>> at_mock.publisher = 'SYSLAB.COM GmbH♥'
        >>> at_mock.placeOfPublication = 'München♥'
        >>> at_mock.get_issue_title = lambda :'Open Source Mag 1♥'
        >>> at_mock.get_volume_title = lambda :'Open Source Mag Vol 1♥'
        >>> at_mock.get_publication_title = lambda :'Open Source♥'
        >>> at_mock.portal_url = lambda :'http://www.syslab.com'
        >>> at_mock.UID = lambda :'12345'
        >>> at_mock.canonical_uri = ''
        >>> at_mock.page_start_end_in_print = '11-21'
        >>> review = ReviewMonographNoMagic(at_mock)
        >>> review.directTranslate = lambda m: m.default
        >>> review.get_citation_string()
        u'de Roiste\u2665, Cillian\u2665: review of: Gerken\u2665, Patrick\u2665 / Pilz, Alexander, Plone 4.0\u2665? Das Benutzerhandbuch\u2665, M\\xfcnchen\u2665: SYSLAB.COM GmbH\u2665, 2009\u2665, in: Open Source\u2665, Open Source Mag Vol 1\u2665, Open Source Mag 1\u2665, p. 11-21, <a href="http://syslab.com/r/12345">http://syslab.com/r/12345</a>'


        Original Spec:

        [Rezensent Nachname], [Rezensent Vorname]: review of: [Werkautor Nachname], [Werkautor Vorname], [Werktitel]. [Werk-Untertitel], [Erscheinungsort]: [Verlag], [Jahr], in: [Zs-Titel], [Nummer], [Heftnummer (Erscheinungsjahr)], p.[pageStart]-[pageEnd] URL recensio.

        Werkautoren kann es mehrere geben, die werden dann durch ' / ' getrennt alle aufgelistet.
        Note: gezähltes Jahr entfernt.
        Da es die Felder Zs-Titel, Nummer und Heftnummer werden die Titel der Objekte magazine, volume, issue genommen, in dem der Review liegt

        Müller, Klaus: review of: Meier, Hans, Geschichte des Abendlandes. Ein Abriss, München: Oldenbourg, 2010, in: Zeitschrift für Geschichte, 39, 3 (2008/2009), www.recensio.net/##

        """
        if obj.customCitation:
            return scrubHTML(obj.customCitation).decode('utf8')

        args = {
            'review_of' : translate_message(Message(
                    u"text_review_of", "recensio", default="review of:")),
            'in'        : translate_message(Message(
                    u"text_in", "recensio", default="in:")),
            'page'      : translate_message(Message(
                    u"text_pages", "recensio", default="p.")),
            ':'         : translate_message(Message(
                    u"text_colon", "recensio", default=":")),
            }
        if obj.title[-1] in '!?:;.,':
            title_subtitle = getFormatter(u' ')
        else:
            title_subtitle = getFormatter(u'. ')
        rev_details_formatter = getFormatter(
            u', ', u', ', u'%(:)s ' % args, u', ')
        rezensent_string = get_formatted_names(
            u' / ', ', ', obj.reviewAuthors, lastname_first = True)
        authors_string = obj.formatted_authors_editorial()
        title_subtitle_string = title_subtitle(obj.title, obj.subtitle)
        item_string = rev_details_formatter(
            authors_string, title_subtitle_string,
            obj.placeOfPublication, obj.publisher,
            obj.yearOfPublication)
        mag_year_string = obj.yearOfPublication.decode('utf-8')
        mag_year_string = mag_year_string and u'(' + mag_year_string + u')' \
            or None

        mag_number_formatter = getFormatter(u', ', u', ')
        mag_number_string = mag_number_formatter(
            obj.get_publication_title(), obj.get_volume_title(),
            obj.get_issue_title())

        location = obj.getUUIDUrl()
        if getattr(obj, "canonical_uri", False): #3102
            location = translate_message(
                Message(u"label_downloaded_via_recensio","recensio"))

        citation_formatter = getFormatter(
            u'%(:)s %(review_of)s ' % args, ', %(in)s ' % args, ', %(page)s ' % args, u', ')

        citation_string = citation_formatter(
            escape(rezensent_string), escape(item_string),
            escape(mag_number_string),
            obj.page_start_end_in_print, location)

        return citation_string
