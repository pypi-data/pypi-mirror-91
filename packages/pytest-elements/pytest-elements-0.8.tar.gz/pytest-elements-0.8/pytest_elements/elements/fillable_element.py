"""
Description: Defines the .fill_out() method used by all fillable elements.
"""
from pytest_elements.elements.page_element import PageElement
from abc import ABC


class FillableElement(PageElement, ABC):
    """
    Abstract class which defines the .fill_out() method inherited by all elements which support text entry.
    """

    def fill_out(self, *value):
        """
        Enters the given value into the given input element,
        checking to ensure that the value has been entered correctly
        before returning.
        """
        element = self.get()
        element.clear()
        for i in range(3):  # Two retries are occasionally necessary - most likely due to a webdriver bug
            element.send_keys(*value)
            if element.get_attribute("value") == "".join(map(str, value)):
                return
            if i < 3:
                element.clear()
        raise RuntimeError("WebDriver was unable to correctly enter the provided value after 3 attempts")
