"""
Description: Represents a form composed of fields, dropdown menus, and other input elements.
"""
from pytest_elements.elements.date_picker import DatePicker
from pytest_elements.elements.dropdown import Dropdown
from pytest_elements.elements.page_element import PageElement
from pytest_elements.elements.select import Select
from pytest_elements.elements.text_field import TextField
from pytest_elements.helpers.autofill_functions import AutofillFunctions
import time
import deprecation


class Form(AutofillFunctions, PageElement):
    """
    Represents a form composed of fields, dropdown menus, and other input elements which extend the FormComponent class.

    """

    def __init__(self, *fields, **named_fields):
        """
        Constructs a form with the given fields.
        *fields is either a list of PageElements
        **named_fields is a list of named PageElements
        """
        super().__init__()
        self.head = None
        self.field_map = None
        if fields:
            self.num_fields = len(fields)
            self.head = fields[0]
            current = self.head
            for f in fields[1:]:
                current.next_node = f
                current = current.next_node
        elif named_fields:
            self.field_map = named_fields

    def fill(self, *params, timeout=0, **named_params):
        """
        Fills out the form by sending each parameter to each of the corresponding form fields.
        If the value is -1, then it will autofill the field with valid data.
        If the value is -2, then it will autofill the field with invalid data.
        Accepts either a list of all parameter values (for Forms created with a list of fields)
        or a list of named field values (for Forms created with a list of named fields).
        If the timeout value is set, each element will be waited on (for a total of 'timeout' seconds
        across all elements) before being filled.
        """
        if self.field_map:
            # Ensure values have been passed in a map.
            assert named_params and not params, "Expected named values."
            input_data = {}
            if timeout:
                start_time = time.time()
            # Validate each passed key
            for key, value in named_params.items():
                field = self.field_map.get(key)
                if not field:
                    raise ValueError(f"Key {key} does not match any form field.")
                if value is not None:
                    # Wait for element to appear if indicated
                    if timeout:
                        time_elapsed = time.time() - start_time
                        time_remaining = timeout - time_elapsed
                        field.wait_until_fillable(timeout=time_remaining)
                    # Set each value to the given value or an auto-generated value if indicated
                    if value == self.AUTOFILL_VALID_INPUT or value == self.AUTOFILL_INVALID_INPUT:
                        value = self.handle_autofill(value, field)
                    else:
                        field.accept_input(value)
                    # Update map of actually input data
                    input_data[key] = value
            # Return the map of actually input data
            return input_data
        else:
            assert (
                len(params) == self.num_fields
            ), f"Expected {self.num_fields} values but was called with {len(params)}."
            current = self.head
            data = []
            if timeout:
                start_time = time.time()
            # Set each value to the given value or an auto-generated value if indicated
            for p in params:
                if p is not None:
                    # Wait for element to appear if indicated
                    if timeout:
                        time_elapsed = time.time() - start_time
                        time_remaining = timeout - time_elapsed
                        current.wait_until_fillable(timeout=time_remaining)
                    if p == self.AUTOFILL_VALID_INPUT or p == self.AUTOFILL_INVALID_INPUT:
                        p = self.handle_autofill(p, current)
                    else:
                        current.accept_input(p)
                data.append(p)
                current = current.next_node
            # Return the list of all of the actually input data
            # This should be used to validate data in the tests.
            return data

    def fill_when_ready(self, *params, timeout=25, **named_params):
        """
        Essentially the same as form.fill(), but it waits for each field to be
        fill-able before attempting to pass it input.
        """
        return self.fill(*params, timeout=timeout, **named_params)

    def handle_autofill(self, parameter, current_field):
        if parameter == self.AUTOFILL_VALID_INPUT:
            valid = True
        else:
            valid = False
        if isinstance(current_field, TextField):
            try:
                parameter = self.generate_data_for_field(input_type=current_field.input_type, valid=valid)

            except TypeError:
                print(
                    f"ERROR: {current_field.input_type} is not a valid input type. Make sure that the field "
                    f"you are attempting to autofill has the correct input_type assigned when "
                    f"instantiated."
                )
                raise
            current_field.accept_input(parameter)
        elif isinstance(current_field, (Select, Dropdown)):
            try:
                if current_field.input_type:
                    parameter = self.generate_data_for_field(input_type=current_field.input_type, valid=valid)
                else:
                    parameter = -1
                current_field.accept_input(parameter)
            except (TypeError, ValueError):
                parameter = -1
                print(
                    f"Warning: {current_field.input_type} is not a valid input type. Autofilling with " f"random data."
                )
                parameter = current_field.accept_input(parameter)
        elif isinstance(current_field, DatePicker):
            current_field.accept_input(self.generate_data_for_field(input_type="date", valid=valid))
        return parameter

    def selector(self):
        """
        Intentionally left un-implemented because Forms are not interacted with directly on the web page.
        """
        raise NotImplementedError(
            "Form instances are not interacted with directly, " "they are just a wrapper for form fields"
        )

    @deprecation.deprecated(details="Use the poll_visibility function instead")
    def wait_visible(self, timeout=10):
        """
        DEPRECATED: use poll_visibility instead.
        Waits until all elements in the form are visible.
        """
        if self.field_map:
            for name, field in self.field_map.items():
                field.wait_until_visible(err_msg=f"Form element '{name}' never became visible")
        elif self.head:
            current_node = self.head
            while current_node:
                current_node.poll_visibility(timeout)
                current_node = current_node.next_node

    def poll_visibility(self, visible=True, timeout=15, poll_frequency=0.5):
        """
        Waits until all elements in the form are visible
        :return: True if all elements are found to be visible w/in the given timeout, otherwise False
        """
        start_time = time.time()
        if self.field_map:
            for name, field in self.field_map.items():
                time_elapsed = time.time() - start_time
                time_remaining = timeout - time_elapsed
                if time_elapsed >= timeout:
                    return False
                if not field.poll_visibility(visible=visible, timeout=time_remaining, poll_frequency=poll_frequency,):
                    return False
            return True
        elif self.head:
            current_node = self.head
            while current_node:
                time_elapsed = time.time() - start_time
                time_remaining = timeout - time_elapsed
                if time_elapsed >= timeout:
                    return False
                if not current_node.poll_visibility(
                    visible=visible, timeout=time_remaining, poll_frequency=poll_frequency,
                ):
                    return False
                current_node = current_node.next_node
            return True

    def fields(self):
        """
        Returns a list (or map) of all fields in the form.
        """
        if self.field_map:
            return self.field_map
        elif self.head:
            fields = []
            node = self.head
            while node:
                fields.append(node)
                node = node.next_node
            return fields

    def get_xpath_string(self):
        """
        Return string of xpath
        :return:
        """
        pass

    def get_values(self):
        """
        Returns a list or map of field values.
        :param web_driver:
        :param value:
        :return:
        """
        if self.field_map:
            values = {}
            for name, field in self.field_map.items():
                values[name] = field.get_value()
            return values
        elif self.head:
            values = []
            for field in self.fields():
                values.append(field.get_value())
            return values
