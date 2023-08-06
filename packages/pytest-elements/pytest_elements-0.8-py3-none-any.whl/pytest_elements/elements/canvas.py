"""
Description: Represents a graphics element on a web page.
"""
from pytest_elements.elements.page_element import PageElement


class Canvas(PageElement):
    """
    Represents a graphic element on a page.
    """

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new Canvas instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(
            element_type="canvas", identifier=identifier, attribute=attribute, xpath=xpath,
        )
