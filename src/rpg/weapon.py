from item import Item

# Keeps track of source paths for all possible Weapon sprites
weapon_sprites = {'IRON_SWORD': 'images/weapon_sprite/IronSword.png',
                  'STEEL_SWORD': 'images/weapon_sprite/SteelSword.png',
                  'SILVER_SWORD': 'images/weapon_sprite/SilverSword.png',
                  'GOLD_SWORD': 'images/weapon_sprite/GoldSword.png',
                  'OBSIDIAN_SWORD': 'images/weapon_sprite/ObsidianSword.png',
                  'DIAMOND_SWORD': 'images/weapon_sprite/DiamondSword.png',
                  'FLAMING_SWORD': 'images/weapon_sprite/FlamingSword.png'}


# Weapon
class Weapon(Item):
    # Minimum attack strength
    min_attack = 0
    # Maximum attack strength
    max_attack = 0

    # Constructor
    def __init__(self, name, kind, value, description, owner, min_attack, max_attack, **kwargs):
        super(Weapon, self).__init__(name, kind, value, description, owner, **kwargs)
        self.min_attack = min_attack
        self.max_attack = max_attack
