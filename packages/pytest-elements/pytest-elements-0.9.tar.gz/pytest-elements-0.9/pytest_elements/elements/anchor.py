"""
Description: Represents an anchor/hyperlink on a web page.
"""
from pytest_elements.elements.page_element import PageElement


class Anchor(PageElement):
    """
    Represents an Anchor (`<a></a>`) tag on a web page.
    """

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new Anchor instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(element_type="a", identifier=identifier, attribute=attribute, xpath=xpath)

    def get_url(self):
        """
        Returns the URL which this anchor points to.
        """
        return self.get_attribute("href")
