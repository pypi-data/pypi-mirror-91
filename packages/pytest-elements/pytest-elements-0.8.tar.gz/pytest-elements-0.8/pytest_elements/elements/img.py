from pytest_elements.elements.page_element import PageElement


class Img(PageElement):
    """
    Represents a IMG on a web page.
    """

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new img instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(element_type="img", identifier=identifier, attribute=attribute, xpath=xpath)

    def get_url(self):
        """
        Returns the URL which this image points to.
        """
        return self.get_attribute("src")
