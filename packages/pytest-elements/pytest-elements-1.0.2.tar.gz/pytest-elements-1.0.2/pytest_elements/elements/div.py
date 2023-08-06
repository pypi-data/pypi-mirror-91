"""
Description: Represents a div element on a web page.
"""
from pytest_elements.elements.page_element import PageElement


class Div(PageElement):
    """
    Represents a div element on a web page.
    """

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new Div instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(element_type="div", identifier=identifier, attribute=attribute, xpath=xpath)
