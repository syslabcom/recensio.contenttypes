""" #2360

In the first version of the Recensio.net site pageStart and pageEnd
were used by PresentationArticleReview, PresentationCollection,
ReviewJournal and ReviewMonograph. The fields had a different meaning
for reviews and presentations and should never have been shared. For
reviews the fields represented the start and end pages of the uploaded
PDF. For presentations they represented the page number of the
presented text in a journal or edited volume.

#2630 requests adding page number fields to reviews to represent the
first and last page of the review in the cooperating journal so
page{Start,End}OfReviewInJournal have been added to ReviewMonograph and
ReviewJournal in addition to the existing pageStart and pageEnd fields
(for the uploaded PDF).

To clarify the situation the pageStart and pageEnd fields in
PresentationArticleReview and PresentationCollection need to be
migrated to page{Start,End}OfPresentedTextInPrint and then removed
from PresentationArticleReview and PresentationCollection.

(venv)$ instance run migrate_page_start_end.py
"""
from AccessControl.SecurityManagement import newSecurityManager
from pprint import pprint
from recensio.contenttypes.content import schemata

import transaction


rec_types = ["Presentation Article Review", "Presentation Collection"]

portal = app.recensio
pc = portal.portal_catalog

user = app.acl_users.getUser("admin").__of__(portal.acl_users)
newSecurityManager(None, user)

for i, brain in enumerate(pc({"portal_type": rec_types})):
    obj = brain.getObject()
    page_start = obj.getPageStart()
    page_end = obj.getPageEnd()
    if page_start:
        print "Migrating %s \n\t pageStart: %s" % (obj.absolute_url(), page_start)

        obj.setPageStartOfPresentedTextInPrint(page_start)
    if page_end:
        print "Migrating %s \n\t pageEnd: %s" % (obj.absolute_url(), page_end)

        obj.setPageEndOfPresentedTextInPrint(page_end)
    if i % 20 == 0:
        transaction.commit()

transaction.commit()
