# -*- coding: utf-8 -*-

from mock import Mock

import unittest2 as unittest


class MockAuthor(dict):
    def __get__(self, key):
        return self[key]


class TestExcelImportUnit(unittest.TestCase):
    def test_list_rows_empty(self):
        from recensio.contenttypes.browser.review import View

        view = View(None, None)
        self.assertEquals("", view.list_rows([], "lastname", "firstname"))

    def test_list_rows_stupid_empty(self):
        from recensio.contenttypes.browser.review import View

        view = View(None, None)
        self.assertEquals(
            "",
            view.list_rows([MockAuthor({"lastname": "", "firstname": ""})], "lastname", "firstname"),
        )

    def test_list_rows_stupid_empty2(self):
        from recensio.contenttypes.browser.review import View

        view = View(None, None)
        self.assertEquals(
            "<ul class='rows_list'><li>a, b</li></ul>",
            view.list_rows(
                [
                    MockAuthor({"lastname": "a", "firstname": "b"}),
                    MockAuthor({"lastname": "", "firstname": ""}),
                ],
                "lastname",
                "firstname",
            ),
        )
