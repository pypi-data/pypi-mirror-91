from string import Template


def get_generic_xpath(element_type, element_identifier="", element_attribute="class"):
    """
    Return element on a web page
    :param element_type: Type of element to search for
    :param element_identifier: Element identifier
    :param element_attribute: Attribute to search on
    :return: xpath for described element
    """

    template_types = {
        "id": Template("//$type[@id='$identifier']"),
        "class": Template("//$type[contains(@class, '$identifier')]"),
        "name": Template("//$type[contains(@name, '$identifier')]"),
        "text": Template("//$type[normalize-space()='$identifier']"),
    }

    generic_template = Template("//$type[@$attribute='$identifier']")

    if element_attribute in template_types.keys():
        return template_types.get(element_attribute, None).substitute(type=element_type, identifier=element_identifier)
    else:
        return generic_template.substitute(
            type=element_type, attribute=element_attribute, identifier=element_identifier,
        )


def get_child_element_from_parent(
    parent_type, child_type, parent_identifier="", parent_attribute="", child_identifier="", child_attribute="class",
):
    """
    Search page for a child element nested in a given parent element
    :param parent_type: Type of parent element
    :param child_type: Type of final element to search for
    :param parent_identifier: Identifier for parent
    :param parent_attribute: Attribute type of parent to search on
    :param child_identifier: Identifier for child
    :param child_attribute: Attribute type of child to search on
    :return: xpath for described element
    """

    xpath = "//" + parent_type + "[contains(@" + parent_attribute + ', "' + parent_identifier + '")]/'
    xpath += child_type + "[contains(@" + child_attribute + ', "' + child_identifier + '")]'
    return xpath
