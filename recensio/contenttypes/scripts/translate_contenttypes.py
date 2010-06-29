#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os

map = {
"trefferdaten" : ("searchresults", ""),
"bezugsautoren" : ("referenceAuthors","Reference Authors"),
"ddcRaum" : ("ddcPlace","ddc place"),
"ddcSach" : ("ddcSubject","ddc subject"),
"ddcZeit" : ("ddcTime","ddc time"),
"erscheinungsjahr" : ("yearOfPublication","Year of publication"),
"erscheinungsort" : ("placeOfPublication","Place of publication"),
"gezaehltesJahr" : ("officialYearOfPublication","Official year of publication"),
"heftnummer" : ("number","Number"),
"kuerzelZeitschrift" : ("shortnameJournal","Shortname (jurnal)"),
"praesentationTextsprache" : ("languagePresentation","Language (presentation)"),
"praesentiertenSchriftTextsprache" : ("languageReview","Language (review)"),
"reihennummer" : ("seriesVol","Series Volume"),
"rezensionAutor" : ("reviewAuthor","Review author"),
"schlagwoerter" : ("subject","Subject"),
"seitenzahl" : ("pages","Pages"),
"untertitel" : ("subtitle","Subtitle"),
"verbundID" : ("idBvb","ID BVB"),
"verlag" : ("publisher","Publisher"),
"praesentationenvonaufsatzinzeitschrift" : ("presentationarticlereview", ""),
"praesentationenvoninternetressourcen" : ("presentationonlineresource", ""),
"praesentationenvonmonographien" : ("presentationmonograph", ""),
"praesentationvonaufsatzinsammelband" : ("presentationcollection", ""),
"rezensioneinermonographie" : ("reviewmonograph", ""),
"rezensioneinerzeitschrift" : ("reviewjournal", ""),
"IPraesentationenvonAufsatzinZeitschrift" : ("IPresentationArticleReview", ""),
"IPraesentationenvonInternetressourcen" : ("IPresentationOnlineResource", ""),
"IPraesentationenvonMonographien" : ("IPresentationMonograph", ""),
"IPraesentationvonAufsatzinSammelband" : ("IPresentationCollection", ""),
"IRezensioneinerMonographie" : ("IReviewMonograph", ""),
"IRezension" : ("IReview", ""),
"IRezensioneinerZeitschrift" : ("IReviewJournal", ""),
"reihe" : ("series","Series"),
"PraesentationenvonAufsatzinZeitschrift" : ("PresentationArticleReview", ""),
"PraesentationenvonInternetressourcen" : ("PresentationOnlineResource", ""),
"PraesentationenvonMonographien" : ("PresentationMonograph", ""),
"PraesentationvonAufsatzinSammelband" : ("PresentationCollection", ""),
"RezensioneinerMonographie" : ("ReviewMonograph", ""),
"Rezension" : ("Review", ""),
"RezensioneinerZeitschrift" : ("ReviewJournal", ""),
"RevieweinerMonographie" : ("ReviewMonograph", ""),
"RevieweinerZeitschrift" : ("ReviewJournal", ""),
"rezension" : ("review","Review"),
"Rezension" : ("Review","Review"),
"nummer" : ("volume","Volume"),
"Add Praesentationen von Internetressourcen": ("Add Presentation Online Resource", ""),
"Add Praesentationen von Aufsatz in Zeitschrift" : ("Add Presentation Article Review", ""),
"Add Praesentation von Aufsatz in Sammelband": ("Add Presentation Collection", ""),
"Add Review einer Zeitschrift" : ("Add Review Journal", ""),
"Add Praesentationen von Monographien": ("Add Presentation Monograph", ""),
"Add Review einer Monographie" : ("Add Review Monograph", ""),
"Praesentationen von Internetressourcen": ("Presentation Online Resource", ""),
"Praesentationen von Aufsatz in Zeitschrift" : ("Presentation Article Review", ""),
"Praesentation von Aufsatz in Sammelband": ("Presentation Collection", ""),
"Review einer Zeitschrift" : ("Review Journal", ""),
"Praesentationen von Monographien": ("Presentation Monograph", ""),
"Review einer Monographie" : ("Review Monograph", ""),
"herausgeberSammelband": ("editorCollectedEdition", ""),
"herausgeber": ("editor", ""),
"Herausgeber Sammelband": ("Editor Collected Edition", ""),
"Herausgeber": ("Editor", ""),

}


sorted_keys = ['verlag', 'verbundID', 'untertitel', 'trefferdaten',
               'seitenzahl', 'schlagwoerter',
               "Herausgeber Sammelband",
               "Herausgeber",
               "Add Praesentationen von Internetressourcen",
               "Add Praesentationen von Aufsatz in Zeitschrift" ,
               "Add Praesentation von Aufsatz in Sammelband",
               "Add Review einer Zeitschrift" ,
               "Add Praesentationen von Monographien",
               "Add Review einer Monographie" ,
               "Praesentationen von Internetressourcen",
               "Praesentationen von Aufsatz in Zeitschrift" ,
               "Praesentation von Aufsatz in Sammelband",
               "Review einer Zeitschrift" ,
               "Praesentationen von Monographien",
               "Review einer Monographie" ,
               'rezensioneinerzeitschrift',
               'rezensioneinermonographie', 'rezensionAutor',
               'rezension', 'reihennummer', 'reihe',
               'praesentiertenSchriftTextsprache',
               'praesentationvonaufsatzinsammelband',
               'praesentationenvonmonographien',
               'praesentationenvoninternetressourcen',
               'praesentationenvonaufsatzinzeitschrift',
               'praesentationTextsprache', 'kuerzelZeitschrift',
               'heftnummer', 'nummer', 'gezaehltesJahr',
               'erscheinungsort', 'erscheinungsjahr', 'ddcZeit',
               'ddcSach', 'ddcRaum', 'bezugsautoren',
               'IRezensioneinerZeitschrift',
               'IRezensioneinerMonographie', 'IRezension',
               'IPraesentationvonAufsatzinSammelband',
               'IPraesentationenvonMonographien',
               'IPraesentationenvonInternetressourcen',
               'IPraesentationenvonAufsatzinZeitschrift',
               "PraesentationenvonAufsatzinZeitschrift",
               "PraesentationenvonInternetressourcen",
               "PraesentationenvonMonographien",
               "PraesentationvonAufsatzinSammelband",
               "RezensioneinerMonographie",
               "RevieweinerMonographie",
               "RevieweinerZeitschrift",
               'Rezension', 
               "herausgeberSammelband",
               "herausgeber",

]

if __name__ == "__main__":
    for dirpath, dirnames, files in os.walk("."):
        for a_file in files:
            if a_file != __file__ and \
                   (a_file.endswith(".pt") or \
                    a_file.endswith(".xml") or \
                    a_file.endswith(".zcml") or \
                    a_file.endswith(".py") ):
                path =  os.path.abspath(os.path.join(dirpath, a_file))
                contents = open(path, "r").read()
                for key in sorted_keys:
                    if key in contents:
                        contents = contents.replace(key, map[key][0])
                        print path
                        print key
                        print map[key][0]
                open(path, "w").write(contents)
