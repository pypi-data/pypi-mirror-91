"""
Description: Represents a table header on a web page.
"""
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pytest_elements.elements.page_element import PageElement
from pytest_elements.elements.table_data import TableData
from typing import List
import deprecation


class TableHead(PageElement):
    """
    Represents a table header on a web page. Allows buttons to be located via different attributes
    e.g. ID or class name.
    """

    _data = None

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new TableHead instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(
            element_type="thead", identifier=identifier, attribute=attribute, xpath=xpath,
        )

    @property
    def headers(self) -> List[TableData]:
        """
        Returns a list of the direct descendents of this header's tr
        (use only when the header structure is typical thead -> single tr -> th's,
        otherwise use the data property)
        """
        return self.get_children(appended_xpath="//tr/th")

    @property
    def text(self) -> List[str]:
        """
        Returns a list of the direct descendents of this header's tr
        (use only when the header structure is not typical thead -> single tr -> th's,
        otherwise use the headers property)
        """
        return [th.get_text() for th in self.headers]

    @property
    def data(self) -> List[TableData]:
        """
        Returns a list of the direct descendents of this header's tr
        (use only when the header structure is not typical thead -> single tr -> th's,
        otherwise use the headers property)
        """
        return self.get_children(appended_xpath="//tr/*")

    @deprecation.deprecated(details="Use the TableHead.data property instead")
    def get_data(self, refresh_data=False):
        """
        Get a list of all the th/td elements in the thead as TableData objects
        :param refresh_data: set True to force refresh of elements.
        :return: list of TableData objects in this TableHead
        """
        if not self._data or refresh_data:
            td_path = self.xpath + "/tr/td"
            th_path = self.xpath + "/tr/th"
            td_elements = self._wd.find_elements(By.XPATH, td_path)
            th_elements = self._wd.find_elements(By.XPATH, th_path)
            self._data = []
            for i, td in enumerate(td_elements):
                self._data.append(TableData(xpath=f"{td_path}[{i + 1}]"))
            for i, th in enumerate(th_elements):
                self._data.append(TableData(xpath=f"{th_path}[{i + 1}]"))
        return self._data
