from pathlib import Path
import pygame as pg


BASE_PATH = Path(__file__).resolve().parent
SOUNDS_PATH = BASE_PATH.parent / "sounds"


def load_sound(filename: str, volume: float = 1.0) -> pg.mixer.Sound:
    # Loads a sound file from the sounds folder.
    path = SOUNDS_PATH / filename

    try:
        sound = pg.mixer.Sound(path)
        sound.set_volume(volume)
        return sound
    except FileNotFoundError:
        print(f"[WARN] Sound '{filename}' not found at '{path}'")
        return pg.mixer.Sound(buffer=b"")
    except Exception as e:
        print(f"[WARN] Failed to load sound '{filename}': {e}")
        return pg.mixer.Sound(buffer=b"")


if not pg.mixer.get_init():
    pg.mixer.init()


SHOT = load_sound("fire.wav", volume=0.6)
BREAK_LARGE = load_sound("bangLarge.wav", volume=0.7)
BREAK_MEDIUM = load_sound("bangMedium.wav", volume=0.7)

# New engine/flight sound for the UFO
FLY_NAVE = load_sound("flyNave.wav", volume=0.3)
