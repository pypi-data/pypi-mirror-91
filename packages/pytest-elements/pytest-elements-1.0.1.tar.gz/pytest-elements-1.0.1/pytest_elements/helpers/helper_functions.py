"""
This file holds useful general methods to be used in tests.
"""
import time
from pytest_elements.page_objects.page import Page
from typing import Any
import deprecation


@deprecation.deprecated(details="Use the append_element_to_xpath in elements/page_element.py.")
def append_element_to_xpath(xpath, element_type, identifier="", attribute="", index=-1):
    """
    DEPRECATED: Moved to page_objects.py
    Append a child element to an xpath
    :param xpath: Starting xpath
    :param element_type: Type of child element to search for
    :param identifier: Identifier for child, if applicable
    :param attribute: Attribute type of child to search on, if applicable
    :param index: Index of child element to get, if applicable
    :return: String of full xpath
    """
    xpath += "/" + element_type
    if not identifier == "":
        xpath += "[contains(@" + attribute + ", '" + identifier + "')]"
    if not index == -1:
        xpath += "[" + str(index) + "]"
    return xpath


@deprecation.deprecated(details="Use the append_index_to_xpath in elements/page_element.py.")
def append_index_to_xpath(xpath, index):
    """
    DEPRECIATED: Moved to page_objects.py
    Append an index to a given xpath
    :param xpath: Xpath to append to
    :param index: Index to append
    :return: String of new xpath
    """
    return xpath + "[" + str(index) + "]"


@deprecation.deprecated(details="Use the which_page_loads in page_objects/page.py.")
def which_page_loads(*pages: Any, web_driver, timeout=15, polling=0.5):
    """
    DEPRECATED: Moved to page.py
    Determines which of the provided Page subclasses loads, if any.
    Returns an instance of the loaded Page subclass, or None if no pages load.
    :param web_driver: The WebDriver instance in which something interesting is happening
    :param timeout: The maximum time this method may wait before returning
    :param polling: How often the method should check the WebDriver for changes
    :param page_list: Page subclasses representing the set of pages which may load in the WebDriver
    :return: Page subclass or None
    """
    page_list = list(pages)
    for page_class in page_list:
        assert issubclass(page_class, Page), "Only Page subclasses are allowed as parameters"
    loaded = False
    while timeout > 0 and not loaded:
        for page_class in page_list:
            # Check if page's URL (or redirect URL) has loaded
            if (
                page_class._url if not page_class._redirect_url else page_class._redirect_url
            ) in web_driver.current_url:
                # Move matching page to the top of the list
                # Speeds up subsequent iteration, allows other pages to load later
                page_list.remove(page_class)
                page_list.insert(0, page_class)
                # Check critical elements of matching page
                for element in page_class._critical_elements:
                    if not element.is_here():
                        # The page has not loaded; return to the top of the while loop
                        time.sleep(polling)
                        timeout -= polling
                        break
                # The URL and all critical elements have loaded, return an instance of the page
                return page_class()
        # No page's URL matched; return to the top of the while loop
        time.sleep(polling)
        timeout -= polling
