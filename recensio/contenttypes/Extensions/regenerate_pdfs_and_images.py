from zope.component.hooks import getSite
from DateTime import DateTime
from recensio.contenttypes.adapter import reviewpdf

portal = getSite()
pc = portal.portal_catalog

rev_types = [
    "Review Monograph", "Presentation Monograph",
    "Presentation Collection", "Presentation Article Review",
    "Presentation Online Resource", "Review Journal" ]

feb_brains = [
    i for i in pc.searchResults({
            "portal_type": rev_types,
            "modified" : {
                "query": [DateTime(2012,2,7)],
                "range": "min", "sort_on" : "modified", "sort_order": "reverse"
                }
            })]

def main():
    for brain in feb_brains:
        obj = brain.getObject()
        obj.update_generated_pdf()
        print reviewpdf._getAllPageImages(obj, (800,1131))

