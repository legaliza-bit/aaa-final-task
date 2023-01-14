from unittest.mock import patch
import io
import sys
import click
from click.testing import CliRunner

import pizza_place
import timer_decorator


def test_cli_order():
    @click.command()
    @click.option("--delivery", default=False, is_flag=True)
    @click.argument("pizza", nargs=1)
    def order(pizza: str, delivery: bool):
        """Bakes and delivers the pizza"""
        pizza = pizza.capitalize()
        try:
            pizza_order = pizza_place.__pizza_classes()[pizza]
        except KeyError:
            click.echo("Sorry, this is not on the menu 😔")
            return None
        pizza_place.Pepperoni.bake.__wrapped__(pizza_order())
        if delivery:
            pizza_place.Pepperoni.delivery.__wrapped__(pizza_order())
        else:
            pizza_place.Pepperoni.pickup.__wrapped__(pizza_order())

    expected = ""
    result = CliRunner().invoke(order, "pepperoni")
    assert result.exit_code == 0
    assert result.output == expected


def test_cli_menu():
    expected = "- Margherita 🧀: tomato sauce, mozzarella, tomatoes\n- Pepperoni 🍕: tomato sauce, mozzarella, pepperoni\n- Hawaiian 🍍: tomato sauce, mozzarella, chicken, pineapple\n"
    result = CliRunner().invoke(pizza_place.menu)
    assert result.exit_code == 0
    assert result.output == expected


@patch("timer_decorator.randint")
def test_decorator(mock_randint):
    capturedOutput = io.StringIO()
    sys.stdout = capturedOutput
    text = "Pizza cooked in {} secs!"
    mock_randint.return_value = 2

    @timer_decorator.timer_decorator(text)
    def mock_func():
        pass

    mock_func()
    actual = capturedOutput.getvalue()
    expected = "Pizza cooked in 2 secs!\n"
    sys.stdout = sys.__stdout__

    assert actual == expected
    mock_randint.assert_called_once()


def test_eq():
    pizza_1 = pizza_place.Margherita(size="L")
    pizza_2 = pizza_place.Margherita(size="XL")
    assert pizza_1 == pizza_2


def test_dict():
    hawaiian_recipe = pizza_place.Hawaiian().dict()
    expected_recipe = {
        "Hawaiian": ["tomato sauce", "mozzarella", "chicken", "pineapple"]
    }
    assert hawaiian_recipe == expected_recipe
