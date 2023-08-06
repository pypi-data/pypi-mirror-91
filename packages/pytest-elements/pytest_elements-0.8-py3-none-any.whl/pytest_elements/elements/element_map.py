"""
Defines a map of all tag names to their corresponding PageElement classes
"""
from selenium.webdriver.remote.webelement import WebElement

from pytest_elements.elements.anchor import Anchor
from pytest_elements.elements.date_picker import DatePicker
from pytest_elements.elements.dropdown_option import DropdownOption
from pytest_elements.elements.file_picker import FilePicker
from pytest_elements.elements.page_element import PageElement
from pytest_elements.elements.button import Button
from pytest_elements.elements.canvas import Canvas
from pytest_elements.elements.checkbox import Checkbox
from pytest_elements.elements.div import Div
from pytest_elements.elements.dropdown import Dropdown
from pytest_elements.elements.form import Form
from pytest_elements.elements.h1 import H1
from pytest_elements.elements.h2 import H2
from pytest_elements.elements.h3 import H3
from pytest_elements.elements.h4 import H4
from pytest_elements.elements.img import Img
from pytest_elements.elements.italic import Italic
from pytest_elements.elements.radio_button import RadioButton
from pytest_elements.elements.select import Select
from pytest_elements.elements.table import Table
from pytest_elements.elements.table_foot import TableFoot
from pytest_elements.elements.table_row import TableRow
from pytest_elements.elements.table_data import TableData
from pytest_elements.elements.table_head import TableHead
from pytest_elements.elements.table_body import TableBody

from typing import List, Tuple

from pytest_elements.elements.text_field import TextField

element_map = {
    "a": Anchor,
    "button": Button,
    "canvas": Canvas,
    "div": Div,
    "select": Dropdown,
    "option": DropdownOption,
    "select": Select,
    "form": Form,
    "h1": H1,
    "h2": H2,
    "h3": H3,
    "h4": H4,
    "img": Img,
    "i": Italic,
    "table": Table,
    "tr": TableRow,
    "td": TableData,
    "thead": TableHead,
    "tbody": TableBody,
    "tfoot": TableFoot,
}

input_type_element_map = {
    "text": TextField,
    "tel": TextField,
    "password": TextField,
    "email": TextField,
    "url": TextField,
    "number": TextField,
    "search": TextField,
    "checkbox": Checkbox,
    "submit": Button,
    "button": Button,
    "reset": Button,
    "radio": RadioButton,
    "date": DatePicker,
    "file": FilePicker,
}


def map_elements(element_list: List[Tuple[WebElement, str]]) -> List[PageElement]:
    page_elements = []
    for element_and_xpath in element_list:
        element, xpath = element_and_xpath
        if element.tag_name == "input":
            input_type = element.get_attribute("type")
            pe_class = input_type_element_map.get(input_type, None)
        else:
            pe_class = element_map.get(element.tag_name, None)
        if pe_class:
            page_elements.append(pe_class(xpath=xpath))
        else:
            page_elements.append(PageElement(xpath=xpath))
    return page_elements
