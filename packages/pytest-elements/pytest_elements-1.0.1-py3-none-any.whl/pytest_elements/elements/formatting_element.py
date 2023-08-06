"""
Description: Represents a formatting element tag on a web page
"""

from pytest_elements.elements.page_element import PageElement


class FormattingElement(PageElement):
    """
    Represents a formatting element tag on a web page
    """

    def __init__(self, element_type=None, identifier=None, attribute=None, xpath=None):
        """
        Construct a new FormattingElement instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(
            element_type=element_type, identifier=identifier, attribute=attribute, xpath=xpath,
        )
