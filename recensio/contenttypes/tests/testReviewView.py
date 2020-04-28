# -*- coding: utf-8 -*-

import unittest2 as unittest
from mock import Mock


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
            view.list_rows(
                [{"lastname": "", "firstname": ""}], "lastname", "firstname"
            ),
        )

    def test_list_rows_stupid_empty2(self):
        from recensio.contenttypes.browser.review import View

        view = View(None, None)
        self.assertEquals(
            "<ul class='rows_list'><li>a, b</li></ul>",
            view.list_rows(
                [
                    {"lastname": "a", "firstname": "b"},
                    {"lastname": "", "firstname": ""},
                ],
                "lastname",
                "firstname",
            ),
        )
