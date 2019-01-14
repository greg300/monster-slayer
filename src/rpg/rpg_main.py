from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.image import Image

# TODO: Finish commenting code
# TODO: DONE? Fix jumping animation after attacking so player stops moving in midair
# TODO: Create save/load system
# TODO: Create death animation; image will scale to size of monster
# TODO: Create doors that open after all monsters are slain
# TODO: Create inventory screen/inventory/item system
# TODO: Create better start screen
# TODO: Create shop system
# TODO: Create monster generation system (monsters are instances of monster class with specific properties)
# TODO: DONE. Create one monster.py file
# TODO: DONE. Implement collision system
# TODO: Create player leveling system
# TODO: Create story
# TODO: Create level generating system
# TODO: Create bosses
# TODO: Create HUD with health and Time Mana display bar
# TODO: Armor/Weapons only add POTENTIAL multiplier for protection/attack bonus

# Keeps track of source paths for all possible Player sprites
sprites = {'ATTACK_RIGHT': 'images/player_sprite/AttackingRight.zip',
           'ATTACK_LEFT': 'images/player_sprite/AttackingLeft.zip',
           'RUNNING_RIGHT': 'images/player_sprite/RunningRight.zip',
           'RUNNING_LEFT': 'images/player_sprite/RunningLeft.zip',
           'STANDING_RIGHT': 'images/player_sprite/StandingRight.zip',
           'STANDING_LEFT': 'images/player_sprite/StandingLeft.zip'}


# Parent Widget
class Game(Widget):
    # Keep track of the number of frames updated (max 60)
    sixty_frame_count = 0
    # Event for updating frames (scheduled on rpg start)
    frames = None
    # GameInterface as Object Property (what goes on the GameScreen)
    game_interface = ObjectProperty(None)

    # Constructor
    def __init__(self, **kwargs):
        super(Game, self).__init__(**kwargs)

        # Schedule frame update 60 times per second
        self.frames = Clock.schedule_interval(self.update, 1.0 / 60)
        # Open keyboard
        self._keyboard_open()

    # Opens keyboard
    def _keyboard_open(self):
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        self._keyboard.bind(on_key_up=self._on_keyboard_up)

    # Unbind keyboard when closed
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard.unbind(on_key_up=self._on_keyboard_up)
        self._keyboard = None
        pass

    # Check for certain keys being pressed
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # Print the keycode of the key pressed
        print keycode[1] + " down"

        # If 'escape' key is pressed
        if keycode[1] == 'escape':
            # Pause the rpg
            self.pause()

        # If '`' key is pressed
        elif keycode[1] == '`':
            # Print which keyboard is in use
            print "MAIN KEYBOARD"

        return True

    # Check for certain keys being unpressed
    def _on_keyboard_up(self, keyboard, keycode, *args):
        # Print the keycode of the key unpressed
        print keycode[1] + " up"

    # Called 60 times per second
    def update(self, *args):
        app = App.get_running_app()

        # If on the Game Screen
        if app.root.current == 'Game Screen':
            # Update game_interface
            self.game_interface.update(self.game_interface)

        # Increase sixty_frame_count by 1
        self.sixty_frame_count += 1
        # If sixty_frame_count equals 60
        if self.sixty_frame_count == 60:
            # Set sixty_frame_count back to 0
            self.sixty_frame_count = 0
            print 'UPDATED'

    # Pause the rpg
    def pause(self):
        # Stop the clock
        self.frames.cancel()
        print "PAUSED"
        app = App.get_running_app()
        # Switch screens to Pause Screen
        app.root.current = 'Pause Screen'
        # Set the game_instance of PauseScreen to the current instance of Game
        PauseScreen.game_instance = self

    # Open the inventory
    def open_inventory(self):
        # Stop the clock
        self.frames.cancel()
        print "OPENED INVENTORY - PAUSED"
        app = App.get_running_app()
        # Switch screens to Inventory Screen
        app.root.current = 'Inventory Screen'
        # Set the game_instance of Inventory to the current instance of Game
        InventoryScreen.game_instance = self

    # Open the death screen
    def open_deathscreen(self):
        # Stop the clock
        self.frames.cancel()
        print "YOU HAVE DIED"
        app = App.get_running_app()
        # Switch screens to Death Screen
        app.root.current = 'Death Screen'

    # Resume the rpg
    def resume(self):
        # Resume the clock
        self.frames = Clock.schedule_interval(self.update, 1.0 / 60)
        print "RESUMED"


# Start Screen displayed upon first launching the gamve
class StartScreen(Screen):

    # Constructor
    def __init__(self, **kwargs):
        super(StartScreen, self).__init__(**kwargs)
        # Preload all player sprites
        self.load_images()

    # Preloads all player sprites
    def load_images(self):
        for key in sprites:
            i = Image(sprites[key], keep_data=True)

    # Start the rpg
    def start(self):
        app = App.get_running_app()
        # Switch screens to Game Screen
        app.root.current = 'Game Screen'


# Game Screen on which GameInterface is
class GameScreen(Screen):

    # Constructor
    def __init__(self, **kwargs):
        super(GameScreen, self).__init__(**kwargs)


# Pause Screen displayed when rpg is paused
class PauseScreen(Screen):
    # Keep track of current instance of Game
    game_instance = None

    # Constructor
    def __init__(self, **kwargs):
        super(PauseScreen, self).__init__(**kwargs)

    # Resume the rpg
    def resume(self):
        # Resume the clock
        Game.resume(self.game_instance)
        app = App.get_running_app()
        # Switch screens to Game Screen
        app.root.current = 'Game Screen'

    # Toggle fullscreen
    @staticmethod
    def go_fullscreen():
        # If already fullscreen
        if Window.fullscreen:
            # Exit fullscreen
            Window.fullscreen = False

        # If not fullscreen
        else:
            # Enter fullscreen
            Window.fullscreen = True


# InventoryScreen displayed when viewing inventory
class InventoryScreen(Screen):
    # Keep track of current instance of Game
    game_instance = None

    # Constructor
    def __init__(self, **kwargs):
        super(InventoryScreen, self).__init__(**kwargs)

    # Resume the rpg
    def resume(self):
        # Resume the clock
        Game.resume(self.game_instance)
        app = App.get_running_app()
        # Switch screens to Game Screen
        app.root.current = 'Game Screen'


# PlayerDeathScreen displayed when player dies
class PlayerDeathScreen(Screen):
    # Constructor
    def __init__(self, **kwargs):
        super(PlayerDeathScreen, self).__init__(**kwargs)


# Handles switching screens
class ScreenSwitcher(ScreenManager):
    pass


# App
class RPGApp(App):
    def build(self):
        game = ScreenSwitcher()
        Window.size = (1280, 720)
        Window.fullscreen = True
        #Window.size = (800, 600)
        return game

if __name__ == '__main__':
    RPGApp().run()
