from abc import abstractmethod
from kivy.uix.widget import Widget
from kivy.properties import ListProperty, ObjectProperty

from random import Random
random = Random()


# Basic blueprint for any character widget
class CharacterWidget(Widget):
    # Current sprite of Character as Object Property
    sprite = ObjectProperty(None)
    # Current color of Character widget as rgba List Property
    sprite_color = ListProperty([1, 0, 0, 0])
    # Rate of position change with respect to time (dv/dt) in x (velocity[0]) and y (velocity[1])
    velocity = ListProperty([0, 0])
    # Keep track of when Character can be attacked again (max 30)
    attacked_counter = 0

    # Constructor
    def __init__(self, **kwargs):
        super(CharacterWidget, self).__init__(**kwargs)


# Basic blueprint for any character
class Character(object):
    # Name (player name or monster type or boss name)
    name = 'Unnamed'
    # Maximum amount of health
    max_health = 100
    # Current amount of health
    current_health = 100
    # Minimum damage of an attack
    min_attack_strength = 0
    # Maximum damage of an attack
    max_attack_strength = 1
    # Maximum protection from armor
    armor_rating = 0
    # Coins held
    coins = 0
    # Experience (player's accumulates, monster's is transferred upon death)
    experience = 0
    # Current experience level
    level = 1
    # Inventory containing all items
    inventory = None

    # Constructor
    def __init__(self, name, max_health, coins, experience, level, inventory):
        self.name = name
        self.max_health = max_health
        self.current_health = self.max_health
        self.coins = coins
        self.experience = experience
        self.level = level
        self.inventory = inventory

    # Generates a random amount of experience depending upon monster level
    def generate_experience(self, monster_level):
        experience = monster_level * Random.randint(Random(), 1, 10)
        return experience

    # Generates a random amount of coins depending upon monster level
    def generate_coins(self, monster_level):
        coins = Random.randint(Random(), 1, 10 * monster_level)
        return coins

    # Character (self) is attacked by attacker
    def getting_attacked(self, attacker):
        # Generate how much damage the attacker will deal
        attack_power = random.randint(attacker.min_attack_strength, attacker.max_attack_strength)
        # Generate how much damage the attacked character will absorb
        armor_power = random.randint(0, self.armor_rating)

        # Determine how much damage the attacker will deal before armor
        damage_taken = 0
        # If armor_power is greater than attack_power
        if armor_power > attack_power:
            # No damage is taken
            damage_taken = 0
        # If attack_power is greater than or equal
        else:
            # Damage taken is the attack_power of the attacker minus the armor_power
            damage_taken = attack_power - armor_power

        self.current_health -= damage_taken
        self.check_if_dead()
        print damage_taken, self.current_health

    # Check to see if Character has died after being attacked
    def check_if_dead(self):
        # If current_health is less than or equal to 0
        if self.current_health <= 0:
            # Character has died
            self.died()

    # Deal with Character death
    @abstractmethod
    def died(self):
        raise NotImplementedError('Must override died')




