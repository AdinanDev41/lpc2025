import pygame
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

pygame.mixer.init()

# Sounds
BASE = Path(__file__).resolve().parent
sound_shot = pygame.mixer.Sound("C:\\Users\\adina\\OneDrive\\Documents\\lpc2025\\lpc2025\\atividade-009\\sounds\\fire.wav")
break_small = pygame.mixer.Sound("C:\\Users\\adina\\OneDrive\\Documents\\lpc2025\\lpc2025\\atividade-009\\sounds\\bangSmall.wav")
break_medium = pygame.mixer.Sound("C:\\Users\\adina\\OneDrive\\Documents\\lpc2025\\lpc2025\\atividade-009\\sounds\\fire.wav")