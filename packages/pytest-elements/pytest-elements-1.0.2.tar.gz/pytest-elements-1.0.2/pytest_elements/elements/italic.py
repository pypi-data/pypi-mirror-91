"""
Description: Represents an italic tag on a web page
DEPRECIATED: Use formatting_element.py!
"""
from pytest_elements.elements.formatting_element import FormattingElement


class Italic(FormattingElement):
    """
    Represents an italic tag on a web page
    """

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new Italic instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(element_type="i", identifier=identifier, attribute=attribute, xpath=xpath)
