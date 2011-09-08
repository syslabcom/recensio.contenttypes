"""Prints out common content type schema fields

Run from your buildout with:
(venv)$ instance run content_types_schema_info.py
"""
from recensio.contenttypes.content import schemata
from pprint import pprint


rec_types =  ['Presentation Online Resource',
              'Presentation Article Review',
              'Presentation Collection',
              'Presentation Monograph',
              'Review Monograph',
              'Review Journal',]

portal = app.recensio
all_fields = set()
portal_type_fields = {}
field_portal_types = {}
portal_types_fields = {}
for portal_type in rec_types:
    obj = portal.portal_catalog({"portal_type":portal_type})[0].getObject()
    portal_type_fields[portal_type] = {}
    for field in obj.Schema().fields():
        field_name = field.getName()
        portal_type_fields[portal_type][field_name] = {}
        field_info = portal_type_fields[portal_type][field_name]
        field_info["label"] = field.widget.label
        field_info["description"] = field.widget.description
        field_info["edit_visible"] = field.widget.visible.get("edit", "")
        field_info["is_metadata"] = field_name in obj.metadata_fields
        all_fields.add(field)
        field_portal_types.setdefault(field.getName(), []).append(portal_type)

[field_portal_types[i].sort() for i in field_portal_types.keys()]
for portal_types in field_portal_types.values():
    for field_name in field_portal_types.keys():
        if field_portal_types[field_name] == portal_types:
            portal_types_fields.setdefault(str(portal_types),
                                           set()).add(field_name)

for key in sorted(portal_types_fields.keys()):
    print "Common schema fields:"
    print(key)
    pprint(sorted(portal_types_fields[key]))

for portal_type in rec_types:
    ptf = portal_type_fields[portal_type].get("uri", None)
    if ptf:
        label       = ptf["label"]
        is_metadata = ptf["is_metadata"]
        description = ptf["description"]
        edit_visible = ptf["edit_visible"]
        print("%s:\n  label: %s\n  description: %s\n  edit visible:  %s"
              % (portal_type, label, description, edit_visible))
    else:
        print("%s:\n  edit_visible: %s"
              % (portal_type, edit_visible))


# canonical_uri is the url of imported reviews/presentations.
# Presentations have a uri field for the location of the presented text
# online (if it exists). Reviews have a uri field for Partner URL. These
# should be two separate fields.

"""
Common schema fields:
['Presentation Article Review', 'Presentation Collection', 'Presentation Monograph', 'Presentation Online Resource', 'Review Journal', 'Review Monograph']
['allowDiscussion',
 'canonical_uri',
 'contributors',
 'creation_date',
 'creators',
 'ddcPlace',
 'ddcSubject',
 'ddcTime',
 'description',
 'effectiveDate',
 'excludeFromNav',
 'expirationDate',
 'generatedPdf',
 'id',
 'language',
 'languageReview',
 'languageReviewedText',
 'location',
 'modification_date',
 'recensioID',
 'review',
 'reviewAuthors',
 'rights',
 'subject',
 'title',
 'uri',
 'urn']
Common schema fields:
['Presentation Article Review', 'Presentation Collection', 'Presentation Monograph', 'Presentation Online Resource']
['isLicenceApproved',
 'labelPresentationAuthor',
 'reviewAuthorEmail',
 'reviewAuthorHonorific',
 'reviewAuthorPersonalUrl']
Common schema fields:
['Presentation Article Review', 'Presentation Collection', 'Presentation Monograph', 'Review Journal', 'Review Monograph']
['idBvb', 'placeOfPublication', 'publisher', 'subtitle', 'yearOfPublication']
Common schema fields:
['Presentation Article Review', 'Presentation Collection', 'Presentation Monograph', 'Review Monograph']
['authors']
Common schema fields:
['Presentation Article Review', 'Presentation Collection', 'Presentation Monograph']
['referenceAuthors']
Common schema fields:
['Presentation Article Review', 'Presentation Collection', 'Review Journal', 'Review Monograph']
['pageEnd', 'pageStart']
Common schema fields:
['Presentation Article Review', 'Presentation Collection']
['pageEndOfPresentedTextInPrint', 'pageStartOfPresentedTextInPrint']
Common schema fields:
['Presentation Article Review', 'Review Journal']
['issn',
 'issueNumber',
 'officialYearOfPublication',
 'shortnameJournal',
 'volumeNumber']
Common schema fields:
['Presentation Article Review']
['titleJournal']
Common schema fields:
['Presentation Collection', 'Presentation Monograph', 'Review Monograph']
['isbn', 'pages', 'series', 'seriesVol']
Common schema fields:
['Presentation Collection']
['editorsCollectedEdition', 'titleCollectedEdition']
Common schema fields:
['Presentation Monograph', 'Review Journal', 'Review Monograph']
['coverPicture']
Common schema fields:
['Presentation Monograph']
['existingOnlineReviews', 'publishedReviews', 'tableOfContents']
Common schema fields:
['Presentation Online Resource']
['documenttypes_bibliographical',
 'documenttypes_cooperation',
 'documenttypes_fulltexts',
 'documenttypes_institution',
 'documenttypes_periodicals',
 'documenttypes_referenceworks',
 'institution',
 'labelwidget_categories']
Common schema fields:
['Review Journal', 'Review Monograph']
['customCitation',
 'doc',
 'pageEndOfReviewInJournal',
 'pageStartOfReviewInJournal',
 'pdf']
Common schema fields:
['Review Journal']
['editor']
Presentation Online Resource:
  label: URL
  description:
  edit visible:  visible
Presentation Article Review:
  label: URL
  description:
  edit visible:  visible
Presentation Collection:
  label: URL
  description:
  edit visible:  visible
Presentation Monograph:
  label: description_presentation_uri
  description: URL
  edit visible:  visible
Review Monograph:
  label: URL
  description:
  edit visible:  hidden
Review Journal:
  label: URL
  description:
  edit visible:  hidden
"""
