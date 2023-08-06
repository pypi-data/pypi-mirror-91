"""
Description: Defines the Tile element.
"""
from pytest_elements.elements.div import Div
from pytest_elements.elements.radio_button import RadioButton
from pytest_elements.elements.div import Div


class Tile(Div):
    """
    Button-like PageElement used in SCA interfaces.
    """

    def __init__(self, id=None, text=None, xpath=None, large_tile=False):
        """
        Construct a new Tile instance,
        located using the specified attribute and attribute-value OR a supplied xpath.
        """
        if id:
            super().__init__(
                xpath=f"//input[@type='radio' and @value='{id}']/..//div[contains(@class,'container-tile-selectable')]"
            )
        elif text:
            super().__init__(
                xpath=f"//div[contains(@class,'container-tile-selectable')]/div[contains(@class,'{'tile-large' if large_tile else 'tile-small'}') and normalize-space() = '{text}']/../div)"
            )
        elif xpath:
            super().__init__(xpath=xpath)
        else:
            raise ValueError("Please specify a Product ID, Visible Text or Xpath for the tile")
