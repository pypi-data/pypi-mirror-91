"""
Helper functions to get data from tables
"""

from pytest_elements.helpers.xpath_creation_functions import get_child_element_from_parent
from pytest_elements.elements.table_row import TableRow
from pytest_elements.elements.table_data import TableData
from pytest_elements.elements.table_body import TableBody
from pytest_elements.elements.table_head import TableHead


##########################
# ## Getters by Value ## #
##########################


def _get_data_from_text(
    wd, search_text, table_identifier="", table_attribute="", column_index=-1, column_header="", type="tr",
):
    matches = list()
    if column_header == "" and column_index == -1:
        # Search entire table
        tbody_xpath = get_child_element_from_parent("table", "tbody", table_identifier, table_attribute)
        tbody = TableBody(xpath=tbody_xpath)
        rows = tbody.get_rows(wd, refresh_data=True)
        for row in rows:
            tds = row.get_data(wd, refresh_data=True)
            for cell in tds:
                text = cell.get_text(wd)
                if text == search_text:
                    if type == "tr":
                        matches.append(TableRow(xpath=cell.xpath + "/.."))
                    else:
                        matches.append(cell)
    else:
        # Search tds for matching text
        tds = get_tds_by_column(wd, table_identifier, table_attribute, column_index, column_header)
        for cell in tds:
            text = cell.get_text(wd)
            if text == search_text:
                if type == "tr":
                    matches.append(TableRow(xpath=cell.xpath + "/.."))
                else:
                    matches.append(cell)
    return matches


def get_tr_from_text(
    wd, search_text, table_identifier="", table_attribute="", column_index=-1, column_header="",
):
    """
    Get the TableRow element(s) containing the search text
    :param wd: Web driver
    :param search_text: Search text to look for
    :param table_identifier: Value in the value-attribute pair for the table to search in
    :param table_attribute: Attribute in the value-attribute pair for the table to search in
    :param column_index: (Optional) Index to search for text in
    :param column_header: (Optional) Column header to search for text in- takes precedence over column_index
    :return: List of TableRow elements with given search text
    """
    return _get_data_from_text(wd, search_text, table_identifier, table_attribute, column_index, column_header, "tr",)


def get_td_from_text(
    wd, search_text, table_identifier="", table_attribute="", column_index=-1, column_header="",
):
    """
    Get the TableData element(s) containing the search text
    :param wd: Web driver
    :param search_text: Search text to look for
    :param table_identifier: Value in the value-attribute pair for the table to search in
    :param table_attribute: Attribute in the value-attribute pair for the table to search in
    :param column_index: (Optional) Index to search for text in
    :param column_header: (Optional) Column header to search for text in- takes precedence over column_index
    :return: List of TableData element(s) with given search text
    """
    return _get_data_from_text(wd, search_text, table_identifier, table_attribute, column_index, column_header, "td",)


def get_tds_by_column(wd, table_identifier="", table_attribute="", column_index=-1, column_header=""):
    """
    Get all the TableData element(s) in a given column in a table
    :param wd: Web driver
    :param table_identifier: Value in the value-attribute pair for the table to search in
    :param table_attribute: Attribute in the value-attribute pair for the table to search in
    :param column_index: (Optional) Index to search for text in
    :param column_header: (Optional) Column header to search for text in- takes precedence over column_index
    :return: List of TableData element(s) in given column
    """
    if table_identifier == "" or table_attribute == "":
        print("Please identify table value-attribute pair")
        return []
    if column_index == -1 and column_header == "":
        print("Please provide method to search for column")
        return []

    # If given the column header:
    if column_index == -1 and column_header != "":
        thead = TableHead(xpath=get_child_element_from_parent("table", "thead", table_identifier, table_attribute))
        column_index = 0
        tds = thead.get_data(wd, refresh_data=True)
        for cell in tds:
            column_index += 1
            if cell.get_text(wd) == column_header:
                break

    tbody_xpath = get_child_element_from_parent("table", "tbody", table_identifier, table_attribute)
    tbody = TableBody(xpath=tbody_xpath)
    rows = tbody.get_rows(wd, refresh_data=True)
    tds = list()
    for tr in range(0, len(rows)):
        index = tr + 1
        tds.append(TableData(xpath=tbody_xpath + "/tr[" + str(index) + "]/td[" + str(column_index) + "]"))
    return tds


###########################
# ## Getters by Parent ## #
###########################
"""
Get table elements by their parent elements.
:param parent_identifier: Parent value in value-attribute pair to search in
:param parent_attribute: Parent attribute in value-attribute pair to search in
:param child_identifier: Child value in value-attribute pair to search in
:param child_attribute: Child attribute in value-attribute pair to search in
:return: Requested element, if any
"""


def get_thead_from_table(
    parent_identifier="", parent_attribute="id", child_identifier="", child_attribute="class",
):
    return TableHead(
        xpath=get_child_element_from_parent(
            "table", "thead", parent_identifier, parent_attribute, child_identifier, child_attribute,
        )
    )


def get_tbody_from_table(
    parent_identifier="", parent_attribute="id", child_identifier="", child_attribute="class",
):
    return TableBody(
        xpath=get_child_element_from_parent(
            "table", "tbody", parent_identifier, parent_attribute, child_identifier, child_attribute,
        )
    )


def get_tr_from_thead(
    parent_identifier="", parent_attribute="id", child_identifier="", child_attribute="class",
):
    return TableRow(
        xpath=get_child_element_from_parent(
            "thead", "tr", parent_identifier, parent_attribute, child_identifier, child_attribute,
        )
    )


def get_tr_from_tbody(
    parent_identifier="", parent_attribute="id", child_identifier="", child_attribute="class",
):
    return TableRow(
        xpath=get_child_element_from_parent(
            "tbody", "tr", parent_identifier, parent_attribute, child_identifier, child_attribute,
        )
    )


def get_td_from_tr(
    parent_identifier="", parent_attribute="id", child_identifier="", child_attribute="class",
):
    return TableData(
        xpath=get_child_element_from_parent(
            "tr", "td", parent_identifier, parent_attribute, child_identifier, child_attribute,
        )
    )


##########################
# ## Getters by Index ## #
##########################
"""
Get table elements by their parent elements and given index
:param index: 
:param parent_identifier: Parent value in value-attribute pair to search in
:param parent_attribute: Parent attribute in value-attribute pair to search in
:param child_identifier: Child value in value-attribute pair to search in
:param child_attribute: Child attribute in value-attribute pair to search in
:return: Requested element, if any
"""


def get_tr_by_index_from_tbody(
    index, parent_identifier="", parent_attribute="id", child_identifier="", child_attribute="class",
):
    return TableRow(
        xpath=get_child_element_from_parent(
            "tbody", "tr", parent_identifier, parent_attribute, child_identifier, child_attribute,
        )
        + "["
        + str(index)
        + "]"
    )


def get_td_by_index_from_tr(
    index, parent_identifier="", parent_attribute="id", child_identifier="", child_attribute="class",
):
    return TableData(
        xpath=get_child_element_from_parent(
            "tr", "td", parent_identifier, parent_attribute, child_identifier, child_attribute,
        )
        + "["
        + str(index)
        + "]"
    )
