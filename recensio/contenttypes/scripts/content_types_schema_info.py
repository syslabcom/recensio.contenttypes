"""Prints out common content type schema fields"""
from recensio.contenttypes.content import schemata
from pprint import pprint


rec_types =  ['Presentation Online Resource',
              'Presentation Article Review',
              'Presentation Collection',
              'Review Journal',
              'Presentation Monograph',
              'Review Monograph',]

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
    print portal_type
    print "uri: %s, is metadata?: %s" % (
        portal_type_fields[portal_type]["uri"]["label"],
        portal_type_fields[portal_type]["uri"]["is_metadata"],
        )

# canonical_uri is the url of imported reviews/presentations.
# Presentations have a uri field for the location of the presented text
# online (if it exists). Reviews have a uri field for Partner URL. These
# should be two separate fields.

"""
['Presentation Article Review', 'Presentation Collection',
 'Presentation Monograph', 'Presentation Online Resource', 'Review
 Journal', 'Review Monograph']:
['allowDiscussion', 'canonical_uri', 'contributors', 'creation_date',
 'creators', 'ddcPlace', 'ddcSubject', 'ddcTime', 'description',
 'effectiveDate', 'excludeFromNav', 'expirationDate', 'generatedPdf',
 'id', 'language', 'languageReview', 'languageReviewedText',
 'location', 'modification_date', 'recensioID', 'review',
 'reviewAuthorFirstname', 'reviewAuthorLastname', 'rights', 'subject',
 'title', 'uri']

['Presentation Article Review', 'Presentation Collection',
'Presentation Monograph', 'Presentation Online Resource']:
['isLicenceApproved', 'labelPresentationAuthor', 'reviewAuthorEmail',
 'reviewAuthorHonorific', 'reviewAuthorPersonalUrl']

['Presentation Article Review', 'Presentation Collection',
'Presentation Monograph', 'Review Journal', 'Review Monograph']:
['idBvb', 'placeOfPublication', 'publisher', 'subtitle', 'yearOfPublication']

['Presentation Article Review', 'Presentation Collection',
'Presentation Monograph', 'Review Monograph']:
['authors']

['Presentation Article Review', 'Presentation Collection',
'Presentation Monograph']:
['referenceAuthors']

['Presentation Article Review', 'Presentation Collection', 'Review
Journal', 'Review Monograph']:
['pageEnd', 'pageStart']

['Presentation Article Review', 'Review Journal']:
['issn', 'issueNumber', 'officialYearOfPublication',
 'shortnameJournal', 'volumeNumber']

['Presentation Article Review']:
['titleJournal']

['Presentation Collection', 'Presentation Monograph', 'Review Monograph']:
['isbn', 'pages', 'series', 'seriesVol']

['Presentation Collection']:
['editorsCollectedEdition', 'titleCollectedEdition']

['Presentation Monograph', 'Review Journal', 'Review Monograph']:
['coverPicture']

['Presentation Monograph']:
['existingOnlineReviews', 'publishedReviews', 'tableOfContents']

['Presentation Online Resource']:
['documenttypes_bibliographical', 'documenttypes_cooperation',
 'documenttypes_fulltexts', 'documenttypes_institution',
 'documenttypes_periodicals', 'documenttypes_referenceworks',
 'institution', 'labelwidget_categories']

['Review Journal', 'Review Monograph']:
['customCitation', 'doc', 'pdf']

['Review Journal']:
['editor']
"""
