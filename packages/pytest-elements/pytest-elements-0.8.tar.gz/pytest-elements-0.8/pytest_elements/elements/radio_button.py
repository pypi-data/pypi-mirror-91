"""
Description: Represents a radio button on a page
"""
from pytest_elements.elements.page_element import PageElement
from pytest_elements.helpers.xpath_creation_functions import get_generic_xpath


class RadioButton(PageElement):
    """
    Represents a radio button on a page.
    """

    def __init__(self, identifier=None, attribute="", xpath=None):
        """
        Construct a new RadioButton instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        if not xpath:
            self.xpath = get_generic_xpath("input", identifier, attribute)
            self.xpath = self.xpath[: len(self.xpath) - 1]  # Yikes. Removes last closing square bracket
            self.xpath += " and @type='radio']"
        else:
            self.xpath = xpath
        super().__init__(
            element_type="input", identifier=identifier, attribute=attribute, xpath=xpath,
        )
