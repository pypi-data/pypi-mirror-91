"""
Description: Represents a label on a web page.
"""

from pytest_elements.elements.form_component import FormComponent


class Label(FormComponent):
    """
    Represents a label on a web page. Allows labels to be located via different attributes
    e.g. ID or class name.
    """

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new Label instance,
        located using the specified attribute and identifier OR a supplied xpath.
        """
        super().__init__(
            element_type="label", identifier=identifier, attribute=attribute, xpath=xpath,
        )

    def accept_input(self, value):
        """
        Allows labels to be used as components of a Form.
        """
        super().accept_input(value)
        if value:
            self.click()

    def get_value(self):
        """
        Returns the text of a label
        """
        return self.get_text()
