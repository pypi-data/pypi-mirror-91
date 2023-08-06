"""
Description: Represents an h4 header on a web page.
DEPRECIATED: Use heading.py!
"""

from pytest_elements.elements.heading import Heading


class H4(Heading):
    """
    Represents an h4 header on a web page. Allows elements to be located via different attributes
    e.g. ID or class name.
    """

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new H4 instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(element_type="h4", identifier=identifier, attribute=attribute, xpath=xpath)
