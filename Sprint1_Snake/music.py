import arcade
import os

_menu_player = None
_game_player = None

# Build absolute paths
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
MENU_PATH   = os.path.join(BASE_DIR, "assets", "menu_music.mp3")
GAME_PATH   = os.path.join(BASE_DIR, "assets", "game_music.mp3")

def play_menu_music():
    global _menu_player
    stop_game_music()
    if not os.path.exists(MENU_PATH):
        print(f"[music] menu music file does not exist.")
        return

    try:
        snd = arcade.load_sound(MENU_PATH)
        _menu_player = arcade.play_sound(snd, loop=True)
    except Exception as e:
        print(f"[music] Error playing menu music: {e}")

def stop_menu_music():
    global _menu_player
    if _menu_player:
        _menu_player.pause()
        _menu_player = None

def play_game_music():
    global _game_player
    stop_menu_music()
    if not os.path.exists(GAME_PATH):
        print(f"[music] game music file does not exist.")
        return

    try:
        snd = arcade.load_sound(GAME_PATH)
        _game_player = arcade.play_sound(snd, loop=True)
    except Exception as e:
        print(f"[music] Error playing game music: {e}")

def stop_game_music():
    global _game_player
    if _game_player:
        _game_player.pause()
        _game_player = None
