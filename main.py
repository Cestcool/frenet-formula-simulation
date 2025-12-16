import math
import pygame
pygame.init()

height = 1280
width = 1920
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
dt = 0

position = pygame.math.Vector2((width / 2), (height / 2) + 200)
velocity = pygame.math.Vector2(100, 0)
acceleration = pygame.math.Vector2(0, 0)
size = 10

attractor_position = pygame.math.Vector2(width/2, height/2)
attractor_radius = 20

def frenet(position, velocity, acceleration, attractor_position):
    velocity = math.sqrt(velocity.x**2 + velocity.y**2)             # norme de la vitesse
    Un = attractor_position - position                       # vecteur unitaire vers l'attracteur
    d = math.sqrt((Un.x**2 + Un.y**2))                     # distance à l'attracteur
    Un = Un.normalize()                         # normalisation du vecteur unitaire
    acceleration = (velocity**2 / d) * Un            # calcul de l'accélération centripète
    return acceleration

def movment(position, velocity, acceleration):
    position += velocity * dt + 0.5 * acceleration * dt * dt    # position = -1/2a•t² + v•t
    velocity += acceleration * dt                    # v = a•t

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
    pygame.draw.line(screen, "blue", position, (position + acceleration), 3)    # vecteur accélération
    pygame.draw.line(screen, "green", position, (position + velocity), 3)   # vecteur vitesse
    pygame.display.flip()
    dt = clock.tick(60) / 1000  # Limite à 60 FPS
pygame.quit()
