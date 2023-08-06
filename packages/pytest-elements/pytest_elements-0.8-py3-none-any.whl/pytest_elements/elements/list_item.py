"""
Description: Represents a list item on a web page.
"""

from pytest_elements.elements.page_element import PageElement


class ListItem(PageElement):
    """
    Represents a list item on a web page
    e.g. ID or class name.
    """

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new ListItem instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(element_type="li", identifier=identifier, attribute=attribute, xpath=xpath)
