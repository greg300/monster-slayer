from kivy.properties import ListProperty
from kivy.animation import Animation
from kivy.core.window import Window
from kivy.uix.widget import Widget

from random import random
from character import *

# Keeps track of source paths for all possible Enemy sprites
enemy_sprites = {'GREEN_FLYING_RIGHT': 'images/enemy_sprite/GreenDragonFlyingRight.zip',
                 'GREEN_FLYING_LEFT': 'images/enemy_sprite/GreenDragonFlyingLeft.zip',
                 'BLACK_FLYING_RIGHT': 'images/enemy_sprite/BlackDragonFlyingRight.zip',
                 'BLACK_FLYING_LEFT': 'images/enemy_sprite/BlackDragonFlyingLeft.zip'}


# Monster
class Monster(Character):
    # Widget displayed
    monster_widget = None
    # Type of monster ('SEEKING', 'BOUNCING', 'WALKING')
    kind = None

    # Constructor
    def __init__(self, kind, name, min_damage, max_damage, max_health, coins, experience, level, inventory):
        super(Monster, self).__init__(name, max_health, coins, experience, level, inventory)
        self.kind = kind
        self.min_attack_strength = min_damage
        self.max_attack_strength = max_damage

    # Deal with Monster death
    def died(self):
        self.monster_widget.parent.remove_widget(self.monster_widget)
        self.monster_widget = None


# Animates to random position; Monster Widget displayed on screen
class SeekingMonsterWidget(CharacterWidget):
    # Increase by 1 on update; animates once counter reaches 180
    counter = 0
    # Keep track of whether SeekingMonster is moving right
    is_moving_right = False
    # Keep track of whether SeekingMonster is moving left
    is_moving_left = False

    # Monster whom this widget represents
    monster = None

    # Constructor
    def __init__(self, **kwargs):
        super(SeekingMonsterWidget, self).__init__(**kwargs)

    # Animates SeekingMonster to a random position
    def anim_to_random_pos(self):
        # Cancel any current animations
        Animation.cancel_all(self)

        # Generate random coordinates within Window and ground boundaries
        random_x = random.random() * (Window.width - self.width)
        random_y = random.random() * (Window.height - self.height)

        # If random_x position is greater than or equal to current x
        if random_x >= self.x:
            # Moving right not left
            self.is_moving_right = True
            self.is_moving_left = False
        # If random_x position is less than current x
        if random_x < self.x:
            # Moving left not right
            self.is_moving_left = True
            self.is_moving_right = False

        # Define new 3-second animation and start
        anim = Animation(x=random_x, y=random_y, duration=3, t='out_quad')
        anim.start(self)

    # Called every time Parent Widget is updated, 60 times per second
    def update_seeker(self, *args):
        # If attacked_counter is less than 31
        if self.attacked_counter < 31:
            # Increase attacked_counter by 1
            self.attacked_counter += 1

        # Increase counter by 1
        self.counter += 1

        # If counter equals 180
        if self.counter == 180:
            # Animate to random position
            self.anim_to_random_pos()
            # Reset counter back to 0
            self.counter = 0

        self.change_sprite()

    # Change SeekingMonster sprite depending on current direction
    def change_sprite(self):
        # If attacked_counter is greater than 30
        if self.attacked_counter > 30:
            # Change sprite color to transparent
            self.sprite_color = [1, 0, 0, 0]

        # If moving right and not currently showing 'BLACK_FLYING_RIGHT' sprite
        if self.is_moving_right and self.sprite.source != enemy_sprites['BLACK_FLYING_RIGHT']:
            # Set sprite to 'BLACK_FLYING_RIGHT'
            self.sprite.source = enemy_sprites['BLACK_FLYING_RIGHT']
        # If moving left and not currently showing 'BLACK_FLYING_LEFT' sprite
        elif self.is_moving_left and self.sprite.source != enemy_sprites['BLACK_FLYING_LEFT']:
            # Set sprite to 'BLACK_FLYING_LEFT'
            self.sprite.source = enemy_sprites['BLACK_FLYING_LEFT']


# Bounces around screen
class BouncingMonsterWidget(CharacterWidget):
    # Rate of position change with respect to time (dv/dt) in x (velocity[0]) and y (velocity[1])
    velocity = ListProperty([5, 5])
    # Increase by 1 on update; BouncingMonster can only collide with Player when greater than 60
    has_collided_counter = 0

    # Monster whom this widget represents
    monster = None

    # Constructor
    def __init__(self, **kwargs):
        super(BouncingMonsterWidget, self).__init__(**kwargs)

    # Called every time Parent Widget is updated, 60 times per second
    def update_bouncer(self, *args):
        # If attacked_counter is less than 31
        if self.attacked_counter < 31:
            # Increase attacked_counter by 1
            self.attacked_counter += 1

        # Update BouncingMonster's position by adding the velocity
        self.x += self.velocity[0]
        self.y += self.velocity[1]

        # If has_collided_counter is less than 61
        if self.has_collided_counter < 61:
            # Increase has_collided_counter by 1
            self.has_collided_counter += 1

        # If touching left or right edge of Window
        if self.x < 0 or (self.x + self.width) > Window.width:
            self.velocity[0] *= -1
        # If touching bottom or top edge of Window
        if self.y < 0 or (self.y + self.height) > Window.height:
            self.velocity[1] *= -1

        # Change sprite if needed
        self.change_sprite()

    # Change BouncingMonster sprite depending on current direction
    def change_sprite(self):
        # If attacked_counter is greater than 30
        if self.attacked_counter > 30:
            # Change sprite color to transparent
            self.sprite_color = [1, 0, 0, 0]

        # If moving right and not currently showing 'GREEN_FLYING_RIGHT' sprite
        if self.velocity[0] > 0 and self.sprite.source != enemy_sprites['GREEN_FLYING_RIGHT']:
            # Set sprite to 'GREEN_FLYING_RIGHT'
            self.sprite.source = enemy_sprites['GREEN_FLYING_RIGHT']
        # If moving left and not currently showing 'GREEN_FLYING_LEFT' sprite
        elif self.velocity[0] < 0 and self.sprite.source != enemy_sprites['GREEN_FLYING_LEFT']:
            # Set sprite to 'GREEN_FLYING_LEFT'
            self.sprite.source = enemy_sprites['GREEN_FLYING_LEFT']


# Walks along the ground
class WalkingMonsterWidget(CharacterWidget):
    # Rate of position change with respect to time (dv/dt) in x (velocity[0]) and y (velocity[1])
    velocity = ListProperty([5, 5])
    # Increase by 1 on update; WalkingMonster can only collide with Player when greater than 60
    has_collided_counter = 0
    # Current color of WalkingMonster as rgba List Property
    sprite_color = ListProperty([1, 0, 0, 0])

    # Monster whom this widget represents
    monster = None

    # Constructor
    def __init__(self, **kwargs):
        super(WalkingMonsterWidget, self).__init__(**kwargs)