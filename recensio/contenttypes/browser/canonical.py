from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from recensio.policy.interfaces import IRecensioSettings


class CanonicalURLHelper(object):

    def get_canonical_url(self):
        registry = getUtility(IRegistry)
        recensio_settings = registry.forInterface(IRecensioSettings)
        if self.request['VIRTUAL_URL_PARTS'][0] != recensio_settings.external_portal_url:
            canonical_url = '/'.join((
                recensio_settings.external_portal_url,
                '/'.join(self.context.getPhysicalPath()[2:]),
            ))
            return canonical_url
        else:
            return self.request['ACTUAL_URL']
