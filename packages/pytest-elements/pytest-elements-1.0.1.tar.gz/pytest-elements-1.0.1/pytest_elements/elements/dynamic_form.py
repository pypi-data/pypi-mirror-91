from pytest_elements.elements.form import Form
from selenium.common.exceptions import StaleElementReferenceException
import time


class DynamicForm(Form):
    """
    Represents a form in which the potential values of the single-select elements
    (e.g. dropdown menus) may change as the form is filled out.
    Note that the inputs themselves do *not* appear/disappear - only their available values change.
    """

    def selector(self):
        super().selector()

    def fill(self, *params):
        """
        Fill out a form, backing off exponentially when StaleElement exceptions are caught
        to allow the fields time to stabilize.
        :param params:
        :return:
        """
        assert len(params) == self.num_fields, f"Expected {self.num_fields} values but was called with {len(params)}."
        current = self.head
        data = []

        for p in params:
            success = False
            attempts = 0
            while (not success) and attempts < 5:
                try:
                    if (
                        p == self.AUTOFILL_VALID_INPUT
                        or p == self.AUTOFILL_INVALID_INPUT
                        or p == self.AUTOFILL_BLANK_INPUT
                    ):
                        p = self.handle_autofill(p, current)
                    else:
                        current.accept_input(p)
                    data.append(p)
                    success = True
                except StaleElementReferenceException:
                    time.sleep(2 ** attempts)
                    attempts += 1
            assert success, f"Form field {current} failed to stabilize after {(2 ** attempts) - 1} seconds."
            current = current.next_node
        return data
