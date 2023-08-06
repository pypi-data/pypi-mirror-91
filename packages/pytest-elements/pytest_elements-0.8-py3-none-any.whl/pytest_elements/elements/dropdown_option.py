"""
Description: Represents an individual option in a dropdown menu.
It is preferred to use this class over Dropdown when the exact options in
a dropdown menu are known, can be interacted with directly, and there is a benefit
to interacting with them individually rather than a group.
"""
from pytest_elements.elements.page_element import PageElement
from pytest_elements.helpers.xpath_creation_functions import get_child_element_from_parent


class DropdownOption(PageElement):
    """
    An option in a dropdown menu.
    """

    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new Dropdown Option instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        if not xpath:
            # Weird because it's nested
            self.xpath = get_child_element_from_parent(
                parent_type="select",
                child_type="option",
                parent_identifier="selector-modal",
                parent_attribute="class",
                child_identifier=identifier,
                child_attribute=attribute,
            )
        else:
            self.xpath = xpath
            self.identifier = ""
        super().__init__(
            element_type="option", identifier=identifier, attribute=attribute, xpath=xpath,
        )
