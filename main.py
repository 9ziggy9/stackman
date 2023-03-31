import pygame
import pprint
import config
from enum import Enum

frame_idx = 0
animation_timer = 0

# TIME
clock = pygame.time.Clock()
dt = 0

pygame.init()
display = pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
pygame.display.set_caption("stackman -- dev")

# font for FPS monitoring
font = pygame.font.SysFont("Arial", 18)

# WEIRD, but I need pygame initialized before loading in sprites
import animate
import bg

class Action(Enum):
    IDLE = 0
    RUN  = 1
    PUSH = 2
    PULL = 3

def stackman_init():
    return {
        "action": Action.IDLE,
        "position": pygame.math.Vector2((0,72)),
        "velocity": pygame.math.Vector2((0, 0))
    }

def set_animation_frames(sm):
    if (sm["action"] == Action.RUN):
        (sprite, frames) = animate.run
        if (sm["velocity"][0] < 0):
            return (pygame.transform.flip(sprite, True, False),
                    frames)
        return (animate.run[0], animate.run[1])
    if (sm["action"] == Action.IDLE):
        frame_idx = 0
        return (animate.idle[0], animate.idle[1])

sm = stackman_init()
bg_layers = bg.init("./assets/level_types/hills", 42)

def apply_physics(sm):
    (dx, dy) = sm["velocity"] * dt
    sm["position"] += (dx, dy)
    return (dx, dy)

def update_position(sm):
    (dx,dy) = apply_physics(sm)
    for layer in bg_layers.values():
        for rect in layer["buffer"]:
            rect["position"] -= (dx * layer["scroll_rate"],
                                 dy * layer["scroll_rate"])

running = True
while running:
    (sprite, frames) = (None, None)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYUP:
            frame_idx = 0
            sm["action"] = Action.IDLE
            sm["velocity"] = pygame.math.Vector2((0,0))

    BASE_VELOCITY = 312.5
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        sm["velocity"] = pygame.math.Vector2((BASE_VELOCITY, 0))
        sm["action"] = Action.RUN
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        sm["velocity"] = pygame.math.Vector2((-BASE_VELOCITY, 0))
        sm["action"] = Action.RUN

    update_position(sm)

    for (level, layer) in bg_layers.items():
        #  Take head of buffer, it's position in the x direction
        if layer["buffer"][0]["position"][0] < -bg.IMAGE_WIDTH:
            bg_layers[level]["buffer"] = bg.buffer_rotate_right(layer["buffer"])
        if layer["buffer"][0]["position"][0] > 0:
            bg_layers[level]["buffer"] = bg.buffer_rotate_left(layer["buffer"])

    display.fill((0,0,0))

    # Q: is blitting, a waste, if it is not in display range?
    # A: https://stackoverflow.com/questions/39185187/
    # will-pygame-blit-sprites-with-a-rect-outside-the-display

    for (level, layer) in bg_layers.items():
        for rect in layer["buffer"]:
            display.blit(layer["surface"], rect["position"], rect["frame"])

    # SPRITE ANIMATION
    animation_timer += 1 / config.FPS

    (sprite, frames) = set_animation_frames(sm)

    if animation_timer >= config.ANIMATION_SPEED:
        frame_idx = (frame_idx + 1) % len(frames)
        animation_timer = 0

    if frame_idx > len(frames) - 1:
        frame_idx = 0
    frames = pygame.Rect(frames[frame_idx])
    display.blit(sprite,
                 ((config.DISPLAY_WIDTH -
                   animate.SPRITE_SCALE * animate.SPRITE_WIDTH)/2,
                  (config.DISPLAY_HEIGHT -
                   animate.SPRITE_SCALE * animate.SPRITE_WIDTH)/2 + 200),
                 frames)
    # END SPRITE ANIMATION

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(config.FPS) / 1000

    # display FPS
    fps_text = font.render(f"FPS: {round(clock.get_fps(),4)}", True, (255,255,255))
    display.blit(fps_text, (config.DISPLAY_WIDTH - fps_text.get_width(), 0))

    pygame.display.update()


pygame.quit()
