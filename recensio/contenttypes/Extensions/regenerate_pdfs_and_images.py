from zope.component.hooks import getSite
from DateTime import DateTime
from recensio.contenttypes.adapter import reviewpdf

portal = getSite()
pc = portal.portal_catalog

rev_types = [
    "Review Monograph", "Presentation Monograph",
    "Presentation Collection", "Presentation Article Review",
    "Presentation Online Resource", "Review Journal" ]

query = {
    "path": '/'.join(portal.getPhysicalPath()),
    "portal_type": rev_types,
    "modified": {
        "query": [DateTime(2012, 2, 7)],
        "range": "min", "sort_on": "modified", "sort_order": "reverse"
        }
}
feb_brains = pc.searchResults(query)
if None in feb_brains:
    query['b_size'] = len(feb_brains)
    feb_brains = pc.searchResults(query)


def main():
    for brain in feb_brains:
        obj = brain.getObject()
        obj.update_generated_pdf()
        print reviewpdf._getAllPageImages(obj, (800,1131))
