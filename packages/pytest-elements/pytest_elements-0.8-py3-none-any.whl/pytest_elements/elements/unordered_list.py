"""
Description: Represents an unordered list on a web page.
"""

from pytest_elements.elements.page_element import PageElement


class UnorderedList(PageElement):
    """
    Represents an unordered list on a web page
    e.g. ID or class name.
    """

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new UnorderedList instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(element_type="ul", identifier=identifier, attribute=attribute, xpath=xpath)
