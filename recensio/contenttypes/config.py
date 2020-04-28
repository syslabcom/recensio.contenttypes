"""Common configuration constants
"""

PROJECTNAME = "recensio.contenttypes"

ADD_PERMISSIONS = {
    "PresentationOnlineResource": "recensio.contenttypes: Add Presentation Online Resource",
    "PresentationArticleReview": "recensio.contenttypes: Add Presentation Article Review",
    "PresentationCollection": "recensio.contenttypes: Add Presentation Collection",
    "ReviewJournal": "recensio.contenttypes: Add Review Journal",
    "ReviewArticleJournal": "recensio.contenttypes: Add Review Article Journal",
    "ReviewArticleCollection": "recensio.contenttypes: Add Review Article Collection",
    "ReviewExhibition": "recensio.contenttypes: Add Review Exhibition",
    "PresentationMonograph": "recensio.contenttypes: Add Presentation Monograph",
    "ReviewMonograph": "recensio.contenttypes: Add Review Monograph",
    "Publication": "recensio.contenttypes: Add Publication",
    "Volume": "recensio.contenttypes: Add Volume",
    "Issue": "recensio.contenttypes: Add Issue",
}

PORTAL_TYPES = [
    "Presentation Online Resource",
    "Presentation Article Review",
    "Presentation Collection",
    "Presentation Monograph",
    "Review Journal",
    "Review Monograph",
    "Review Article Journal",
    "Review Article Collection",
    "Review Exhibition",
    "Publication",
    "Volume",
    "Issue",
]

PRESENTATION_TYPES = [
    "Presentation Online Resource",
    "Presentation Article Review",
    "Presentation Collection",
    "Presentation Monograph",
]

REVIEW_TYPES = [
    "Review Journal",
    "Review Monograph",
    "Review Article Journal",
    "Review Article Collection",
    "Review Exhibition",
]
