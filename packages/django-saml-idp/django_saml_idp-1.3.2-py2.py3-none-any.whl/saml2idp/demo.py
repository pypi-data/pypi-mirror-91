from __future__ import absolute_import, print_function, unicode_literals
from . import base, xml_render

class Processor(base.Processor):
    """
    Demo Response Handler Processor for testing against django-saml2-sp.
    """
    def _format_assertion(self):
        # NOTE: This uses the SalesForce assertion for the demo.
        self._assertion_xml = xml_render.get_assertion_salesforce_xml(self._assertion_params, signed=True)


class AttributeProcessor(base.Processor):
    """
    Demo Response Handler Processor for testing against django-saml2-sp;
    Adds SAML attributes to the assertion.
    """
    def _format_assertion(self):
        # NOTE: This uses the SalesForce assertion for the demo.
        self._assertion_params['ATTRIBUTES'] = {
            'foo': 'bar',
        }
        self._assertion_xml = xml_render.get_assertion_salesforce_xml(self._assertion_params, signed=True)
