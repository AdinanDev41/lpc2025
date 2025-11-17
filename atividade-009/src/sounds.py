import pygame
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

pygame.mixer.init()

# Sounds
BASE = Path(__file__).resolve().parent
sound_shot = pygame.mixer.Sound("atividade-009/sounds/fire.wav")