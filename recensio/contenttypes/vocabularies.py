# -*- coding: utf-8 -*-
from plone import api
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm


class PersonsVocabularyFactory(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        return PersonsVocabulary()


class PersonsVocabulary(object):
    @property
    def gnd_view(self):
        return api.content.get_view(
            context=api.portal.get(),
            request=api.portal.getRequest(),
            name="gnd",
        )

    def getTerm(self, value):
        return api.content.get(UID=value)

    def getTermByToken(self, token):
        return self.getTerm(token)

    def __iter__(self):
        for brain in self.gnd_view.list():
            yield SimpleTerm(brain["UID"], title=brain["Title"])

    def __len__(self):
        return self.gnd_view.count()
