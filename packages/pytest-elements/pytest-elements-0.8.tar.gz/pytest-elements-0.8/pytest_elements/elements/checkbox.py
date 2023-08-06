"""
Description: Represents a checkbox button on a page.
"""
from pytest_elements.elements.form_component import FormComponent
from pytest_elements.helpers.xpath_creation_functions import get_generic_xpath


class Checkbox(FormComponent):
    """
    A checkbox on a web page.
    """

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new Checkbox (input) instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        if not xpath:
            self.xpath = get_generic_xpath("input", identifier, attribute)
            self.xpath = self.xpath[: len(self.xpath) - 1]  # Yikes. Removes last closing square bracket
            self.xpath += " and @type='checkbox']"
        else:
            self.xpath = xpath
        super().__init__(
            element_type="input", identifier=identifier, attribute=attribute, xpath=self.xpath,
        )

    def is_checked(self):
        """
        Checks whether or not the checkbox is currently checked.
        :return: True if checked, else False.
        """
        return self.get().is_selected()

    def is_not_checked(self):
        """
        Check whether or not the checkbox is currently not checked
        """
        return self.get().is_selected() is False

    def accept_input(self, check):
        """
        Allows checkboxes to be used as components of a Form.
        :param check: True to check the checkbox, False to un-check.
        :return: None
        """
        if check != self.is_checked():
            self.click()

    def get_value(self):
        """
        Checks the value if the checkbox is checked or not
        :return: True if checked, else False.
        """
        return self.is_checked()
