"""
Description: Ancestor to all pages in the Page Object family.
Contains selectors and methods common to all pages.
"""
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException
import selenium.webdriver.support.expected_conditions as ec
from pytest_elements import get_driver
import time
import logging
import os
from typing import List
from pytest_elements.elements.page_element import PageElement


def allow_retry_for_method(action, *action_args, attempts=3, loop_delay=5):
    """
    Allows the user to pass in a function; if it throws an exception, it will wait the given delay and retry.
    This method should be used to allow specific actions within a test method to retry;
    this isn't designed for just passing in a test method.
    :param action: Method for the action within test to allow retries for
    :param action_args: arguments which get passed into the function passed in for param action
    :param attempts:number of attempts before raising exception
    :param loop_delay: time between retries
    :return:
    """
    success = False
    while attempts > 0 and not success:
        try:
            action(*action_args)
            success = True
        except Exception as e:
            print(f"Exception {type(e).__name__} was caught with message: {e}")
            attempts -= 1
            if attempts > 0:
                print(f"Retrying... Attempts left: {attempts}")
                time.sleep(loop_delay)
            else:
                raise e


def which_page_loads(*pages, web_driver, timeout=15, polling=0.5):
    """
    Determines which of the provided Page subclasses loads, if any.
    Returns an instance of the loaded Page subclass, or None if no pages load.
    :param web_driver: The WebDriver instance in which something interesting is happening
    :param timeout: The maximum time this method may wait before returning
    :param polling: How often the method should check the WebDriver for changes
    :param pages: Page subclasses representing the set of pages which may load in the WebDriver
    :return: Page subclass or None
    """
    pages = list(pages)
    for page_class in pages:
        assert issubclass(page_class, Page), "Only Page subclasses are allowed as parameters"

    assumed_loaded = False
    while timeout > 0 and not assumed_loaded:
        for page_class in pages:
            # Check if page's URL (or redirect URL) has loaded
            page_url = page_class._url
            redirect_url = page_class._redirect_url
            if (page_url if not redirect_url else redirect_url) in web_driver.current_url:
                logging.info(f"Loading page at {page_url}")

                # Move matching page to the top of the list
                # Speeds up subsequent iteration, allows other pages to load later
                pages.remove(page_class)
                pages.insert(0, page_class)

                # Check critical elements of matching page
                critical_elements = page_class._critical_elements
                for element in critical_elements:
                    if not element.is_here():
                        # The page has not loaded; return to the top of the while loop
                        time.sleep(polling)
                        timeout -= polling
                        logging.info(f"{page_class} not fully loaded at {page_url}")
                        break

                # The URL and all critical elements have loaded, return an instance of the page
                logging.info(f"{page_class} fully loaded at {page_url}")
                return page_class()

        # No page's URL matched; return to the top of the while loop
        time.sleep(polling)
        timeout -= polling


class Page:
    """
    A generic page.
    """

    # Selectors common to all pages

    # The single most important part of any page, I'd say
    _root_element_tag = "html"

    _url = None
    _redirect_url = None
    _load_time = 15  # 15 seems to be the more common time out than 10
    _critical_elements: List["PageElement"] = []  # In page object files create populated lists
    _pre_loaded = True

    @property
    def _wd(self):
        return get_driver(os.environ.get("AF_DRIVER_KEY", "default"))

    @property
    def url(self):
        """
        The url to this page
        """
        return self._url

    @property
    def redirect_url(self):
        """
        A url that this page may redirect to
        """
        return self._redirect_url

    @property
    def load_time(self):
        """
        The time (in seconds) allowed for this page to completely
        load (all critical elements present).

        Default: 10
        """
        return self._load_time

    @property
    def critical_elements(self):
        """
        An array of PageElements that must be present for this page to be considered "loaded"
        """
        return self._critical_elements

    @property
    def pre_loaded(self):
        """
        if True - do not navigate to this page's url or
                  check for critical elements, as it should already be loaded
        """
        return self._pre_loaded

    def __init__(
        self, url=None, redirect_url=None, load_time=None, critical_elements=None, pre_loaded=None,
    ):
        """
        Constructor for all page objects.
        Verifies that the webpage it represents has loaded in the browser.
        """

        # If params are not None, we should set the class's params as we're being called by a subclass
        # Deprecated logic; exists for backwards compatibility with classes that define __init__ (which is
        # no longer strictly necessary).
        if pre_loaded is not None:
            self._pre_loaded = pre_loaded
        if url is not None:
            self._url = url
        if redirect_url is not None:
            self._redirect_url = redirect_url
        if critical_elements is not None:
            self._critical_elements = critical_elements
        if load_time is not None:
            self._load_time = load_time

        # Load the page if the caller has not already done so
        if not self._pre_loaded:
            self._go()
        else:
            # Wait until the page has loaded
            self._is_here()

    def _go(self):
        """
        Loads the webpage represented by this page object and verifies that the page loads correctly.
        :return: None
        """
        logging.info(f"Going to {self._url}")
        self._wd.get(self._url)
        self._is_here()

    def _is_here(self, wait_for_elements=None):
        """
        Verifies that the webpage represented by this page object has loaded.
        Checks for the presence of the webpage's URL as well as the presence
        of all of the webpage's 'critical elements'.
        """
        start_time = time.time()

        try:
            # Wait to see if the correct URL loaded
            WebDriverWait(self._wd, self._load_time).until(
                # Note: I chose to use 'in' instead of ec.url_matches because url_matches is unreliable,
                # and 'in' will match urls that have parameters on the end.
                lambda _: (self._url if not self._redirect_url else self._redirect_url)
                in self._wd.current_url
            )
        except TimeoutException:
            # catch and re-raise so we get an error message with the correct current_url
            raise TimeoutException(
                f"The WebDriver did not finish on the correct URL for page {self.__class__.__name__}.\n"
                f"Expected: {self._url if not self._redirect_url else self._redirect_url}\n"
                f"Actual: {self._wd.current_url}"
            )

        # Calculate time remaining for page to load
        load_time_remaining = self._load_time - (time.time() - start_time)

        # Collect VIP elements
        vip_elements = [
            element.selector() for element in (wait_for_elements if wait_for_elements else self._critical_elements)
        ]
        stragglers = vip_elements
        # Ensure that enough time remains to check all elements
        # and that there are elements remaining to look for
        while stragglers and load_time_remaining > 0:
            loop_start_time = time.time()
            # Wait for the VIPs to arrive
            stragglers = [
                selector[1]
                # Always check for all elements to ensure they are all present at the same time
                for selector in vip_elements
                if not self._wd.find_elements(*selector)
            ]
            # Give the page a chance to load between checks
            time.sleep(0.5)
            load_time_remaining -= time.time() - loop_start_time
        if stragglers:
            error_msg = "\n".join(stragglers)
            raise TimeoutException(
                f"Page {self.__class__.__name__} did not load within the expected time of {self._load_time} seconds.\n"
                f"The following element(s) failed to load:\n"
                f"{error_msg}"
            )

    def _wait_refresh(self, wait_for_elements=None):
        """
        Waits for the page to refresh before continuing.
        """
        logging.info(f"Refresh initiated on {self._url}")
        page = self._wd.find_element_by_tag_name(self._root_element_tag)
        WebDriverWait(self._wd, self._load_time).until(ec.staleness_of(page))
        self._is_here(wait_for_elements)

    def refresh(self, wait_for_elements=None):
        """
        Refreshes the page
        :return:
        """
        page = self._wd.find_element_by_tag_name(self._root_element_tag)
        self._wd.get(self._url)
        WebDriverWait(self._wd, self._load_time).until(ec.staleness_of(page))
        self._is_here(wait_for_elements)
        logging.info(f"Refresh complete on {self._url}")
        return self
