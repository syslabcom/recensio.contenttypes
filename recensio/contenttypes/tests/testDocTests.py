import unittest2 as unittest
import doctest
from recensio.contenttypes.content import reviewmonograph, reviewjournal,\
    presentationarticlereview

def test_suite():
    suite = doctest.DocTestSuite(reviewjournal)
    suite.addTests(doctest.DocTestSuite(reviewmonograph))
    suite.addTests(doctest.DocTestSuite(presentationarticlereview))
    return suite
