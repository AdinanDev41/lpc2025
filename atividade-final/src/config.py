# Tela
WIDTH = 960
HEIGHT = 720
FPS = 60

# Game - Dificulty and Rounds
START_LIVES = 3
SAFE_SPAWN_TIME = 2.0  
WAVE_DELAY = 3.0       

# Progression of Difficulty
BASE_ENEMIES = 5       # I increased the number slightly because now they die faster.
ENEMIES_INC = 3        # Increases the number of enemies by +3 per round.
BASE_SPEED = 90.0      
SPEED_INC = 15.0       

# Nave
SHIP_RADIUS = 15
SHIP_TURN_SPEED = 220.0
SHIP_THRUST = 220.0
SHIP_FRICTION = 0.995
SHIP_FIRE_RATE = 0.2
SHIP_BULLET_SPEED = 420.0

# Asteroides
AST_SIZES = {
    "L": {"r": 30, "split": []}, 
    "M": {"r": 15, "split": []},
    "S": {"r": 8, "split": []},
}

# Bullet
BULLET_RADIUS = 2
BULLET_TTL = 1.0
MAX_BULLETS = 5

# UFO
UFO_RADIUS = 15
UFO_FIRE_RATE = 2.0
UFO_BULLET_SPEED = 300.0

# Color
WHITE = (240, 240, 240)
GRAY = (120, 120, 120)
BLACK = (0, 0, 0)
SEA_GREEN = (46, 139, 87)
MUSTARD_YELLOW = (255, 219, 88)
RED_DANGER = (255, 80, 80)

# Random
RANDOM_SEED = None