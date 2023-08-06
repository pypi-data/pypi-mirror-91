"""
Description: Represents an HTML Section element.
"""

from pytest_elements.elements.page_element import PageElement


class Section(PageElement):
    """
    Represents an HTML Section element.
    """

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new Section instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(
            element_type="section", identifier=identifier, attribute=attribute, xpath=xpath,
        )
