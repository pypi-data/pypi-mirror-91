"""
Description: A "null element" is just a placeholder when an element is needed in a data structure, but no
corresponding element exists on the actual web page.
"""

from pytest_elements.elements.page_element import PageElement


class NullElement(PageElement):
    """
    A placeholder element which does not exist on the web page.
    """

    def __init__(self):
        """
        Constructs a PageElement with no identifier.
        """
        super().__init__()

    def selector(self):
        """
        Intentionally left un-implemented because null elements do not exist.
        """
        raise NotImplementedError("Null elements do not exist and therefore cannot be interacted with")

    def get_xpath_string(self):
        """
        Return string of xpath
        :return:
        """
        pass
