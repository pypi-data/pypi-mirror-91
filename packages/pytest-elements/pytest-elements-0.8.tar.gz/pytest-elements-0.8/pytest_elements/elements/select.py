"""
Description: Represents a <select> element on a web page.
"""
import time
from random import randint, choice
from time import sleep

from selenium.webdriver.common.by import By
from pytest_elements.elements.form_component import FormComponent
from selenium.webdriver.support.ui import Select as SeleniumSelect
from selenium.common.exceptions import StaleElementReferenceException


class Select(FormComponent):
    def __init__(
        self, identifier=None, attribute=None, xpath=None, input_type=None, valid_start_index=0,
    ):
        """
        Construct a new Select instance,
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
        return SeleniumSelect(super().get())

    def get_attribute(self, attribute_name):
        """
        Overriding default page element get_attribute
        so we can interact w/the WebElement, not the Select,
        which does not have the get_attribute function
        """
        return super().get().get_attribute(attribute_name)

    def get_children(self, appended_xpath="/*"):
        """
        Returns a list of currently loaded child elements, found by xpath
        """
        from pytest_elements.elements.element_map import map_elements

        xpath = self.xpath + appended_xpath
        web_element_children = super().get().find_elements(By.XPATH, xpath)
        elements_and_xpaths = []
        for i, child in enumerate(web_element_children):
            child_xpath = xpath + f"[{i + 1}]"
            elements_and_xpaths.append((child, child_xpath))
        return map_elements(elements_and_xpaths)

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
        init_selected_option = self.get_value()
        options = self.get_options(valid=True)
        index_options = list(range(0, len(options)))
        try:
            selected_index = options.index(init_selected_option)
            index_options.remove(selected_index)
        except ValueError:
            pass
        new_choice = choice(index_options)
        self.accept_input(new_choice)
        new_selected_option = self.get_value()
        return new_selected_option

    def get_value(self):
        """
        Returns value of the selected option in dropdown
        """
        return self.get().first_selected_option.text

    def wait_until_fillable(self, timeout=15, poll_frequency=0.5, err_msg=None):
        """
        Special implementation for the Select:
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
