import pygame
import config
from enum import Enum

dx = 50

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

class Action(Enum):
    IDLE = 0
    RUN  = 1
    PUSH = 2
    PULL = 3

class Dir(Enum):
    RIGHT = 0
    LEFT  = 1

def stackman_init():
    return {
        "action": Action.IDLE,
        "direction": Dir.RIGHT,
        "position": pygame.math.Vector2((0,72))
    }

def set_animation_frames(sm):
    if (sm["action"] == Action.RUN):
        (sprite, frames) = animate.run
        if (sm["direction"] == Dir.LEFT):
            return (pygame.transform.flip(sprite, True, False),
                    frames)
        return (animate.run[0], animate.run[1])
    if (sm["action"] == Action.IDLE):
        frame_idx = 0
        return (animate.idle[0], animate.idle[1])

BG_IMAGE_WIDTH = 1920
def bg_buffer_init(offset=72):
    return tuple(({
        "frame": pygame.Rect(0, 0, BG_IMAGE_WIDTH, config.DISPLAY_HEIGHT),
        "position": pygame.math.Vector2((idx * BG_IMAGE_WIDTH, offset))
    } for idx in range(0,3)))

def bg_buffer_rotate(buffer):
    # This is fucking stupid, use a ring buffer,
    # keep track of the head of the tuple
    buffer[0]["position"][0] = buffer[2]["position"][0] + BG_IMAGE_WIDTH
    return buffer[1:] + buffer[:1]

sm = stackman_init()
bg_layers = {
    "layer-1": {
        "buffer": bg_buffer_init(),
        "surface": pygame.image.load("./assets/bg1_e.png").convert_alpha(),
        "scroll_rate": 0.03125,
    },
    "layer-2": {
        "buffer": bg_buffer_init(120),
        "surface": pygame.image.load("./assets/bg1_d.png").convert_alpha(),
        "scroll_rate": 0.0625,
    },
    "layer-3": {
        "buffer": bg_buffer_init(180),
        "surface": pygame.image.load("./assets/bg1_c.png").convert_alpha(),
        "scroll_rate": 0.125,
    },
    "layer-4": {
        "buffer": bg_buffer_init(360),
        "surface": pygame.image.load("./assets/bg1_b.png").convert_alpha(),
        "scroll_rate": 0.25,
    },
}


running = True
while running:
    (sprite, frames) = (None, None)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYUP:
            frame_idx = 0
            sm["action"] = Action.IDLE

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        sm["position"] += (-dx,0)
        sm["direction"] = Dir.RIGHT
        sm["action"] = Action.RUN
        for layer in bg_layers.values():
            for rect in layer["buffer"]:
                rect["position"] += (-dx * layer["scroll_rate"], 0)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        sm["position"] += (dx,0)
        sm["direction"] = Dir.LEFT
        sm["action"] = Action.RUN
        for layer in bg_layers.values():
            for rect in layer["buffer"]:
                rect["position"] += (dx * layer["scroll_rate"], 0)

    for (level, layer) in bg_layers.items():
        #  Take head of buffer, it's position in the x direction
        if layer["buffer"][0]["position"][0] < -BG_IMAGE_WIDTH:
            bg_layers[level]["buffer"] = bg_buffer_rotate(layer["buffer"])

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
    fps = round(1 / dt, 2)
    fps_text = font.render(f"FPS: {fps}", True, (255,255,255))
    display.blit(fps_text, (config.DISPLAY_WIDTH - fps_text.get_width(), 0))

    pygame.display.update()


pygame.quit()
