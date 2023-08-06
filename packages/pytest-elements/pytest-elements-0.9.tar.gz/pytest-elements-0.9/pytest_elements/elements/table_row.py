"""
Description: Represents a table row (tr) on a web page.
"""
from abc import ABC
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from pytest_elements.elements.page_element import PageElement
from pytest_elements.elements.table_data import TableData
from typing import List
import deprecation


class TableRow(PageElement):
    """
    Represents a table row on a web page. Allows buttons to be located via different attributes
    e.g. ID or class name.
    """

    _data = None
    _data_elements = None

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new TableRow instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(element_type="tr", identifier=identifier, attribute=attribute, xpath=xpath)

    @property
    def data(self) -> List[TableData]:
        """
        Get a list of the TableData elements in this row
        """
        return self.get_children(appended_xpath="/td")  # List[TableData]

    @property
    def text(self) -> List[str]:
        result = []
        for data in self.data:
            try:
                result.append(data.get_text())
            except NoSuchElementException:
                result.append("")
        return result

    @deprecation.deprecated(details="Use the TableRow.data property instead")
    def get_data(self, refresh_data=False):
        """
        Get a list of all the data in the table header as TableData objects
        :param refresh_data: set True to force refresh of elements.
        :return: list of TableData objects (or selenium web elements) in this row
        """
        if not self._data or refresh_data:
            td_path = self.xpath + "/td"
            self._data_elements = self._wd.find_elements(By.XPATH, td_path)
            self._data = []
            for i, td in enumerate(self._data_elements):
                self._data.append(TableData(xpath=f"{td_path}[{i+1}]"))
        return self._data

    @deprecation.deprecated(details="Use the TableRow.data property instead")
    def get_data_elements(self, refresh_data=False):
        """
         Returns the constituent table data cells as a list of selenium web elements
         :param refresh_data: whether or not to force refresh of elements
         :return:
         """
        self.get_data(refresh_data=refresh_data)
        return self._data_elements


class TableRowContainer(PageElement, ABC):
    @property
    def rows(self) -> List[TableRow]:
        # generate path to rows inside a tbody tag
        rows: List[TableRow] = self.get_children(appended_xpath="//tr")
        return rows

    @property
    def text(self) -> List[List[str]]:
        return [row.text for row in self.rows]
