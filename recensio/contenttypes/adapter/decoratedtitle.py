#-*- coding: utf-8 -*-
from recensio.contenttypes.interfaces import IDecoratedTitle
from recensio.contenttypes.citation import getFormatter
from recensio.contenttypes.content.review import get_formatted_names
from recensio.contenttypes.helperutilities import translate_message
from zope import interface
from zope.i18nmessageid import Message


class DecoratedTitle(object):
    interface.implements(IDecoratedTitle)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def getDecoratedTitle(self, obj, lastname_first=False):
        """
        >>> from mock import Mock
        >>> at_mock = Mock()
        >>> at_mock.customCitation = ''
        >>> at_mock.formatted_authors_editorial = "Patrick Gerken / Alexander Pilz"
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
        authors_string = obj.formatted_authors_editorial

        rezensent_string = get_formatted_names(
            u' / ', ' ', obj.reviewAuthors, lastname_first=lastname_first)
        if rezensent_string:
            rezensent_string = "(%s)" % translate_message(
                Message(u"reviewed_by", "recensio",
                        mapping={u"review_authors": rezensent_string}))

        full_citation = getFormatter(': ', ' ')
        return full_citation(
            authors_string, obj.punctuated_title_and_subtitle, rezensent_string)
