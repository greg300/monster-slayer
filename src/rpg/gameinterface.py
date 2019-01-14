from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.core.window import Window
from all_items import *
from inventory import Inventory
from player import *
from all_monsters import *


# Parent Widget
class GameInterface(Widget):
    # Child Widgets of Parent Widget as ObjectProperties
    player = ObjectProperty(None)
    seeker = ObjectProperty(None)
    bouncer = ObjectProperty(None)
    base = ObjectProperty(None)
    background = ObjectProperty(None)

    # Keep track of whether or not the left and right keys are being pressed
    is_pressing_left = False
    is_pressing_right = False

    # Keep track of whether or not up key is being pressed
    is_pressing_up = False

    # Keep track of whether or not space key is being pressed
    is_pressing_space = False

    # Keep track of whether or not widgets and objects were linked
    linked = False

    # Constructor
    def __init__(self, **kwargs):
        super(GameInterface, self).__init__(**kwargs)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    # Unbind keyboard when closed
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None

    # Check for certain keys being pressed
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Print the keycode of the key pressed
        #print keycode[1] + " down"

        app = App.get_running_app()

        # If 'a' key is pressed and on the Game Screen
        if keycode[1] == 'a' and app.root.current == 'Game Screen':
            print "Moving left"
            # Pressing left and not right
            self.is_pressing_left = True
            #self.is_pressing_right = False

        # If 'd' key is pressed and on the Game Screen
        elif keycode[1] == 'd' and app.root.current == 'Game Screen':
            print "Moving right"
            # Pressing right and not left
            #self.is_pressing_left = False
            self.is_pressing_right = True

        # If 'w' key is pressed and on the Game Screen
        elif keycode[1] == 'w' and app.root.current == 'Game Screen':
            print "Jumping"
            # Pressing up
            self.is_pressing_up = True

        # If 'spacebar' is pressed and on the Game Screen
        elif keycode[1] == 'spacebar' and app.root.current == 'Game Screen':
            print "Attacking"
            # Pressing space
            self.is_pressing_space = True

        # If 'escape' key is pressed
        elif keycode[1] == 'escape':
            # Go to pause menu
            self.parent.pause()

        # If 'i' key is pressed
        elif keycode[1] == 'i':
            # Go to inventory menu
            self.parent.open_inventory()

        # If 't' key is pressed
        elif keycode[1] == 't':
            # Create a test inventory
            self.create_test_inventory()

        # If 'p' key is pressed
        elif keycode[1] == 'p':
            # Print out widget references
            print self.bouncer
            print self.seeker
            print self.bouncer.monster.monster_widget
            print self.seeker.monster.monster_widget

        # If '`' key is pressed
        elif keycode[1] == '`':
            # Print which keyboard is in use
            print "OTHER KEYBOARD"

        return True

    # Check for certain keys being unpressed
    def _on_keyboard_up(self, keyboard, keycode, *args):
        # Print the keycode of the key unpressed
        #print keycode[1] + " up"

        # If 'a' key is unpressed
        if keycode[1] == 'a':
            # Not pressing left
            self.is_pressing_left = False
            #self.is_pressing_right = False

        # If 'd' key is unpressed
        elif keycode[1] == 'd':
            # Not pressing right
            #self.is_pressing_left = False
            self.is_pressing_right = False

        # If 'w' key is unpressed
        elif keycode[1] == 'w':
            print "Not jumping"
            # Not pressing up
            self.is_pressing_up = False

        # If 'spacebar' key is unpressed
        elif keycode[1] == 'spacebar':
            print "Not attacking"
            # Not pressing space
            self.is_pressing_space = False

        return True

    # Links objects to widgets
    def link(self):
        # Set the player whom the player widget is representing to be a new player
        self.player.player = Player('Player', 100, 0, 0, 1, Inventory(), weapons['GOLD_SWORD'])
        # Set the player widget representing the player
        self.player.player.player_widget = self.player

        # Set the monster whom the bouncing widget is representing to be a bouncing monster
        self.bouncer.monster = bouncing_monsters['GREEN_DRAGON']
        # Set the bouncing widget representing the bouncer
        self.bouncer.monster.monster_widget = self.bouncer

        # Set the monster whom the seeking widget is representing to be a seeking monster
        self.seeker.monster = seeking_monsters['BLACK_DRAGON']
        # Set the seeking widget representing the seeker
        self.seeker.monster.monster_widget = self.seeker

    # Called 60 times per second; used for interactions between widgets
    def update(self, *args):
        # If first update
        if not self.linked:
            # Link objects to widgets
            self.link()
            self.linked = True

        # Player
        # If Player is colliding with ground while falling
        if self.player.collide_widget(self.base) and self.player.velocity[1] < 0:
            # Set Player y velocity to 0
            self.player.velocity[1] = 0
            # Fix Player y position
            self.player.y = self.base.height
            # Set Player is_jumping to False
            self.player.is_jumping = False
            # Set Player jump_counter to 0
            self.player.jump_counter = 0
            # Set anim_delay for Player sprite back to normal
            self.player.sprite.anim_delay = 0.1

        # If Player is not attacking and falling
        elif not self.player.is_attacking and self.player.velocity[1] < 0:
            # Set anim_delay for Player sprite very large
            self.player.sprite.anim_delay = 1000

        # Monsters
        # If BouncingMonster is colliding with the ground
        if self.bouncer.collide_widget(self.base):
            # Reverse velocity of BouncingMonster
            self.bouncer.velocity[1] *= -1

        # If SeekingMonster is colliding with the player
        if self.seeker.collide_widget(self.player):
            self.hitting_player(self.seeker)
            #print 'COLLIDING WITH SEEKER'

        # If BouncingMonster is colliding with the player
        if self.bouncer.collide_widget(self.player):
            # If has_collided_counter is greater than 60
            if self.bouncer.has_collided_counter > 60:
                # Reset has_collided_counter
                self.bouncer.has_collided_counter = 0
                # Reverse velocity of BouncingMonster
                self.bouncer.velocity[1] *= -1
            self.hitting_player(self.bouncer)
            #print 'COLLIDING WITH BOUNCER'

        # If Player's Weapon is out
        if self.player.weapon_displayed is not None:
            # If Player's Weapon is colliding with seeker
            if self.player.weapon_displayed.collide_widget(self.seeker):
                #print 'HITTING SEEKER'
                self.hitting_monster(self.seeker)

            # If Player's Weapon is colliding with bouncer
            if self.player.weapon_displayed.collide_widget(self.bouncer):
                #print 'HITTING BOUNCER'
                self.hitting_monster(self.bouncer)

        self.seeker.update_seeker()
        self.bouncer.update_bouncer()
        self.player.update_player(self.is_pressing_right, self.is_pressing_left,
                                  self.is_pressing_up, self.is_pressing_space)

    # Check to make sure that Player can hit Monster
    def hitting_monster(self, monster):
        # If Monster can be attacked (attacked_counter is greater than 30)
        if monster.attacked_counter > 30:
            # Change sprite color of monster to red
            monster.sprite_color = [1, 0, 0, 0.5]
            # Player attacks Monster
            monster.monster.getting_attacked(self.player.player)
            # Reset monster's attacked_counter to 0
            monster.attacked_counter = 0

    # Check to make sure that Monster can hit Player
    def hitting_player(self, monster):
        # If Player can be attacked (attacked_counter is greater than 30)
        if self.player.attacked_counter > 30:
            # Change sprite color of player to red
            self.player.sprite_color = [1, 0, 0, 0.5]
            # Monster attacks Player
            self.player.player.getting_attacked(monster.monster)
            # Reset player's attacked_counter to 0
            self.player.attacked_counter = 0

    def create_test_inventory(self):
        inventory = Inventory()
        inventory.items = [weapons['IRON_SWORD'], armor['IRON_CHESTPLATE'], potions['SMALL_HEALTH_POTION']]
        self.player.player.inventory = inventory
        for item in self.player.player.inventory.items:
            item.print_item()


# App
class GameInterfaceApp(App):
    def build(self):
        game = GameInterface()
        return game
