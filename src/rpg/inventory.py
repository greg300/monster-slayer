from kivy.uix.widget import Widget
from kivy.properties import ListProperty


# Inventory
class Inventory(Widget):
    # List of all items in inventory
    items = ListProperty([])
    # Owner of inventory
    owner = None

    # Constructor
    def __init__(self, **kwargs):
        super(Inventory, self).__init__(**kwargs)

    # Add an item to inventory
    def add_item(self, item):
        self.items.add(item)

