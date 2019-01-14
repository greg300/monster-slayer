from item import Item

# Keeps track of source paths for all possible Potion sprites
potion_sprites = {'SMALL_HEALTH_POTION': 'images/item_sprite/SmallHealthPotion.png',
                  'MEDIUM_HEALTH_POTION': 'images/item_sprite/MediumHealthPotion.png',
                  'LARGE_HEALTH_POTION': 'images/item_sprite/LargeHealthPotion.png',
                  'EXTRA_LARGE_HEALTH_POTION': 'images/item_sprite/ExtraLargeHealthPotion.png',
                  'SUPER_HEALTH_POTION': 'images/item_sprite/SuperHealthPotion.png',
                  'MIRACULOUS_HEALTH_POTION': 'images/item_sprite/MiraculousHealthPotion.png'}


# Potion
class Potion(Item):
    min_heal_amount = 0
    max_heal_amount = 1

    # Constructor
    def __init__(self, name, kind, value, description, owner, min_heal_amount, max_heal_amount, **kwargs):
        super(Potion, self).__init__(name, kind, value, description, owner, **kwargs)
        self.min_heal_amount = min_heal_amount
        self.max_heal_amount = max_heal_amount
