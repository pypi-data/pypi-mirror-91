"""
Description: Represents a file picker.
"""
import time

from pytest_elements.elements.fillable_element import FillableElement
from pytest_elements.elements.form_component import FormComponent
from pytest_elements.helpers.xpath_creation_functions import get_generic_xpath


class FilePicker(FillableElement, FormComponent):
    """
    Represents a file picker. Allows a filepath to be entered via accept_input().
    """

    def __init__(self, identifier=None, attribute=None, xpath=None, input_type=None):
        if not xpath:
            self.xpath = get_generic_xpath("input", identifier, attribute)
            self.xpath = self.xpath[: len(self.xpath) - 1]  # Yikes. Removes last closing square bracket
            self.xpath += " and @type='file']"
        else:
            self.xpath = xpath
        super().__init__(
            element_type="input", identifier=identifier, attribute=attribute, xpath=self.xpath,
        )

    def accept_input(self, value):
        """
        Fills in the field with the given text string.
        """
        super().accept_input(value)
        self.fill_out(value)

    def get_value(self):
        """
        Returns value from textfield
        """
        return self.get_attribute("value")

    def get_text(self):
        return self.get_value()

    def fill_out(self, *value):
        """
        Enters the given value into the file picker.
        """
        element = self.get()
        element.clear()
        element.send_keys(*value)
