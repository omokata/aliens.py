import pygame
import sys
import os

dir_path = os.path.split(__file__)
HIGHSCORE_FILE = os.path.join(dir_path[0], "score.txt")

def resource_path(relative_path):
    """
    This is just to deal with pyinstaller stuff.
    I don't know enough but I guess during runtime,
    it points sys._MEIPASS to the _internal. At least
    this is true for onedir i guess. but maybe they talk more about
    it here: https://pyinstaller.org/en/stable/advanced-topics.html
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    print(os.path.join(base_path, relative_path))
    return os.path.join(base_path, relative_path)

def load_image(path):
    try:
        surface = pygame.image.load(resource_path(path))
        return surface.convert_alpha()
    except Exception as err:
        raise SystemExit(f"Could not load image {path}: {str(err)}")


def load_sound(path):
    try:
        sound = pygame.mixer.Sound(resource_path(path))
        return sound
    except Exception as err:
        raise SystemExit(f"Could not load sound {path}: {str(err)}")

def save_score(score):
    try:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(f"{score}")
    except Exception as err:
        print(f"Failed to save high score {score}: {str(err)}")
        return

def load_score():
    try:
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read().strip())
    except Exception as err:
        print(f"Failed to load score: {str(err)}")
        return 0
