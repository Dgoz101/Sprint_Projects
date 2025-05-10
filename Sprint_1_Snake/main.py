import arcade
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE
from ui import MenuView

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu = MenuView()
    window.show_view(menu)
    arcade.run()

if __name__ == "__main__":
    main()
