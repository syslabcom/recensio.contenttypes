from recensio.contenttypes.content.schemata import ImageValidator

import pkg_resources
import unittest2 as unittest


class TestImageChecker(unittest.TestCase):
    def testWithInvalidImages(self):
        no_image = file(pkg_resources.resource_filename(__name__, "test.txt"))
        self.assertFalse(ImageValidator()(no_image) == True)

    def testWithValidImage(self):
        image = file(pkg_resources.resource_filename(__name__, "test.jpg"))
        self.assertTrue(ImageValidator()(image))
