"""
Description: Represents a Heading on a web page.
"""

from pytest_elements.elements.page_element import PageElement


class Heading(PageElement):
    """
    Represents a Heading on a web page. Allows elements to be located via different attributes
    e.g. ID or class name.
    """

    def __init__(self, element_type=None, identifier=None, attribute=None, xpath=None):
        """
        Construct a new Heading instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(
            element_type=element_type, identifier=identifier, attribute=attribute, xpath=xpath,
        )
