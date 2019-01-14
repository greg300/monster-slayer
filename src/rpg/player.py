from kivy.properties import ObjectProperty
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.uix.widget import Widget

from weapon import Weapon
from character import *
from all_items import *

# Keeps track of source paths for all possible Player sprites
player_sprites = {'ATTACKING_RIGHT': 'images/player_sprite/AttackingRight.zip',
                  'ATTACKING_LEFT': 'images/player_sprite/AttackingLeft.zip',
                  'RUNNING_RIGHT': 'images/player_sprite/RunningRight.zip',
                  'RUNNING_LEFT': 'images/player_sprite/RunningLeft.zip',
                  'STANDING_RIGHT': 'images/player_sprite/StandingRight.zip',
                  'STANDING_LEFT': 'images/player_sprite/StandingLeft.zip'}


# Player
class Player(Character):
    # Weapon equipped (not necessarily onscreen)
    weapon = None
    # Keep track of monsters killed
    monsters_killed = 0
    # Widget displayed
    player_widget = None

    # Constructor
    def __init__(self, name, max_health, coins, experience, level, inventory, weapon):
        super(Player, self).__init__(name, max_health, coins, experience, level, inventory)
        self.equip_weapon(weapon)

    # Deal with Player death
    def died(self):
        self.player_widget.parent.parent.open_deathscreen()
        self.player_widget.parent.remove_widget(self.player_widget)

    # Equip a weapon
    def equip_weapon(self, weapon):
        self.weapon = weapon
        self.max_attack_strength = self.weapon.max_attack
        self.min_attack_strength = self.weapon.min_attack


# Player Widget displayed on screen
class PlayerWidget(CharacterWidget):
    # Keep track of whether Player is jumping
    is_jumping = False
    # Keep track of jump duration (max 20)
    jump_counter = 0
    # Keep track of whether Player is attacking
    is_attacking = False
    # Keep track of time between attacks (max 20)
    attack_counter = 0

    # Player whom this widget represents
    player = None
    # Weapon Widget displayed onscreen
    weapon_displayed = None

    # Constructor
    def __init__(self, **kwargs):
        super(PlayerWidget, self).__init__(**kwargs)

    # Change Player sprite depending on current action
    def change_sprite(self, is_pressing_right, is_pressing_left, is_pressing_up, is_pressing_space):
        # If attacked_counter is greater than 30
        if self.attacked_counter > 30:
            # Change sprite color to transparent
            self.sprite_color = [1, 0, 0, 1]

        # If attacking and not currently showing attack sprite
        if self.is_attacking and (self.sprite.source != player_sprites['ATTACKING_RIGHT'] and
                                  self.sprite.source != player_sprites['ATTACKING_LEFT']):
            # If facing right
            if self.is_facing_right():
                # Set sprite to 'ATTACKING_RIGHT'
                self.sprite.source = player_sprites['ATTACKING_RIGHT']
            # If facing left
            elif self.is_facing_left():
                # Set sprite to 'ATTACKING_LEFT'
                self.sprite.source = player_sprites['ATTACKING_LEFT']
            return

        # If attacking and showing attack sprite
        elif self.is_attacking:
            # Do nothing
            return

        # Fix for both right and left pressed simultaneously creating oscillating image
        # If pressing right and left and moving right
        if is_pressing_right and is_pressing_left and self.velocity[0] > 0:
            # Set sprite to 'RUNNING_RIGHT'
            self.sprite.source = player_sprites['RUNNING_RIGHT']
        # If pressing right and left and moving left
        elif is_pressing_right and is_pressing_left and self.velocity[0] < 0:
            # Set sprite to 'RUNNING_LEFT'
            self.sprite.source = player_sprites['RUNNING_LEFT']
        # If pressing right and left and not moving
        elif is_pressing_right and is_pressing_left and self.velocity[0] == 0:
            # If was just showing 'RUNNING_RIGHT' sprite
            if self.sprite.source == player_sprites['RUNNING_RIGHT']:
                # Set sprite to 'STANDING_RIGHT'
                self.sprite.source = player_sprites['STANDING_RIGHT']
            # If was just showing 'RUNNING_LEFT' sprite
            elif self.sprite.source == player_sprites['RUNNING_LEFT']:  # Not working for higher speeds
                # Set sprite to 'STANDING_LEFT'
                self.sprite.source = player_sprites['STANDING_LEFT']

        # If pressing right and not currently showing 'RUNNING_RIGHT' sprite
        elif is_pressing_right and self.sprite.source != player_sprites['RUNNING_RIGHT']:
            # Set sprite to 'RUNNING_RIGHT'
            self.sprite.source = player_sprites['RUNNING_RIGHT']

        # If pressing left and not currently showing 'RUNNING_LEFT' sprite
        elif is_pressing_left and self.sprite.source != player_sprites['RUNNING_LEFT']:
            # Set sprite to 'RUNNING_LEFT'
            self.sprite.source = player_sprites['RUNNING_LEFT']

        # If not moving and was just facing right
        elif self.velocity[0] == 0 and self.is_facing_right():
            # Set sprite to 'STANDING_RIGHT'
            self.sprite.source = player_sprites['STANDING_RIGHT']

        # If not moving and was just facing left
        elif self.velocity[0] == 0 and self.is_facing_left():
            # Set sprite to 'STANDING_LEFT'
            self.sprite.source = player_sprites['STANDING_LEFT']

        """"# If moving
        if abs(self.velocity[0]) > 0:
            # Set anim_delay inversely proportional to x velocity
            self.sprite.anim_delay = 0.1 #/ (abs(self.velocity[0]) + 1)

        # If not moving
        elif self.velocity[0] == 0:
            # Set anim_delay to 0.1
            self.sprite.anim_delay = 0.1"""

    # Returns True if Player is facing right
    def is_facing_right(self):
        if (self.sprite.source == player_sprites['RUNNING_RIGHT'] or
            self.sprite.source == player_sprites['ATTACKING_RIGHT'] or
            self.sprite.source == player_sprites['STANDING_RIGHT']):
            return True
        else:
            return False

    # Returns True if Player is facing left
    def is_facing_left(self):
        if (self.sprite.source == player_sprites['RUNNING_LEFT'] or
            self.sprite.source == player_sprites['ATTACKING_LEFT'] or
            self.sprite.source == player_sprites['STANDING_LEFT']):
            return True
        else:
            return False

    # Called every time Parent Widget is updated, 60 times per second
    def update_player(self, is_pressing_right, is_pressing_left, is_pressing_up, is_pressing_space):
        # If attacked_counter is less than 31
        if self.attacked_counter < 31:
            # Increase attacked_counter by 1
            self.attacked_counter += 1

        # If attacking
        """if self.is_attacking:
            # If moving right
            if self.velocity[0] > 0:
                # Decelerate
                self.velocity[0] -= 0.5
            # If moving left
            elif self.velocity[0] < 0:
                # Decelerate
                self.velocity[0] += 0.5"""

        # Update Player's position by adding the velocity
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        # If pressing right and not left
        if is_pressing_right and not is_pressing_left:
            # Accelerate right
            self.accelerate_x()

        # If pressing left and not right
        elif is_pressing_left and not is_pressing_right:
            # Accelerate left
            self.decelerate_x()

        # If pressing both left and right
        elif is_pressing_right and is_pressing_left:
            # If moving left
            if self.velocity[0] < 0:
                # Accelerate right until stopping
                self.accelerate_x()
            # If moving right
            elif self.velocity[0] > 0:
                # Accelerate left until stopping
                self.decelerate_x()

        # If not pressing left and moving left
        if not is_pressing_left and self.velocity[0] < 0:
            # Accelerate right until stopping
            self.accelerate_x()
        # If not pressing right and moving right
        elif not is_pressing_right and self.velocity[0] > 0:
            # Accelerate left until stopping
            self.decelerate_x()

        # If touching the edge of Window
        if self.x < 0 or (self.x + self.width) > Window.width:
            # If glitched to left of Window
            if self.x < -1:
                # Fix position to 0
                self.x = 0
            # If glitched to right of Window
            if (self.x + self.width) > Window.width + 1:
                # Fix position to Window border
                self.x = Window.width - self.width
            # Reverse x velocity
            self.velocity[0] *= -1
            return

        # If pressing up and jumping and jump_counter is less than 21 and not falling or at peak height
        if is_pressing_up and self.is_jumping and self.jump_counter < 21 and self.velocity[1] > 0:
            # Accelerate up
            self.accelerate_y()
            # Increase jump_counter by 1
            self.jump_counter += 1
        # If not pressing up and jumping
        elif not is_pressing_up and self.is_jumping:
            # Accelerate down
            self.decelerate_y()
            # Set jump_counter to 20 so Player can't jump again in midair
            self.jump_counter = 21
        # If pressing up and jump_counter is greater than 20
        elif is_pressing_up and self.jump_counter > 20:
            # Accelerate down
            self.decelerate_y()
        # If pressing up and not jumping and touching ground
        elif is_pressing_up and not self.is_jumping:
            # Set is_jumping to True
            self.is_jumping = True
            # Accelerate up
            self.accelerate_y()
            # Increase jump_counter by 1
            self.jump_counter += 1
            # If not attacking
            if not self.is_attacking:
                # Set anim_delay for sprite very large
                self.sprite.anim_delay = 1000

        # If attack_counter is less than 20
        if self.attack_counter < 20:
            # Increase attack_counter by 1
            self.attack_counter += 1
        # If attack_counter equals 20 and attacking
        elif self.attack_counter == 20 and self.is_attacking:
            # Set is_attacking to False
            self.is_attacking = False
            # Set anim_delay for sprite back to normal
            self.sprite.anim_delay = 0.1
            #print 'DONE ATTACKING'
        # PROBLEM: ATTACKING RIGHT AFTER BEING DONE ATTACKING - FIXED?
        # If pressing space and not attacking
        elif is_pressing_space and not self.is_attacking: #and self.velocity[1] == 0:
            # Set is_attacking to True
            self.is_attacking = True
            # Set attack_counter to 0
            self.attack_counter = 0
            # Set anim_delay for sprite much smaller
            self.sprite.anim_delay = 0.03
            #print 'START ATTACKING'
        # If attack_counter equals 15 and attacking
        if self.attack_counter == 15 and self.is_attacking:
            # Attack with Weapon Widget
            self.weapon_out()
        # If attack_counter is between 15 and 18 and attacking
        if 15 < self.attack_counter < 18 and self.is_attacking:
            # Weapon Widget is out, so update position with Player velocity
            self.weapon_displayed.x += self.velocity[0]
            self.weapon_displayed.y += self.velocity[1]
        # If attack_counter equals 18 and attacking
        if self.attack_counter == 18 and self.is_attacking:
            # Put weapon away
            self.weapon_away()

        # Change sprite if needed
        self.change_sprite(is_pressing_right, is_pressing_left, is_pressing_up, is_pressing_space)

    # Increase x velocity
    def accelerate_x(self):
        # If velocity is very large
        if self.velocity[0] > 10:
            # Do nothing
            return
        # If velocity is small
        if 2 >= self.velocity[0] >= 0.5:
            # Increase by larger increment
            self.velocity[0] += 0.5
        # If velocity is larger
        else:
            # Increase by smaller increment
            self.velocity[0] += 0.25

    # Decrease x velocity
    def decelerate_x(self):
        # If velocity is very large
        if self.velocity[0] < -10:
            # Do nothing
            return
        # If velocity is larger
        if -2 <= self.velocity[0] <= -0.5:
            # Decrease by larger increment
            self.velocity[0] -= 0.5
        # If velocity is smaller:
        else:
            # Decrease by smaller increment
            self.velocity[0] -= 0.25

    # Increase y velocity
    def accelerate_y(self):
        # If velocity is small
        if self.velocity[1] <= 6:
            # Increase by larger increment
            self.velocity[1] += 2
        else:
            # Increase by smaller increment
            self.velocity[1] += 0.2

    # Decrease y velocity
    def decelerate_y(self):
        # Decrease
        self.velocity[1] -= 1

    # Take weapon out
    def weapon_out(self):
        # Take weapon out
        self.weapon_displayed = self.player.weapon
        # If attacking right
        if self.sprite.source == player_sprites['ATTACKING_RIGHT']:
            # Place Weapon Widget on right
            self.weapon_displayed.pos = (self.x + self.width - 50, self.y + 0.1 * self.height)
        # If attacking left
        elif self.sprite.source == player_sprites['ATTACKING_LEFT']:
            # Place Weapon Widget on left
            self.weapon_displayed.pos = (self.x - 90, self.y + 0.1 * self.height)
        # Fix Size of weapon
        self.weapon_displayed.size = (140, 140)
        # Fix Color of weapon
        with self.weapon_displayed.canvas:
            Color(0, 1, 0, 0.25)
            Rectangle(pos=(self.weapon_displayed.x, self.weapon_displayed.y), size=self.weapon_displayed.size)
        # Add Weapon Widget to Game
        self.add_widget(self.weapon_displayed)

    # Put weapon away
    def weapon_away(self):
        # Clear Weapon Widget from Game
        self.remove_widget(self.weapon_displayed)
        self.weapon_displayed.canvas.clear()
        self.weapon_displayed = None
