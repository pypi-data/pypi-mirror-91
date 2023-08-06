"""
Description: Represents a table data cell on a web page.
"""

from pytest_elements.elements.page_element import PageElement


class TableData(PageElement):
    """
    Represents a table data cell on a web page
    e.g. ID or class name.
    """

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new TableData instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(element_type="td", identifier=identifier, attribute=attribute, xpath=xpath)
