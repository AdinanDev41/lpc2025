import pygame
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

pygame.mixer.init()

# Sounds
BASE = Path(__file__).resolve().parent
sound_shot = pygame.mixer.Sound("atividade-009/sounds/fire.wav")
break_small = pygame.mixer.Sound("atividade-009/sounds/bagSmall.wav")
break_medium = pygame.mixer.Sound("atividade-009/sounds/bagMedium.wav")