"""
Description: Represents any element which aggregates other elements, any of which may be selected by clicking it.
"""

from pytest_elements.elements.form_component import FormComponent
from selenium.common.exceptions import TimeoutException
from random import randint


class SelectionElement(FormComponent):
    """
    An element which aggregates other elements, any of which may be selected by clicking it.
    Useful for representing dropdown menus and tile-pickers in Forms.
    """

    def __init__(self, *options):
        """
        Constructs a new SelectionElement with the specified options.
        """
        super().__init__(None)
        self.options = options
        assert len(self.options) > 0, (
            "Error: SelectionElement created with 0 options - " "must be the result of a page defect"
        )

    def accept_input(self, value):
        """
        Selects the specified option.
        """
        if isinstance(value, int):
            if value == -1:
                self.select_by_index(randint(0, len(self.options) - 1))
            else:
                self.select_by_index(value)
        else:
            self.select_by_value(value)

    def select_by_value(self, value):
        """
        Selects the specified option by value.
        """
        for option in self.options:
            if option.identifier == value:
                try:
                    option.click()
                    return
                except TimeoutException:
                    self.select_by_index(0)
        raise ValueError(f"Unrecognized option {value} could not be selected")

    def select_by_index(self, index):
        """
        Selects the specified option by index.
        """
        try:
            self.options[index].click()
        except IndexError:
            raise ValueError("The specified index was out of range for the available options")
        except TimeoutException:
            self.select_by_index(0)

    def selector(self):
        """
        Intentionally left un-implemented because SelectionElements are not interacted with directly on the web page.
        """
        raise NotImplementedError(
            "SelectionElement instances are not interacted with directly, " "they are just a wrapper for other elements"
        )

    def __len__(self):
        """
        Returns the number of options in this element.
        """
        return len(self.options)

    def get_xpath_string(self):
        """
        Return string of xpath
        :return:
        """
        pass

    def get_value(self):
        """
        Returns value
        """
        pass
