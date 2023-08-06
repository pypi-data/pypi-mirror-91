"""
Description: Represents a dropdown element on a web page.
It is preferable to use this class over DropdownOption when
the exact options in a dropdown menu are unknown or the dropdown options
cannot reliably be interacted with directly.
"""
import time
import deprecation
from random import randint
from time import sleep

from pytest_elements.elements.form_component import FormComponent
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import StaleElementReferenceException


class Dropdown(FormComponent):
    """
    Represents a dropdown menu on a web page.
    """

    @deprecation.deprecated(
        deprecated_in="2.0.7",
        removed_in="3.0",
        details="The Dropdown class has been moved/renamed, please use the "
        "'Select' class from pytest_elements.elements.select",
    )
    def __init__(
        self, identifier=None, attribute=None, xpath=None, input_type=None, valid_start_index=0,
    ):
        """
        Construct a new Dropdown instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        :param valid_start_index: Start random selection of index from this value, in case the specific drop down
        contains and invalid start index at 0.

        """
        super().__init__(
            element_type="select", identifier=identifier, attribute=attribute, xpath=xpath, input_type=input_type,
        )
        self.valid_start_index = valid_start_index

    def get(self):
        """
        Returns the element as a Selenium Select element.
        """
        return Select(super().get())

    def get_attribute(self, attribute_name):
        """
        Overriding default page element get_attribute
        so we can interact w/the WebElement, not the Select,
        which does not have the get_attribute function
        """
        return super().get().get_attribute(attribute_name)

    def get_len(self, valid=False):
        """
        Returns the number of options
        :param valid: whether or not to only return the # of valid options
        """
        if valid:
            return len(self.get().options) - self.valid_start_index
        else:
            return len(self.get().options)

    def get_options(self, valid=False):
        """
        :param valid: whether or not to return only the valid options
        :return: a list of strings representing the options in the dropdown
        """
        if valid:
            options = [o.text for o in self.get().options]
            return options[self.valid_start_index :]
        else:
            return [o.text for o in self.get().options]

    def accept_input(self, value):
        """
        Selects the option with the specified value.
        """
        if isinstance(value, int):
            if value < 0:
                return self.pick_random()
            else:
                self.get().select_by_index(value)
        else:
            self.get().select_by_visible_text(value)
            return value

    def pick_random(self, ensure_change=False):
        """
        Selects a random option and returns the text of the option
        :param ensure_change: attempt to select a value that was not previously selected
        :return the text value of the newly selected option
        """
        attempts = 0
        while attempts < 5:
            try:
                if ensure_change:
                    return self._ensure_change()
                else:
                    index = randint(self.valid_start_index, self.get_len() - 1)
                    self.accept_input(index)
                    return self.get().first_selected_option.text
            except StaleElementReferenceException:
                attempts += 1
                sleep(1)

    def _ensure_change(self):
        """
        Attempt to select a value that was not previously selected
        :return:
        """
        init_selected_option = self.get().first_selected_option.text
        attempts = self.get_len(valid=True)
        new_selected_option = ""
        while init_selected_option == new_selected_option and attempts > 0:
            index = randint(self.valid_start_index, self.get_len() - 1)
            self.accept_input(index)
            new_selected_option = self.get().first_selected_option.text
            attempts -= 1
        assert new_selected_option != init_selected_option, (
            "A new value could not be randomly selected from this dropdown. "
            "Are there enough valid, unique values to ensure a change? (>1 valid values required)\n"
            f"Options: {self.get_options()}"
        )
        return new_selected_option

    def get_value(self):
        """
        Returns value of the selected option in dropdown
        """
        return self.get().first_selected_option.text

    def wait_until_fillable(self, timeout=15, poll_frequency=0.5, err_msg=None):
        """
        Special implementation for the dropdown:
        We need to make sure there is a valid option to be selected.
        """
        # first, wait for the element to not be disabled
        start_time = time.time()
        super().wait_until_fillable(timeout=timeout, poll_frequency=poll_frequency, err_msg=err_msg)
        # next, wait for there to be at least one valid selectable option
        while self.get_len(valid=True) == 0:
            time_elapsed = time.time() - start_time
            if time_elapsed > timeout:
                raise TimeoutError(err_msg)
            time.sleep(poll_frequency)
        return True
