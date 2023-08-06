"""
Description: Declares the .accept_input() method used by all form components.
"""
import time

from selenium.common.exceptions import TimeoutException, InvalidElementStateException

from pytest_elements.elements.page_element import PageElement
from abc import ABC, abstractmethod


class FormComponent(PageElement, ABC):
    """
    Declares the .accept_input() method used by all form components.
    """

    def __init__(
        self, element_type=None, identifier=None, attribute=None, xpath=None, input_type=None,
    ):
        """
        Construct a new TextField instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(
            element_type=element_type, identifier=identifier, attribute=attribute, xpath=xpath,
        )
        self.input_type = input_type

    @abstractmethod
    def accept_input(self, value):
        """
        The declaration of the .accept_input() method used by all form components.
        """
        self.poll_visibility()
        pass

    @abstractmethod
    def get_value(self):
        """

        :param web_driver:
        :param value:
        :return:
        """
        pass

    def wait_until_fillable(self, timeout=15, poll_frequency=0.5, err_msg=None):
        """
        The default implementation of the .wait_until_fillable() method used by all form components.
        """
        start_time = time.time()
        if not err_msg:
            err_msg = f"The {self.__class__.__name__} element was still un-fillable after timeout expired"
        if not self.poll_clickability(timeout=timeout, poll_frequency=poll_frequency,):
            raise TimeoutException(err_msg)

        while self.get_attribute("readonly"):
            time_elapsed = time.time() - start_time
            if time_elapsed > timeout:
                raise InvalidElementStateException(
                    f"The {self.__class__.__name__} element is " f"still readonly after timeout expired."
                )
            time.sleep(poll_frequency)
        return True
