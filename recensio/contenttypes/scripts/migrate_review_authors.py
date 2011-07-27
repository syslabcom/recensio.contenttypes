""" #3143

migrate reviewAuthorLastname, reviewAuthorFirstname to
reviewAuthors["lastname"] , reviewAuthors["firstname"]

note reviewAuthorLastname and reviewAuthorFirstname need to be part of
the schema before this can be run

(venv)$ instance run
migrate_review_authors.py
"""
from pprint import pprint

import transaction

from recensio.contenttypes.content import schemata


rec_types =  ['Presentation Online Resource',
              'Presentation Article Review',
              'Presentation Collection',
              'Presentation Monograph',
              'Review Monograph',
              'Review Journal',]

portal = app.recensio
pc = portal.portal_catalog
for i, brain in enumerate(pc({"portal_type": rec_types})):
    obj = brain.getObject()
    review_authors = obj.getReviewAuthors()
    firstname = obj.getReviewAuthorFirstname()
    lastname = obj.getReviewAuthorLastname()
    if review_authors == ({'firstname': '', 'lastname': ''},):
        print "Migrating %s \n\tReview Authors: %s \n\tFirst: %s, Last: %s" %(
            obj.absolute_url(), review_authors, firstname, lastname)

        obj.setReviewAuthors(({'firstname': firstname, 'lastname': lastname},))
    else:
        print "Skipping %s \n\tReview Authors: %s \n\tFirst: %s, Last: %s" %(
            obj.absolute_url(), review_authors, firstname, lastname)
    if i % 20 == 0:
        transaction.commit()

transaction.commit()
