"""
Description: Represents a table element on a web page.
"""
from selenium.common.exceptions import NoSuchElementException

from pytest_elements.elements.page_element import PageElement
from pytest_elements.elements.table_data import TableData
from pytest_elements.elements.table_foot import TableFoot
from pytest_elements.elements.table_row import TableRow
from pytest_elements.elements.table_head import TableHead
from pytest_elements.elements.table_body import TableBody
from typing import List, Optional, Dict
from selenium.webdriver.common.by import By
import deprecation


class Table(PageElement):
    """
    Represents a table on a web page.
    """

    _data = None
    _data_elements = None

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new Table instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(
            element_type="table", identifier=identifier, attribute=attribute, xpath=xpath,
        )

    @property
    def head(self) -> Optional[TableHead]:
        """
        Get the head of this table (if one exists)

        :return: TableHead (or None)
        """
        heads = self.get_children(appended_xpath="/thead")
        if len(heads) > 0:
            return heads[0]
        return None

    @property
    def headers(self) -> List[TableData]:
        """
        Get the head of this table (if one exists)

        :return: TableHead (or None)
        """
        head = self.head
        if head:
            return head.headers
        return []

    @property
    def body(self) -> Optional[TableBody]:
        """
        Get the body of this table (if one exists)

        :return: TableBody (or None)
        """
        # generate path
        bodies = self.get_children(appended_xpath="/tbody")
        if len(bodies) > 0:
            return bodies[0]
        return None

    @property
    def foot(self) -> Optional[TableFoot]:
        """
        Get the foot of this table (if one exists)

        :return: TableFoot (or None)
        """
        # generate path
        feet = self.get_children(appended_xpath="/tfoot")
        if len(feet) > 0:
            return feet[0]
        return None

    @property
    def text(self) -> List[List[str]]:
        """
        Return a list of lists, each representing a row in the table head, body, and foot

        [
            [ thead row 1 ], ... [ thead row N ],
            [ tbody row 1 ], ... [ tbody row N ],
            [ tfoot row 1 ], ... [ tfoot row N ],
        ]

        It is recommended to use more specific table elements before accessing the text,

        e.g. `table.body.text` or `table.head.text`

        """
        result = []
        head = self.head
        body = self.body
        foot = self.foot
        if head:
            result.extend([head.text])
        if body:
            result.extend(body.text)
        if foot:
            result.extend(foot.text)
        return result

    @property
    def rows(self) -> List[TableRow]:
        """
        Get the rows of this table (if any exist) found
        by appending "//tr" to this table's xpath.

        It is recommended to use more specific table elements before accessing the text,

        e.g. `table.body.rows`

        :return: List[TableRow]
        """
        rows: List[TableRow] = self.get_children(appended_xpath="//*[not(self::thead) and not(self::tfoot)]//tr")
        return rows

    @property
    def columns(self) -> Dict[str, List[TableData]]:
        """
        Get the columns of this table, represented by a dictionary with the
        table's header text mapped to a list of TableData elements found in the table body
        """
        columns = {}
        nameless_columns = 0
        head = self.head
        body = self.body
        if head and body:
            for c_index, th in enumerate(head.headers):
                header = th.get_text()
                if len(header) == 0:
                    header = f"nameless column {nameless_columns}"
                    nameless_columns += 1
                column = []
                for r_index, row, in enumerate(body.rows):
                    if len(row.data) >= c_index + 1:
                        column.append(row.data[c_index])
                columns[header] = column
        return columns

    @property
    def text_columns(self) -> Dict[str, List[str]]:
        """
        Get the columns of this table, represented by a dictionary with the
        table's header text mapped to a list of string elements found in the table body's rows
        represented by the header
        """
        text_columns = {}
        for header, column in self.columns.items():
            text_columns[header] = [td.get_text() for td in column]
        return text_columns

    @deprecation.deprecated(details="Use the Table.head property instead")
    def get_thead(self):
        """
        Get the head of this table (if one exists)
        :return: TableHead
        """
        # generate path
        head_path = self.xpath + "/thead"
        return TableHead(xpath=head_path)

    @deprecation.deprecated(details="Use the Table.body property instead")
    def get_tbody(self):
        """
        Get the body of this table (if one exists)
        :return: TableBody
        """
        # generate path
        head_path = self.xpath + "/tbody"
        return TableBody(xpath=head_path)

    @deprecation.deprecated(details="Use the Table.rows property instead")
    def get_rows(self, refresh_data=False):
        """
        Get a list of all the rows in the table body as TableRow objects
        :param refresh_data: set True to force refresh of elements.
        :return: list of TableRow objects
        """
        if not self._data or refresh_data:
            # generate path to rows inside a tbody tag
            tr_path = self.xpath + "/tbody/tr"
            row_elements = self._wd.find_elements(By.XPATH, tr_path)
            # check if any table rows exist outside of a tbody
            no_body_tr_path = self.xpath + "/tr"
            no_body_row_elements = self._wd.find_elements(By.XPATH, tr_path)
            self._data = []
            self._data_elements = []
            # create TableRow objects
            for i, tr in enumerate(row_elements):
                self._data_elements.append(tr)
                self._data.append(TableRow(xpath=f"{tr_path}[{i + 1}]"))
            for i, tr in enumerate(no_body_row_elements):
                self._data_elements.append(tr)
                element = TableRow(xpath=f"{no_body_tr_path}[{i + 1}]")
                try:
                    element.get_text()
                    self._data.append(element)
                except NoSuchElementException:
                    continue
        return self._data

    @deprecation.deprecated(details="Use the Table.rows property instead")
    def get_row_elements(self, refresh_data=False):
        """
        Returns the constituent rows as a list of selenium web elements
        :param refresh_data: whether or not to force refresh of elements
        :return:
        """
        return self.get_rows(refresh_data=refresh_data)
