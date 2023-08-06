"""
Description: Represents an editable date picker which accepts date strings
in the format "MM/DD/YYYY"
"""
import time
from datetime import date

from pytest_elements.elements.fillable_element import FillableElement
from pytest_elements.elements.form_component import FormComponent
from pytest_elements.helpers.xpath_creation_functions import get_generic_xpath
from selenium.webdriver.common.keys import Keys


class DatePicker(FillableElement, FormComponent):
    """
    Represents an editable date picker which accepts date strings
    in the format "MM/DD/YYYY"
    """

    def __init__(self, identifier=None, attribute=None, xpath=None, input_type=None):
        """
        Construct a new DatePicker instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        if not xpath:
            self.xpath = get_generic_xpath("input", identifier, attribute)
            self.xpath = self.xpath[: len(self.xpath) - 1]  # Yikes. Removes last closing square bracket
            self.xpath += " and @type='date']"  # Only select date pickers, not other input elemenrs.
        else:
            self.xpath = xpath
        super().__init__(
            element_type="input", identifier=identifier, attribute=attribute, xpath=self.xpath,
        )

    def fill_out(self, *values):
        """
        Enters the given date object into the date picker,
        checking to ensure that the value has been entered correctly
        before returning.
        """
        value = list(values).pop()
        element = self.get()
        element.clear()
        for i in range(3):  # Two retries are occasionally necessary - most likely due to a webdriver bug
            element.click()
            element.send_keys(value.strftime("%Y"))
            element.send_keys(Keys.ARROW_LEFT)
            element.send_keys(value.strftime("%d"))
            element.send_keys(Keys.ARROW_LEFT)
            element.send_keys(Keys.ARROW_LEFT)
            element.send_keys(value.strftime("%m"))
            if self.get_date() == value:
                return
            i -= 1
            if i < 3:
                element.clear()
        raise RuntimeError("WebDriver was unable to correctly enter the provided value after 3 attempts")

    def accept_input(self, value):
        """
        Fills in the field with the given text string.
        """
        self.poll_visibility()
        self.fill_out(value)

    def get_value(self):
        """
        Returns value from textfield
        """
        return self.get_attribute("value")

    def get_date(self):
        """
        Returns a Python date object useful for date comparisons in tests.
        """
        return date.fromisoformat(self.get_value())

    def _check_fill(self, value):
        original_value = self.get_date()
        self.accept_input(value)
        if self.get_date() == value:
            self.accept_input(original_value)
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
        # next, wait for our sample date to be successfully filled in
        while not self._check_fill(date(1993, 8, 3)):
            time_elapsed = time.time() - start_time
            if time_elapsed > timeout:
                raise TimeoutError(err_msg)
            time.sleep(poll_frequency)
        return True
