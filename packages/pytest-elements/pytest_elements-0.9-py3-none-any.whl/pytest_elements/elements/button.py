"""
Description: Represents a button on a web page.
"""

from pytest_elements.elements.form_component import FormComponent


class Button(FormComponent):
    """
    Represents a button on a web page. Allows buttons to be located via different attributes
    e.g. ID or class name.
    """

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new Button instance,
        located using the specified attribute and identifier OR a supplied xpath.
        """
        super().__init__(
            element_type="button", identifier=identifier, attribute=attribute, xpath=xpath,
        )

    def accept_input(self, value):
        """
        Allows buttons to be used as components of a Form.
        """
        super().accept_input(value)
        if value:
            self.click()

    def get_value(self):
        """
        Returns the text of a button
        """
        return self.get_text()
