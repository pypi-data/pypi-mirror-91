"""
Description: Represents a span element on a web page.
"""

from pytest_elements.elements.page_element import PageElement


class Span(PageElement):
    """
    Represents a div element on a web page.
    """

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new Span instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(element_type="span", identifier=identifier, attribute=attribute, xpath=xpath)
