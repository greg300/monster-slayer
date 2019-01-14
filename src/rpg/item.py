from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty


# Item
class Item(Widget):
    # Sprite of item as Object Property
    item_sprite = ObjectProperty(None)

    # Name of item
    name = 'Item'
    # Kind of item
    kind = 'Type'
    # Value of item in coins
    value = 0
    # Description of item
    description = ''
    # Owner of item
    owner = None
    # Keeps track of whether item is equipped
    is_equipped = False

    # Constructor
    def __init__(self, name, kind, value, description, owner, **kwargs):
        super(Item, self).__init__(**kwargs)
        self.name = name
        self.kind = kind
        self.value = value
        self.description = description
        self.owner = owner

    # Print all the properties of an item
    def print_item(self):
        print self.name, self.kind, self.value, self.description, self.owner
