import arcade

# Window
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE  = "Snake Game"

# Grid
BLOCK_SIZE = 20

# Speed = seconds per move
DIFFICULTY_SPEED = {
    "easy":   0.20,   # slow
    "medium": 0.10,   # normal
    "hard":   0.05,   # fast
}

# Colors
BG_COLOR    = arcade.color.BLACK
SNAKE_COLOR = arcade.color.AFRICAN_VIOLET
FOOD_COLOR  = arcade.color.YELLOW
TEXT_COLOR  = arcade.color.WHITE
