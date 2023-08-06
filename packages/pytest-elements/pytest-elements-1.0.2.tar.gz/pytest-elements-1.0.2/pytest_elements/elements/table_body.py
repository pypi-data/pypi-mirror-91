"""
Description: Represents a table body on a web page.
"""
from selenium.webdriver.common.by import By
from pytest_elements.elements.table_row import TableRow, TableRowContainer
import deprecation


class TableBody(TableRowContainer):
    """
    Represents a table body on a web page. Allows buttons to be located via different attributes
    e.g. ID or class name.
    """

    _data = None
    _data_elements = None

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new TableBody instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(
            element_type="tbody", identifier=identifier, attribute=attribute, xpath=xpath,
        )

    @deprecation.deprecated(details="Use the TableBody.rows property instead")
    def get_rows(self, refresh_data=False):
        """
        Get a list of all the rows in the table body as TableRow objects
        :param refresh_data: set True to force refresh of elements.
        :return: list of TableRow objects
        """
        if not self._data or refresh_data:
            # generate path to rows inside a tbody tag
            tr_path = self.xpath + "/tr"
            row_elements = self._wd.find_elements(By.XPATH, tr_path)
            # create TableRow objects
            self._data = []
            self._data_elements = []
            for i, tr in enumerate(row_elements):
                self._data.append(TableRow(xpath=f"{tr_path}[{i+1}]"))
                self._data_elements.append(tr)
        return self._data

    @deprecation.deprecated(details="Use the TableBody.rows property instead")
    def get_row_elements(self, refresh_data=False):
        """
        Returns the constituent rows as a list of selenium web elements
        :param refresh_data: whether or not to force refresh of elements
        :return:
        """
        self.get_rows(refresh_data=refresh_data)
        return self._data_elements
