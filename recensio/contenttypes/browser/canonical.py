from plone.registry.interfaces import IRegistry
from recensio.policy.interfaces import IRecensioSettings
from zope.component import getUtility


class CanonicalURLHelper(object):
    def get_canonical_url(self):
        registry = getUtility(IRegistry)
        recensio_settings = registry.forInterface(IRecensioSettings)
        virtual_url = self.request.get("VIRTUAL_URL_PARTS", [])
        if virtual_url and virtual_url[0] != recensio_settings.external_portal_url:
            canonical_url = "/".join(
                (
                    recensio_settings.external_portal_url,
                    "/".join(self.context.getPhysicalPath()[2:]),
                )
            )
            return canonical_url
        else:
            return self.request["ACTUAL_URL"]
