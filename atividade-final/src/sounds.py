from pathlib import Path
import pygame as pg

BASE_PATH = Path(__file__).resolve().parent
# Ajuste o caminho se necessário. Aqui assume que 'sounds' está uma pasta acima ou na mesma raiz.
SOUNDS_PATH = BASE_PATH.parent / "sounds" 
if not SOUNDS_PATH.exists():
    SOUNDS_PATH = BASE_PATH / "sounds" # Tenta na mesma pasta

def init_mixer() -> None:
    if not pg.mixer.get_init():
        pg.mixer.init()

def load_sound(filename: str, volume: float = 1.0) -> pg.mixer.Sound:
    try:
        sound_path = SOUNDS_PATH / filename
        sound = pg.mixer.Sound(sound_path)
        sound.set_volume(volume)
        return sound
    except FileNotFoundError:
        print(f"AVISO: Som {filename} não encontrado em {SOUNDS_PATH}")
        # Retorna um som vazio para não crashar o jogo
        return pg.mixer.Sound(buffer=bytearray([0]*100))

init_mixer()

SHOT = load_sound("fire.wav", volume=0.6)
BREAK_LARGE = load_sound("bangLarge.wav", volume=0.9)
BREAK_MEDIUM = load_sound("bangMedium.wav", volume=0.8)
FLY_BIG = load_sound("flyBig.wav", volume=0.1) # Usado para inimigos gerais agora
FLY_SMALL = load_sound("flySmall.wav", volume=0.1)