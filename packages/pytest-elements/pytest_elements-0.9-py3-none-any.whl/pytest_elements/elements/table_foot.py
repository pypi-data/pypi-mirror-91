from pytest_elements.elements.table_row import TableRowContainer


class TableFoot(TableRowContainer):
    def __init__(self, identifier=None, attribute=None, xpath=None):
        """
        Construct a new TableFoot instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        super().__init__(
            element_type="tfoot", identifier=identifier, attribute=attribute, xpath=xpath,
        )
