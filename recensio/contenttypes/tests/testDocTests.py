import unittest2 as unittest
import doctest
from recensio.contenttypes.content import reviewmonograph, reviewjournal,\
    presentationarticlereview, presentationcollection, presentationmonograph,\
    presentationonlineresource

@unittest.skip("Obsolete, see TestMetadataFormat")
def test_suite():
    suite = doctest.DocTestSuite(reviewjournal)
    suite.addTests(doctest.DocTestSuite(reviewmonograph))
    suite.addTests(doctest.DocTestSuite(presentationarticlereview))
    suite.addTests(doctest.DocTestSuite(presentationcollection))
    suite.addTests(doctest.DocTestSuite(presentationmonograph))
    suite.addTests(doctest.DocTestSuite(presentationonlineresource))
    return suite
