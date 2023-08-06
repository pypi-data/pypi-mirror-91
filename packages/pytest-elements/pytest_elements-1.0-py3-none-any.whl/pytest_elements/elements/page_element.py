"""
Description: Defines properties and actions common to all Page Element types.
"""
import logging
import os
from abc import ABC
from selenium.common.exceptions import (
    TimeoutException,
    ElementNotVisibleException,
    ElementNotInteractableException,
    InvalidElementStateException,
)
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.expected_conditions import (
    element_to_be_clickable,
    visibility_of_element_located,
)
from pytest_elements import get_driver
from pytest_recorder.screenshot import take_screenshot
from pytest_recorder.hooks import attach_file_to_log
from pytest_elements.helpers.xpath_creation_functions import get_generic_xpath
from time import sleep


class PageElement(ABC):
    """
    Generic page element, to be extended by all other element classes.
    """

    @property
    def _wd(self):
        return get_driver(os.environ.get("AF_DRIVER_KEY", "default"))

    def __init__(self, element_type=None, identifier=None, attribute=None, xpath=None):
        """
        Construct a basic page element with references to parent(s) and child(ren) elements.
        :param xpath: The string value of the xpath to the element
        """
        self.identifier = identifier
        self.attribute = attribute
        if not xpath and (element_type and identifier and attribute):
            self.xpath = get_generic_xpath(element_type, identifier, attribute)
        elif xpath:
            self.xpath = xpath
        else:
            self.xpath = ""
        # Element relationship variables
        self.prev_set = []
        self.next_set = []
        self.prev_node = None
        self.next_node = None

    def selector(self):
        """
        Selector used to uniquely identify the element on a web page.
        """
        return By.XPATH, self.xpath

    def get_xpath_string(self):
        """
        Return string of xpath
        """
        return self.xpath

    def get(self):
        """
        Retrieves the Selenium WebElement represented by this PageElement.
        """
        return self._wd.find_element(*self.selector())

    def get_children(self, appended_xpath="/*"):
        """
        Returns a list of currently loaded child elements, found by xpath
        """
        from pytest_elements.elements.element_map import map_elements

        xpath = self.xpath + appended_xpath
        web_element_children = self.get().find_elements(By.XPATH, xpath)
        elements_and_xpaths = []
        for i, child in enumerate(web_element_children):
            child_xpath = xpath + f"[{i + 1}]"
            elements_and_xpaths.append((child, child_xpath))
        return map_elements(elements_and_xpaths)

    def get_attribute(self, attribute_name):
        """
        Get the attribute of a given element through selenium
        """
        return self.get().get_attribute(attribute_name)

    def get_text(self):
        """
        Get the text of a given element through selenium
        """
        return self.get().text

    def get_css_property(self, css_property):
        """
        Get the given css property value of an element through selenium
        """
        return self.get().value_of_css_property(css_property)

    def is_here(self):
        """
        Determines how many instances of the element are present and enabled on the page.
        """
        return (
            len(
                [
                    element
                    for element in self._wd.find_elements(*self.selector())
                    if element.is_enabled() and element.is_displayed()
                ]
            )
            > 0
        )

    def is_enabled(self):
        """
        Determines whether or not the element is enabled on the page.
        """
        return self.get().is_enabled()

    def is_visible(self):
        """
        Determines whether or not the element is displayed on the page.
        """
        return self._wd.find_element(*self.selector()).is_displayed()

    def click(self):
        """
        Clicks on the element
        """
        ActionChains(self._wd).move_to_element(self.get()).perform()
        self.get().click()

    def click_when_ready(self, timeout=10, poll_frequency=0.5, err_msg=None):
        """
        Waits for the element to become clickable, then clicks it.
        Raises ElementNotInteractable/ElementNotVisible exception on failure.
        """
        if not err_msg:
            err_msg = f"The {self.__class__.__name__} element never became clickable"
        if not self.poll_clickability(timeout=timeout, poll_frequency=poll_frequency):
            if not self.poll_visibility(timeout=timeout, poll_frequency=poll_frequency):
                raise ElementNotVisibleException(err_msg)
            screenshot = take_screenshot(web_driver=self._wd, highlight_element=self)
            attach_file_to_log(
                screenshot, msg="Screenshot captured on click failure: ", log_method=logging.error,
            )
            raise ElementNotInteractableException(err_msg)
        self.click()

    def wait_for_children(
        self, n=1, appended_xpath="/*", timeout=10, poll_frequency=0.5, err_msg=None,
    ):
        """
        Waits for n direct children, throwing a timeout error if enough children are not found
        """
        children = self.get_children(appended_xpath=appended_xpath)
        while len(children) < n:
            if timeout > 0:
                sleep(poll_frequency)
                timeout -= poll_frequency
                children = self.get_children(appended_xpath=appended_xpath)
            else:
                if not err_msg:
                    err_msg = (
                        f"Could not gather the expected # of elements ({n})"
                        f" with the xpath {self.xpath + appended_xpath}. {len(children)} elements were found."
                    )
                raise TimeoutError(err_msg)
        return children

    def wait_until_not_clickable(self, timeout=10, poll_frequency=0.5, err_msg=None):
        """
        Waits for the element to become unclickable.
        Raises ElementNotInteractable exception on failure.
        """
        if not err_msg:
            err_msg = (
                f"The {self.__class__.__name__} element was still clickable after timeout expired,"
                f"expected to not be clickable"
            )
        if not self.poll_clickability(timeout=timeout, poll_frequency=poll_frequency, clickable=False,):
            raise TimeoutException(err_msg)

    def wait_until_visible(self, timeout=10, poll_frequency=0.5, err_msg=None):
        """
        Waits for the element to become visible. Raises ElementNotVisible exception on failure.
        """
        if not err_msg:
            err_msg = f"The {self.__class__.__name__} element never became visible"
        if not self.poll_visibility(timeout=timeout, poll_frequency=poll_frequency):
            raise ElementNotVisibleException(err_msg)

    def wait_until_not_visible(self, timeout=10, poll_frequency=0.5, err_msg=None):
        """
        Waits for the element to become invisible. Raises InvalidElementStateException exception on failure.
        """
        if not err_msg:
            err_msg = f"The {self.__class__.__name__} element never became invisible"
        if not self.poll_visibility(timeout=timeout, poll_frequency=poll_frequency, visible=False,):
            raise InvalidElementStateException(err_msg)

    def wait_until_css_property_is(
        self, css_property: str, target_value: str, timeout=10, poll_frequency=0.5, err_msg=None,
    ):
        """
        Waits for the element's given css property to change to the given value,
        raises InvalidElementStateException if the timeout is exceeded.
        """
        if not err_msg:
            err_msg = f"The {self.__class__.__name__} element's {css_property} never became {target_value}"

        current_value = self.get_css_property(css_property)

        while current_value != target_value:
            if timeout <= 0:
                raise InvalidElementStateException(err_msg)
            sleep(poll_frequency)
            timeout -= poll_frequency
            current_value = self.get_css_property(css_property)

    def wait_until_css_property_is_not(
        self, css_property: str, value: str, timeout=10, poll_frequency=0.5, err_msg=None,
    ):
        """
        Waits for the element's given css property to change from the given value,
        raises InvalidElementStateException if the timeout is exceeded.
        """
        if not err_msg:
            err_msg = f"The {self.__class__.__name__} element's {css_property} never changed from {value}"

        current_value = self.get_css_property(css_property)

        while current_value == value:
            if timeout <= 0:
                raise InvalidElementStateException(err_msg)
            sleep(poll_frequency)
            timeout -= poll_frequency
            current_value = self.get_css_property(css_property)

    def wait_until_attribute_is(
        self, attribute: str, target_value: str, timeout=10, poll_frequency=0.5, err_msg=None,
    ):
        """
         Waits for the element's given attribute to change to the given value,
         raises InvalidElementStateException if the timeout is exceeded.
         """
        if not err_msg:
            err_msg = f"The {self.__class__.__name__} element's {attribute} never changed to {target_value}"

        current_value = self.get_attribute(attribute)

        while current_value != target_value:
            if timeout <= 0:
                raise InvalidElementStateException(err_msg)
            sleep(poll_frequency)
            timeout -= poll_frequency
            current_value = self.get_attribute(attribute)

    def wait_until_attribute_is_not(self, attribute: str, value: str, timeout=10, poll_frequency=0.5, err_msg=None):
        """
        Waits for the element's given attribute to change from the given value,
        raises InvalidElementStateException if the timeout is exceeded.
        """
        if not err_msg:
            err_msg = f"The {self.__class__.__name__} element's {attribute} never changed from {value}"

        current_value = self.get_attribute(attribute)

        while current_value == value:
            if timeout <= 0:
                raise InvalidElementStateException(err_msg)
            sleep(poll_frequency)
            timeout -= poll_frequency
            current_value = self.get_attribute(attribute)

    def find(self, selector):
        """
        Returns a list of all elements within this element which can be located with the given selector.
        """
        return self.get().find_elements(*selector)

    @staticmethod
    def get_element_from_xpath(xpath):
        """
        Get a selenium element by given xpath
        """
        return By.XPATH, xpath

    def poll_visibility(self, visible=True, timeout=15, poll_frequency=0.5):
        """
        An expectation waiting that the given element is visible (displayed & not 0x0 size)
        """
        try:
            if visible is False:
                WebDriverWait(self._wd, timeout, poll_frequency).until_not(
                    visibility_of_element_located(self.selector())
                )
            else:
                WebDriverWait(self._wd, timeout, poll_frequency).until(visibility_of_element_located(self.selector()))
        except TimeoutException:
            return False
        return True

    def poll_clickability(self, clickable=True, timeout=15, poll_frequency=0.5):
        """
        An expectation waiting that the given element is clickable or not (displayed & not 0x0 size)
        """
        try:
            if clickable is False:
                WebDriverWait(self._wd, timeout, poll_frequency).until_not(element_to_be_clickable(self.selector()))
            else:
                WebDriverWait(self._wd, timeout, poll_frequency).until(element_to_be_clickable(self.selector()))
        except TimeoutException:
            return False
        return True

    def append_element_to_xpath(self, element_type, identifier="", attribute="", index=-1):
        """
        Append a child element to an xpath
        This method will not append the element to this instance's xpath outside the scope of this function.
        :param element_type: Type of child element to search for
        :param identifier: Identifier for child, if applicable
        :param attribute: Attribute type of child to search on, if applicable
        :param index: Index of child element to get, if applicable
        :return: String of full xpath
        """
        xpath = self.xpath
        xpath += "/" + element_type
        if not identifier == "":
            xpath += "[contains(@" + attribute + ", '" + identifier + "')]"
        if not index == -1:
            xpath += "[" + str(index) + "]"
        return xpath

    def append_index_to_xpath(self, index):
        """
        Append an index to a given xpath
        This method will not append the element to this instance's xpath outside the scope of this function.
        :param index: Index to append
        :return: String of new xpath
        """
        return self.xpath + "[" + str(index) + "]"
