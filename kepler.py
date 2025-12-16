import math
import pygame
pygame.init()

height = 1280
width = 1920
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
dt = 0

position = pygame.math.Vector2((width / 2), (height / 2) + 200)
velocity = pygame.math.Vector2(200, 0)
v0 = velocity
acceleration = pygame.math.Vector2(0, 0)
size = 10

attractor_position = pygame.math.Vector2(width/2, height/2)
attractor_radius = 20
attractor_weight = 2e17  # masse fictive de l'attracteur

g = 6.67430e-11  # constante gravitationnelle

def frenet(position, velocity, acceleration, attractor_position):
    speed = math.sqrt(velocity.x**2 + velocity.y**2)             # norme de la vitesse
    Un = attractor_position - position                       # vecteur unitaire vers l'attracteur
    d = math.sqrt((Un.x**2 + Un.y**2))                     # distance à l'attracteur
    Un = Un.normalize()                         # normalisation du vecteur unitaire
    acceleration = (g * attractor_weight / d**2) * Un            # calcul de l'accélération gravitationnelle
    return acceleration

def movment(position, velocity, acceleration):
    position += velocity * dt + 0.5 * acceleration * dt * dt    # position = -1/2a•t² + v•t
    velocity += acceleration * dt                   # v = a•t

# IA
def draw_arrow(screen, vec, origin, color="blue", width=3, head_size=10):
    if vec.length_squared() == 0:
        return  # rien à dessiner si vecteur nul

    end = origin + vec

    # Ligne principale
    pygame.draw.line(screen, color, origin, end, width)

    # Vecteur unitaire dans la direction de la flèche
    direction = vec.normalize()

    # Vecteur perpendiculaire unitaire
    perp = pygame.math.Vector2(-direction.y, direction.x)

    # Base de la tête (un peu en arrière de l'extrémité)
    base = end - direction * head_size

    # Deux points de la tête
    left = base + perp * (head_size * 0.5)
    right = base - perp * (head_size * 0.5)

    # Dessin de la tête (triangle ouvert)
    pygame.draw.line(screen, color, end, left, width)
    pygame.draw.line(screen, color, end, right, width)

# IA
def draw_labeled_arrow(screen, vec, origin, color, label, scale=1.0):
    scaled_vec = vec * scale
    draw_arrow(screen, scaled_vec, origin, color)
    
    # Label avec norme
    font = pygame.font.SysFont(None, 24)
    text = font.render(f"{label}: {vec.length():.1f}", True, color)
    screen.blit(text, (origin.x + scaled_vec.x + 5, origin.y + scaled_vec.y))

running = True
while running:
    acceleration = frenet(position, velocity, acceleration, attractor_position)         # calcul de l'accélération
    movment(position, velocity, acceleration)                 # application du mouvement

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))  # Fond noir
    pygame.draw.circle(screen, (255, 0, 0), (position.x, position.y), size)
    pygame.draw.circle(screen, (255, 0, 0), (attractor_position.x, attractor_position.y), attractor_radius)

    # Vecteurs
    draw_labeled_arrow(screen, velocity, position, "blue", "v")     # vecteur vitesse
    draw_labeled_arrow(screen, acceleration, position, "green", "a")   # vecteur accélération
    pygame.display.flip()
    dt = clock.tick(60) / 1000  # Limite à 60 FPS
pygame.quit()
