from item import Item

# Keeps track of source paths for all possible Armor sprites
armor_sprites = {'IRON_BOOTS': 'images/item_sprite/IronBoots.png',
                 'IRON_GREAVES': 'images/item_sprite/IronGreaves.png',
                 'IRON_CHESTPLATE': 'images/item_sprite/IronChestplate.png',
                 'IRON_GAUNTLETS': 'images/item_sprite/IronGauntlets.png',
                 'IRON_HELMET': 'images/item_sprite/IronHelmet.png',
                 'STEEL_BOOTS': 'images/item_sprite/SteelBoots.png',
                 'STEEL_GREAVES': 'images/item_sprite/SteelGreaves.png',
                 'STEEL_CHESTPLATE': 'images/item_sprite/SteelChestplate.png',
                 'STEEL_GAUNTLETS': 'images/item_sprite/SteelGauntlets.png',
                 'STEEL_HELMET': 'images/item_sprite/SteelHelmet.png',
                 'SILVER_BOOTS': 'images/item_sprite/SilverBoots.png',
                 'SILVER_GREAVES': 'images/item_sprite/SilverGreaves.png',
                 'SILVER_CHESTPLATE': 'images/item_sprite/SilverChestplate.png',
                 'SILVER_GAUNTLETS': 'images/item_sprite/SilverGauntlets.png',
                 'SILVER_HELMET': 'images/item_sprite/SilverHelmet.png',
                 'GOLD_BOOTS': 'images/item_sprite/GoldBoots.png',
                 'GOLD_GREAVES': 'images/item_sprite/GoldGreaves.png',
                 'GOLD_CHESTPLATE': 'images/item_sprite/GoldChestplate.png',
                 'GOLD_GAUNTLETS': 'images/item_sprite/GoldGauntlets.png',
                 'GOLD_HELMET': 'images/item_sprite/GoldHelmet.png',
                 'OBSIDIAN_BOOTS': 'images/item_sprite/ObsidianBoots.png',
                 'OBSIDIAN_GREAVES': 'images/item_sprite/ObsidianGreaves.png',
                 'OBSIDIAN_CHESTPLATE': 'images/item_sprite/ObsidianChestplate.png',
                 'OBSIDIAN_GAUNTLETS': 'images/item_sprite/ObsidianGauntlets.png',
                 'OBSIDIAN_HELMET': 'images/item_sprite/ObsidianHelmet.png',
                 'DIAMOND_BOOTS': 'images/item_sprite/DiamondBoots.png',
                 'DIAMOND_GREAVES': 'images/item_sprite/DiamondGreaves.png',
                 'DIAMOND_CHESTPLATE': 'images/item_sprite/DiamondChestplate.png',
                 'DIAMOND_GAUNTLETS': 'images/item_sprite/DiamondGauntlets.png',
                 'DIAMOND_HELMET': 'images/item_sprite/DiamondHelmet.png'}


# Armor
class Armor(Item):
    # Armor rating
    armor_rating = 0

    # Constructor
    def __init__(self, name, kind, value, description, owner, armor_rating, **kwargs):
        super(Armor, self).__init__(name, kind, value, description, owner, **kwargs)
        self.armor_rating = armor_rating


# Boots
class Boots(Armor):
    # Constructor
    def __init__(self, name, kind, value, description, owner, armor_rating, **kwargs):
        super(Boots, self).__init__(name, kind, value, description, owner, armor_rating, **kwargs)


# Greaves
class Greaves(Armor):
    # Constructor
    def __init__(self, name, kind, value, description, owner, armor_rating, **kwargs):
        super(Greaves, self).__init__(name, kind, value, description, owner, armor_rating, **kwargs)


# Chestplate
class Chestplate(Armor):
    # Constructor
    def __init__(self, name, kind, value, description, owner, armor_rating, **kwargs):
        super(Chestplate, self).__init__(name, kind, value, description, owner, armor_rating, **kwargs)


# Gauntlets
class Gauntlets(Armor):
    # Constructor
    def __init__(self, name, kind, value, description, owner, armor_rating, **kwargs):
        super(Gauntlets, self).__init__(name, kind, value, description, owner, armor_rating, **kwargs)


# Helmet
class Helmet(Armor):
    # Constructor
    def __init__(self, name, kind, value, description, owner, armor_rating, **kwargs):
        super(Helmet, self).__init__(name, kind, value, description, owner, armor_rating, **kwargs)
