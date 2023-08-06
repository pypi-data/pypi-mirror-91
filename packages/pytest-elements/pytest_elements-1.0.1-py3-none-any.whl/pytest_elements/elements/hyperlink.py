"""
Description: Represents a hyperlink on a web page.
"""
import deprecation
from pytest_elements.elements.page_element import PageElement


class Hyperlink(PageElement):
    """
    Represents a hyperlink on a web page.
    """

    @deprecation.deprecated(
        deprecated_in="2.0.7",
        removed_in="3.0",
        details="The Hyperlink class has been moved/renamed, please use the "
        " 'Anchor' class from pytest_elements.elements.anchor",
    )
    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new Hyperlink instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(element_type="a", identifier=identifier, attribute=attribute, xpath=xpath)

    def get_url(self):
        """
        Returns the URL which this link points to.
        """
        return self.get_attribute("href")
