import click
from timer_decorator import timer_decorator


class Pizza:
    emoji = ""
    ingredients = ["tomato sauce", "mozzarella"]

    def __init__(self, size="L"):
        self.size = size  # assume default pizza size is L

    def dict(self) -> dict:
        recipe = {self.__class__.__name__: self.ingredients}
        return recipe

    @timer_decorator("👨‍🍳 Cooked in {} secs!")
    def bake(self):
        pass

    @timer_decorator("🏍️ Delivered in {} secs!")
    def delivery(self):
        pass

    @timer_decorator("🏠 Picked up in {} secs!")
    def pickup(self):
        pass

    def __eq__(self, other) -> bool:
        if isinstance(other, self.__class__):
            return True
        return False


class Margherita(Pizza):
    emoji = "🧀"
    ingredients = Pizza.ingredients + ["tomatoes"]


class Pepperoni(Pizza):
    emoji = "🍕"
    ingredients = Pizza.ingredients + ["pepperoni"]


class Hawaiian(Pizza):
    emoji = "🍍"
    ingredients = Pizza.ingredients + ["chicken", "pineapple"]


def __pizza_classes() -> dict:
    """Return a dict of class names as keys and classes as values"""
    dict_of_classes = {}
    for class_ in Pizza.__subclasses__():
        dict_of_classes[class_.__name__] = class_
    return dict_of_classes


@click.group()
def cli():
    pass


@cli.command()
def menu():
    """Prints the menu"""
    for pizza in Pizza.__subclasses__():
        click.echo(
            f"- {pizza.__name__} {pizza().emoji}: {', '.join(pizza().ingredients)}"
        )


@cli.command()
@click.option("--delivery", default=False, is_flag=True)
@click.argument("pizza", nargs=1)
def order(pizza: str, delivery: bool):
    """Bakes and delivers the pizza"""
    pizza = pizza.capitalize()
    try:
        pizza_order = __pizza_classes()[pizza]
    except KeyError:
        click.echo("Sorry, this is not on the menu 😔")
        return None
    pizza_order().bake()
    if delivery:
        pizza_order().delivery()
    else:
        pizza_order().pickup()


if __name__ == "__main__":
    cli()
