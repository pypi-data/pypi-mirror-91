import random
from datetime import datetime, timedelta

from faker import Faker
import json
import sys


class AutofillFunctions:
    """
    Allows form components to generate and access autofill data
    """

    address_input_types = [
        "address_line",
        "address_line2",
        "zip_code",
        "zip_code_plus4",
        "country",
        "city",
        "state",
        "region",
    ]
    months = [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    ]

    python_version_str = f"{sys.version_info.major}.{sys.version_info.minor}"
    autofill_data_path = (
        f"venv/lib/python{python_version_str}/" "site-packages/pytest_elements/helpers/autofill_data.json"
    )

    faker = Faker()

    AUTOFILL_VALID_INPUT = -1
    AUTOFILL_INVALID_INPUT = -2

    ###################################
    #                                 #
    #     Data Generation Methods     #
    #                                 #
    ###################################

    @classmethod
    def name(cls):
        """
        Generates and returns a random name.
        :return:
        """

        first_name = cls.first_name()
        middle_name = cls.middle_name()
        last_name = cls.last_name()
        full_name = first_name + " " + middle_name + " " + last_name
        return full_name

    @classmethod
    def first_name(cls):
        """
        Generates and returns a random first name
        """
        return cls.faker.first_name()

    @classmethod
    def middle_name(cls):
        """
        Generates and returns a random middle name
        """
        return cls.faker.first_name()

    @classmethod
    def last_name(cls):
        """
        Generates and returns a random last name
        """
        return cls.faker.last_name()

    @classmethod
    def attention(cls):
        """
        Generates and returns a random attention
        :return:
        """
        return f"Attention {cls.name()}"

    @classmethod
    def text(cls, max_nb_chars=None, ext_word_list=None):
        """
        Generates and returns a random text
        :param max_nb_chars: NUmber of characters the text should have
        :param ext_word_list:
        :return:
        """

        if not max_nb_chars:
            max_nb_chars = random.randint(5, 10)

        return cls.faker.text(max_nb_chars, ext_word_list)

    @classmethod
    def email(cls, valid):
        """
        Generates and returns a random email
        :param valid: True if good data that is valid for the field should be returned.
        """
        return cls.faker.ascii_safe_email() if valid else cls.faker.domain_name()

    @classmethod
    def phone_number(cls, valid):
        """
        Generates adn returns a random phone number.
        :param valid: True if good data that is valid for the field should be returned.
        """
        return random.randint(1000000000, 9999999999) if valid else "NOT-NUM-CELL"

    @classmethod
    def extension(cls, valid):
        """
        Generates and returns a random phone extension.
        :param valid: True if good data that is valid for the field should be returned.
        """
        return random.randint(1000, 9999) if valid else "FAKE"

    @classmethod
    def country_code(cls, valid):
        """
        Generates and returns a random country code.
        :param valid: True if good data that is valid for the field should be returned.
        """
        return 1 if valid else "FAKE"

    @classmethod
    def address(cls, valid):
        """
        Pulls a random json address from autofill_data.json and assigns each value to the correct value
        :param valid: True if good data that is valid for the field should be returned.
        """

        if valid:
            return cls.random_valid_real_address()

        else:
            return cls.random_valid_fake_address()

    @classmethod
    def date(cls, valid):
        """
        Generates and returns a Python date object.
        If valid is True, returns a date from the future. Otherwise,
        returns a date from the past.
        """
        date = datetime.now() + timedelta(days=(1 if valid else -1) * (random.randint(0, 356)))
        return date.date()

    @classmethod
    def card_number(cls, valid):
        """
        Generates and returns a random credit card number.
        :param valid: True if good data that is valid for the field should be returned.
        """
        card = cls.random_valid_credit_card()
        return card["CardNumber"] if valid else random.randint(0000000000000000, 9999999999999999)

    @classmethod
    def card_expiration_month_num(cls):
        """
        Generates and returns a random card expiration month in number form (ex. 01 for January)
        """
        expiration = cls.faker.credit_card_expire(start="now", end="+10y", date_format="%m/%y").split("/")
        return expiration[0]

    @classmethod
    def card_expiration_month_str(cls):
        """
        Generates and returns a random card expiration month in string form (ex. Jan for January)
        """
        expiration = cls.faker.credit_card_expire(start="now", end="+10y", date_format="%m/%y").split("/")
        return cls.months[int(expiration[0]) - 1]

    @classmethod
    def card_expiration_year(cls):
        """
        Generates and returns a random expiration year for a credit card.
        """
        expiration = cls.faker.credit_card_expire(start="now", end="+10y", date_format="%m/%y").split("/")
        return str(datetime.today().year + 10)[:2] + str(expiration[1])

    @classmethod
    def card_expiration_date(cls, valid):
        """
        Generates and returns a complete expiration date for a credit card.
        :param valid: True if good data that is valid for the field should be returned.
        """
        if valid:
            expiration = cls.faker.credit_card_expire(start="now", end="+10y", date_format="%m/%y").split("/")
            expiration_month_num = expiration[0]
            expiration_month_str = cls.months[int(expiration[0]) - 1]
            expiration_year = str(datetime.today().year + 10)[:2] + str(expiration[1])
        else:
            expiration = cls.faker.credit_card_expire(start="-20y", end="-10y", date_format="%m/%y").split("/")
            expiration_month_num = expiration[0]
            expiration_month_str = cls.months[int(expiration[0]) - 1]
            expiration_year = str(datetime.today().year - 20)[:2] + str(expiration[1])

        return expiration_month_num, expiration_month_str, expiration_year

    @classmethod
    def card_cvv(cls):
        """
        Generates and returns a random credit card cvv
        """
        return cls.faker.credit_card_security_code()

    @classmethod
    def bank_account_number(cls):
        """
        Generates and returns a random bank account number
        """
        return cls.faker.bban()

    @classmethod
    def bank_routing_number(cls):
        """
        Generates and returns a random bank routing number.
        """
        return random.randint(100000000, 999999999)

    @classmethod
    def generate_data_for_field(cls, input_type, valid):
        """
        Generates data for a specific field type. Do not regenerate address if valid = True
        :param input_type: The input type for the field
        :param valid: Whether or not the field should contain valid data
        :return:
        """
        if input_type == "first_name":
            return cls.first_name()
        elif input_type == "middle_name":
            return cls.middle_name()
        elif input_type == "last_name":
            return cls.last_name()
        elif input_type == "name":
            return cls.name()
        elif input_type == "email":
            return cls.email(valid)
        elif input_type == "attention":
            return cls.attention()
        elif input_type in cls.address_input_types:
            return cls.address(valid)[input_type]
        elif input_type == "phone":
            return cls.phone_number(valid)
        elif input_type == "extension":
            return cls.extension(valid)
        elif input_type == "country_code":
            return cls.country_code(valid)
        elif input_type == "text":
            return cls.text()
        elif input_type == "date":
            return cls.date(valid)
        elif input_type == "bank_account_number":
            return cls.bank_account_number()
        elif input_type == "bank_routing_number":
            return cls.bank_routing_number()
        elif input_type == "card_number":
            return cls.card_number(valid)
        elif input_type == "exp_month_num":
            return cls.card_expiration_month_num()
        elif input_type == "exp_month_str":
            return cls.card_expiration_month_str()
        elif input_type == "exp_year":
            return cls.card_expiration_year()
        elif input_type == "card_expiration_date":
            return cls.card_expiration_date(valid)
        elif input_type == "cvv":
            return cls.card_cvv()
        else:
            raise ValueError(
                f"Data could not be generated for {cls} since it has no valid input_type assigned."
                f"\nType which could not be generated: {input_type}"
            )

    ###################################
    #                                 #
    #          Helper Methods         #
    #                                 #
    ###################################

    @classmethod
    def random_valid_fake_address(cls):
        """
        Pulls an address that doesn't actually exist, but is still valid from autofill_data.json
        """
        with open(cls.autofill_data_path) as file:
            data = json.load(file)
            real_addresses = data["fake_addresses"]
            return random.choice(real_addresses)

    @classmethod
    def random_valid_real_address(cls):
        """
        Pulls a real, valid address from autofill_data.json
        """
        with open(cls.autofill_data_path) as file:
            data = json.load(file)
            real_addresses = data["real_addresses"]
            return random.choice(real_addresses)

    @classmethod
    def random_valid_credit_card(cls):
        """
        Pulls a valid credit card from autofill_data.json
        """
        with open(cls.autofill_data_path) as file:
            data = json.load(file)
            real_credit_cards = data["credit_cards"]
            return random.choice(real_credit_cards)
