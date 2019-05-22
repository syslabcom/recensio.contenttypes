# -*- coding: utf-8 -*-
import unittest
from recensio.contenttypes.content.review import BaseReview


class TestReviewTitle(unittest.TestCase):

    def test_one_title_and_one_subtitle(self):
        obj = BaseReview(None)
        obj.title = u"Die spanische Verfassung von 1812"
        obj.subtitle = u"Der Beginn des europäischen Konstitutionalismus"
        obj.getAdditionalTitles = lambda: []
        self.assertEqual(
            obj.punctuated_title_and_subtitle,
            u"Die spanische Verfassung von 1812. Der Beginn des europäischen "
            u"Konstitutionalismus",
        )

    def test_two_titles_and_two_subtitles(self):
        obj = BaseReview(None)
        obj.title = u"Die spanische Verfassung von 1812"
        obj.subtitle = u"Der Beginn des europäischen Konstitutionalismus"
        obj.getAdditionalTitles = lambda: [
            {
                "title": u"La Constitución española de 1812",
                "subtitle": u"El comienzo del constitucionalismo europeo",
            },
        ]
        self.assertEqual(
            obj.punctuated_title_and_subtitle,
            u"Die spanische Verfassung von 1812. Der Beginn des europäischen "
            u"Konstitutionalismus / La Constitución española de 1812. El "
            u"comienzo del constitucionalismo europeo",
        )
