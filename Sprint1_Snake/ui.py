import arcade
import music
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, BG_COLOR, TEXT_COLOR
from game import GameView

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

    def on_show_view(self):
        arcade.set_background_color(BG_COLOR)
        music.play_menu_music()

    def on_draw(self):
        self.clear()
        arcade.draw_text("SNAKE", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 60,
                         TEXT_COLOR, font_size=48, anchor_x="center")
        arcade.draw_text("Select Difficulty:", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 10,
                         TEXT_COLOR, font_size=24, anchor_x="center")
        arcade.draw_text("1 – Easy (Slow)",   SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 30,
                         TEXT_COLOR, font_size=20, anchor_x="center")
        arcade.draw_text("2 – Medium (Normal)", SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 60,
                         TEXT_COLOR, font_size=20, anchor_x="center")
        arcade.draw_text("3 – Hard (Fast)",   SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 90,
                         TEXT_COLOR, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        if key == arcade.key.KEY_1:
            self.start_game("easy")
        elif key == arcade.key.KEY_2:
            self.start_game("medium")
        elif key == arcade.key.KEY_3:
            self.start_game("hard")

    def start_game(self, difficulty):
        music.stop_menu_music()
        game = GameView(difficulty)
        game.setup()
        self.window.show_view(game)
