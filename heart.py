import pygame
import math
import random
import sys

# Initialize Pygame
pygame.init()

# Higher Resolution Window
WIDTH, HEIGHT = 900, 950
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Heart Protocol v24.04")
clock = pygame.time.Clock()

# Premium Color Palette
BLACK = (8, 8, 12)
NEON_PINK = (255, 60, 120)
DEEP_CHERRY = (140, 15, 50)
SOFT_WHITE = (240, 242, 245)
MUTED_GRAY = (90, 95, 105)

# Fonts
font_mono = pygame.font.SysFont("Courier", 18)
font_button = pygame.font.SysFont("Arial", 18, bold=True)
font_heart = pygame.font.SysFont("Arial", 11, bold=True) 

# Calligraphic Font Setup
font_center_letter = pygame.font.SysFont(["apple chancery", "georgia", "timesnewroman"], 110, italic=True, bold=True)

state = 0

class Particle:
    def __init__(self, base_x, base_y):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2 + 50
        
        self.base_x = base_x
        self.base_y = base_y
        
        self.text = random.choice(["love", "i love you", "you", "♥", "always"])
        self.color = (
            random.randint(230, 255), 
            random.randint(40, 90), 
            random.randint(110, 150)
        )
        self.speed = random.uniform(0.03, 0.06) 

    def update(self, pulse_factor):
        target_x = WIDTH // 2 + int(self.base_x * pulse_factor)
        target_y = HEIGHT // 2 - int(self.base_y * pulse_factor) + 50
        
        self.x += (target_x - self.x) * self.speed
        self.y += (target_y - self.y) * self.speed

    def draw(self, surface):
        text_surf = font_heart.render(self.text, True, self.color)
        surface.blit(text_surf, (self.x, self.y))

# --- Ring Layout Setup ---
particles = []

def get_heart_point(t):
    x = 16 * (math.sin(t) ** 3)
    y = 13 * math.cos(t) - 5 * math.cos(2*t) - 2 * math.cos(3*t) - math.cos(4*t)
    return x, y

LAYERS = [0.6, 0.8, 1.0, 1.2]  
PARTICLES_PER_LAYER = 350 
BASE_SCALE = 20  

for layer_scale in LAYERS:
    for i in range(PARTICLES_PER_LAYER):
        t = (i / PARTICLES_PER_LAYER) * 2 * math.pi
        t += random.uniform(-0.02, 0.02)
        
        x, y = get_heart_point(t)
        
        base_x = x * BASE_SCALE * layer_scale
        base_y = y * BASE_SCALE * layer_scale
        
        particles.append(Particle(base_x, base_y))

# UI Button Layout
button_rect = pygame.Rect(WIDTH // 2 - 130, HEIGHT // 2 - 20, 260, 50)

# --- Main App Loop ---
running = True
while running:
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == 0:
                state = 1
                
    if state == 0:
        t1 = font_mono.render("[system] Booting HEART_PROTOCOL_v4.2.exe...", True, NEON_PINK)
        t2 = font_mono.render("> Calligraphic sequence available.", True, SOFT_WHITE)
        screen.blit(t1, (WIDTH // 2 - t1.get_width() // 2, HEIGHT // 2 - 140))
        screen.blit(t2, (WIDTH // 2 - t2.get_width() // 2, HEIGHT // 2 - 100))
        
        pygame.draw.rect(screen, DEEP_CHERRY, button_rect, border_radius=8)
        pygame.draw.rect(screen, NEON_PINK, button_rect, 2, border_radius=8)
        
        btn_text = font_button.render("INITIALIZE DECRYPT", True, SOFT_WHITE)
        btn_rect = btn_text.get_rect(center=button_rect.center)
        screen.blit(btn_text, btn_rect)
        
    elif state == 1:
        current_time = pygame.time.get_ticks()
        
        # Heart Pulse Factor
        pulse_factor = 1.0 + 0.05 * math.sin(current_time * 0.004)
        
        # Draw the heart ring particles
        for p in particles:
            p.update(pulse_factor)
            p.draw(screen)
            
        # Independent glowing value loop (0.0 to 1.0)
        glow_wave = abs(math.sin(current_time * 0.0025))
        
        # Color shifting calculation
        glow_r = int(150 + (105 * glow_wave)) 
        glow_g = int(20 + (220 * glow_wave))  
        glow_b = int(60 + (185 * glow_wave))  
        glow_color = (glow_r, glow_g, glow_b)
        
        # Render the text canvas
        letter_surface = font_center_letter.render("D", True, glow_color)
        
        # --- FIXED ALIGNMENT HERE ---
        target_center_x = WIDTH // 2 + 35
        target_center_y = HEIGHT // 2 + 65
        
        letter_rect = letter_surface.get_rect(center=(target_center_x, target_center_y))
        screen.blit(letter_surface, letter_rect)
            
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
