from recensio.contenttypes.content import presentationarticlereview
from recensio.contenttypes.content import presentationcollection
from recensio.contenttypes.content import presentationmonograph
from recensio.contenttypes.content import presentationonlineresource
from recensio.contenttypes.content import reviewarticlecollection
from recensio.contenttypes.content import reviewarticlejournal
from recensio.contenttypes.content import reviewexhibition
from recensio.contenttypes.content import reviewjournal
from recensio.contenttypes.content import reviewmonograph

import doctest
import unittest2 as unittest


def test_suite():
    suite = doctest.DocTestSuite(reviewexhibition)
    suite.addTests(doctest.DocTestSuite(reviewjournal))
    suite.addTests(doctest.DocTestSuite(reviewmonograph))
    suite.addTests(doctest.DocTestSuite(reviewarticlejournal))
    suite.addTests(doctest.DocTestSuite(reviewarticlecollection))
    suite.addTests(doctest.DocTestSuite(presentationarticlereview))
    suite.addTests(doctest.DocTestSuite(presentationcollection))
    suite.addTests(doctest.DocTestSuite(presentationmonograph))
    suite.addTests(doctest.DocTestSuite(presentationonlineresource))
    return suite
