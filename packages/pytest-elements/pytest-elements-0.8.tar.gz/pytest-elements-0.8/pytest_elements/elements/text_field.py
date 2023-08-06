"""
Description: Represents an editable text field.
"""
import time

from pytest_elements.elements.fillable_element import FillableElement
from pytest_elements.elements.form_component import FormComponent


class TextField(FillableElement, FormComponent):
    """
    Represents an editable text field. Allows fields to be located via different attributes
    e.g. ID or class name.
    """

    def __init__(self, identifier=None, attribute=None, xpath=None, input_type=None):
        """
        Construct a new TextField instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(
            element_type="input", identifier=identifier, attribute=attribute, xpath=xpath, input_type=input_type,
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

    def _check_fill(self, value):
        self.accept_input(value)
        if self.get_value() == value:
            self.accept_input("")
            return True
        return False

    def wait_until_fillable(self, timeout=15, poll_frequency=0.5, err_msg=None):
        """
        Special implementation for the dropdown:
        We need to make sure text is able to be filled in.
        """
        # first, wait for the element to not be disabled
        start_time = time.time()
        super().wait_until_fillable(timeout=timeout, poll_frequency=poll_frequency, err_msg=err_msg)
        # next, wait for our sample text to be successfully filled in
        possible_inputs = ["1", "a", "A", "*", "-", "$"]
        can_fill = any([self._check_fill(inp) for inp in possible_inputs])
        while not can_fill:
            time_elapsed = time.time() - start_time
            if time_elapsed > timeout:
                raise TimeoutError(err_msg)
            time.sleep(poll_frequency)
            can_fill = any([self._check_fill(inp) for inp in possible_inputs])
        return True
