import arcade
import random
import music
from collections import deque
from settings import (
    SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE,
    BG_COLOR, SNAKE_COLOR, FOOD_COLOR, TEXT_COLOR,
    DIFFICULTY_SPEED
)

class GameView(arcade.View):
    def __init__(self, difficulty):
        super().__init__()
        self.difficulty    = difficulty
        self.move_interval = DIFFICULTY_SPEED[difficulty]
        self.move_timer    = 0.0
        self.segments      = deque()
        self.direction     = "RIGHT"
        self.food_position = (0, 0)
        self.score         = 0

    def setup(self):
        music.play_game_music()
        # Center snake on grid
        cx = (SCREEN_WIDTH // 2 // BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE // 2
        cy = (SCREEN_HEIGHT // 2 // BLOCK_SIZE) * BLOCK_SIZE + BLOCK_SIZE // 2
        self.segments.clear()
        self.segments.append((cx, cy))
        self.spawn_food()

    def spawn_food(self):
        while True:
            x = random.randint(0, SCREEN_WIDTH // BLOCK_SIZE - 1) * BLOCK_SIZE + BLOCK_SIZE // 2
            y = random.randint(0, SCREEN_HEIGHT // BLOCK_SIZE - 1) * BLOCK_SIZE + BLOCK_SIZE // 2
            if (x, y) not in self.segments:
                self.food_position = (x, y)
                return

    def on_draw(self):
        self.clear()
        half = BLOCK_SIZE / 2

        left   = half
        right  = SCREEN_WIDTH  - half
        bottom = half
        top    = SCREEN_HEIGHT - half
        thickness = 2

        # bottom
        arcade.draw_line(left,  bottom, right, bottom, TEXT_COLOR, thickness)
        # top
        arcade.draw_line(left,  top,    right, top,    TEXT_COLOR, thickness)
        # left
        arcade.draw_line(left,  bottom, left,  top,    TEXT_COLOR, thickness)
        # right
        arcade.draw_line(right, bottom, right, top,    TEXT_COLOR, thickness)

        for x, y in self.segments:
            arcade.draw_lbwh_rectangle_filled(
                x - half,
                y - half,
                BLOCK_SIZE,
                BLOCK_SIZE,
                SNAKE_COLOR
            )

        fx, fy = self.food_position
        arcade.draw_lbwh_rectangle_filled(
            fx - half,
            fy - half,
            BLOCK_SIZE,
            BLOCK_SIZE,
            FOOD_COLOR
        )

        # ── Draw score ──
        arcade.draw_text(f"Score: {self.score}", 10, 10, TEXT_COLOR, 16)

    def on_update(self, delta_time):
        self.move_timer += delta_time
        if self.move_timer < self.move_interval:
            return
        self.move_timer = 0.0

        # Compute new head position
        hx, hy = self.segments[0]
        if   self.direction == "UP":    hy += BLOCK_SIZE
        elif self.direction == "DOWN":  hy -= BLOCK_SIZE
        elif self.direction == "LEFT":  hx -= BLOCK_SIZE
        elif self.direction == "RIGHT": hx += BLOCK_SIZE

        # Clamp inside border
        half = BLOCK_SIZE / 2
        hx = max(half, min(hx, SCREEN_WIDTH  - half))
        hy = max(half, min(hy, SCREEN_HEIGHT - half))
        new_head = (hx, hy)

        # Self collision back to menu
        if new_head in self.segments:
            music.stop_game_music()
            from ui import MenuView   # avoid circular import at module top
            self.window.show_view(MenuView())
            return

        self.segments.appendleft(new_head)

        # Eat food????
        if new_head == self.food_position:
            self.score += 1
            self.spawn_food()
        else:
            self.segments.pop()

    def on_key_press(self, key, modifiers):
        if   key == arcade.key.UP    and self.direction != "DOWN":
            self.direction = "UP"
        elif key == arcade.key.DOWN  and self.direction != "UP":
            self.direction = "DOWN"
        elif key == arcade.key.LEFT  and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif key == arcade.key.RIGHT and self.direction != "LEFT":
            self.direction = "RIGHT"
