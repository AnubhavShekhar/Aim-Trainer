import math
import random
import pygame
import time
from typing import List, Tuple

pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Aim Trainer")

TARGET_INCREMENT = 400
TARGET_EVENT = pygame.USEREVENT
TARGET_PADDING = 30

BG_COLOR = (0, 25, 40)

LIVES = 3

GAME_STATS_HEIGHT = 50

LABEL_FONT = pygame.font.SysFont("MODERN WARFARE", 24)

class Target:
    MAX_SIZE = 30
    GROWTH_RATE = 0.2
    COLOR = "red"
    SECOND_COLOR = "white"

    def __init__(self, x: int, y: int) -> None:
        """
        Initialize the Target object.

        Args:
            x (int): The x-coordinate of the target.
            y (int): The y-coordinate of the target.
        """
        self.x = x
        self.y = y
        self.size = 0
        self.grow = True

    def update(self) -> None:
        """Update the target's size."""
        if self.size >= self.MAX_SIZE:
            self.grow = False

        if self.grow:
            self.size += self.GROWTH_RATE
        else:
            self.size -= self.GROWTH_RATE

    def draw(self, win: pygame.Surface) -> None:
        """
        Draw the target on the window.

        Args:
            win (pygame.Surface): The game window surface.
        """
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.8)
        pygame.draw.circle(win, self.COLOR, (self.x, self.y), self.size * 0.6)
        pygame.draw.circle(win, self.SECOND_COLOR, (self.x, self.y), self.size * 0.4)
    
    def collide(self, x: int, y: int) -> bool:
        """
        Check if the target collides with a point.

        Args:
            x (int): The x-coordinate of the point.
            y (int): The y-coordinate of the point.

        Returns:
            bool: True if the target collides with the point, False otherwise.
        """
        distance = math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)
        return distance <= self.size

def draw(win: pygame.Surface, targets: List[Target]) -> None:
    """
    Draw the game window.

    Args:
        win (pygame.Surface): The game window surface.
        targets (List[Target]): The list of targets to draw.
    """
    win.fill(BG_COLOR)

    for target in targets:
        target.draw(win)


def format_time(seconds: float) -> str:
    """
    Format time into a string in the format MM:SS:MS.

    Args:
        seconds (float): Time in seconds.

    Returns:
        str: Formatted time string.
    """
    ms = math.floor(int(seconds * 1000 % 1000) / 100)
    second = int(round(seconds % 60, 1))
    minutes = int(seconds // 60)

    return f"{minutes:02d}:{second:02d}:{ms}"

def game_stats(win: pygame.Surface, elapsed_time: float, targets_pressed: int, misses: int) -> None:
    """
    Display game statistics.

    Args:
        win (pygame.Surface): The game window surface.
        elapsed_time (float): Elapsed time in seconds.
        targets_pressed (int): Number of targets pressed.
        misses (int): Number of misses.
    """
    pygame.draw.rect(win, "grey", (0, 0, WIDTH, GAME_STATS_HEIGHT))
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "black")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed : {speed} t/s", 1, "black")

    hits_label = LABEL_FONT.render(f"Hits : {targets_pressed}", 1, "black")

    lives_label = LABEL_FONT.render(f"Lives : {LIVES - misses}", 1, "black")

    win.blit(time_label, (15, 15))
    win.blit(speed_label, (230, 15))
    win.blit(hits_label, (500, 15))
    win.blit(lives_label, (650, 15))

def end_screen(win: pygame.Surface, elapsed_time: float, targets_pressed: int, clicks: int) -> None:
    """
    Display the end screen with final statistics.

    Args:
        win (pygame.Surface): The game window surface.
        elapsed_time (float): Elapsed time in seconds.
        targets_pressed (int): Number of targets pressed.
        clicks (int): Total number of clicks.
    """
    win.fill(BG_COLOR)
    time_label = LABEL_FONT.render(f"Time: {format_time(elapsed_time)}", 1, "white")

    speed = round(targets_pressed / elapsed_time, 1)
    speed_label = LABEL_FONT.render(f"Speed : {speed} t/s", 1, "white")

    hits_label = LABEL_FONT.render(f"Hits : {targets_pressed}", 1, "white")

    if clicks > 0:
        accuracy = round(targets_pressed / clicks * 100, 1)
    else:
        accuracy = 0
    accuracy_label = LABEL_FONT.render(f"Accuracy : {accuracy}", 1, "white")

    win.blit(time_label, (get_centre_of_screen(time_label), 100))
    win.blit(speed_label, (get_centre_of_screen(speed_label), 200))
    win.blit(hits_label, (get_centre_of_screen(hits_label), 300))
    win.blit(accuracy_label, (get_centre_of_screen(accuracy_label), 400))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN:
                quit()

def get_centre_of_screen(surface: pygame.Surface) -> float:
    """
    Get the x-coordinate for centering a surface on the screen.

    Args:
        surface (pygame.Surface): The surface to be centered.

    Returns:
        float: The x-coordinate for centering.
    """
    return WIDTH / 2 - surface.get_width() / 2

def main() -> None:
    """Main function to run the game."""
    run = True
    targets = []

    clock = pygame.time.Clock()

    targets_pressed = 0
    clicks = 0
    misses = 0
    start_time = time.time()

    pygame.time.set_timer(TARGET_EVENT, TARGET_INCREMENT)

    while run:

        clock.tick(60)
        click = False
        mouse_position = pygame.mouse.get_pos()
        elapsed_time = time.time() - start_time

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == TARGET_EVENT:
                x = random.randint(TARGET_PADDING, WIDTH - TARGET_PADDING)
                y = random.randint(TARGET_PADDING + GAME_STATS_HEIGHT, HEIGHT - TARGET_PADDING)
                target = Target(x, y)
                
                if len(targets) < 7: # Limiting the no of targets on the screen to 6
                    targets.append(target)

            if event.type == pygame.MOUSEBUTTONDOWN:
                click = True
                clicks += 1

        for target in targets:
            target.update()
            
            if target.size <= 0: # remove target if it shrinks to 0
                targets.remove(target)
                misses += 1

            if click and target.collide(*mouse_position): # remove target if clicked upon
                targets.remove(target)
                targets_pressed += 1
        
        if misses >= LIVES: # end game if we loose all of our lives
            end_screen(WIN, elapsed_time, targets_pressed, clicks)


        draw(WIN, targets)
        game_stats(WIN, elapsed_time, targets_pressed, misses)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()