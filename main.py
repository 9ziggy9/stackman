import pygame
import pprint
import config
import math
from enum import Enum

frame_idx = 0
animation_timer = 0

# TIME
clock = pygame.time.Clock()
dt = 0

pygame.init()
display = pygame.display.set_mode((config.DISPLAY_WIDTH,
                                   config.DISPLAY_HEIGHT))
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

class Dir(Enum):
    LEFT  = -1
    RIGHT =  1

STACKMAN_INITIAL_Y = 72
STACKMAN_INITIAL_X = 0

def stackman_init():
    return {
        "action": Action.IDLE,
        "direction": Dir.RIGHT,
        "position": pygame.math.Vector2((STACKMAN_INITIAL_X,
                                         STACKMAN_INITIAL_Y)),
        "velocity": pygame.math.Vector2((0, 0)),
        "max_speed": 312.5,
        "mass": 1, # 1 stackman
        "forces": {},
        "freefalling": False
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
        (sprite, frames) = animate.idle
        if (sm["direction"] == Dir.LEFT):
            return (pygame.transform.flip(sprite, True, False),
                    frames)
        return (animate.idle[0], animate.idle[1])

sm = stackman_init()
bg_layers = bg.init("./assets/level_types/hills", 42)

GROUND_LEVEL = 235
ground = {
    "frame": pygame.Surface((10 * config.DISPLAY_WIDTH, 2 * GROUND_LEVEL)),
    "position": pygame.math.Vector2((0, config.DISPLAY_HEIGHT - GROUND_LEVEL)),
}
ground["frame"].fill((20,20,20))

### BEGIN PHYSICS ENGINE ###
def run_acceleration(sm):
    if abs(sm["velocity"][0]) >= sm["max_speed"]:
        return (0,0)
    return (sm["direction"].value * 420 * dt, 0)

def x_friction(sm):
    if abs(sm["velocity"][0]) > 10:
        return (-sm["direction"].value * 420 * dt, 0)
    sm["velocity"][0] = 0
    sm["forces"] = {}
    sm["action"] = Action.IDLE
    return (0,0)

G_ACCELERATION = 420
def gravity(sm):
    assert sm["freefalling"], "Applying gravity when not falling!"
    if (sm["position"][1] > STACKMAN_INITIAL_Y):
        sm["velocity"][1] = 0
        sm["position"][1] = STACKMAN_INITIAL_Y
        sm["freefalling"] = False
        return (0,0)
    return (0, G_ACCELERATION * dt)

def has_forces(sm, *force_names):
    return any(force in sm["forces"] for force in force_names)

def apply_forces(sm):
    # generalize later, for now, f is strictly acceleration on unit mass
    for f in sm["forces"].values():
        sm["velocity"] += pygame.math.Vector2(f(sm))

def apply_physics(sm):
    ## HANDLE GRAVITY
    if "gravity" in sm["forces"]:
        if not sm["freefalling"]:
            del sm["forces"]["gravity"]
    elif sm["freefalling"]:
        sm["forces"]["gravity"] = gravity
    ## END GRAVITY
    apply_forces(sm)
    (dx, dy) = sm["velocity"] * dt
    sm["position"] += (dx, dy)
    return (dx, dy)

def clamp_ground(ground, is_falling):
    if not is_falling:
        ground["position"][1] = config.DISPLAY_HEIGHT - GROUND_LEVEL

def clamp_bg_layers(bg_layers, is_falling):
    if not is_falling:
        for (layer_num, layer) in enumerate(bg_layers.values()):
            for rect in layer["buffer"]:
                rect["position"][1] = layer_num * 72

def update_position(sm):
    (dx,dy) = apply_physics(sm)

    ground["position"] -= (dx, dy * 10) # hardcoded scrollrates
    clamp_ground(ground, sm["freefalling"])

    for layer in bg_layers.values():
        for rect in layer["buffer"]:
            rect["position"] -= (dx * layer["scroll_rate"], dy * layer["scroll_rate"])
    clamp_bg_layers(bg_layers, sm["freefalling"])
    
### END PHYSICS ENGINE ###
running = True
while running:
    (sprite, frames) = (None, None)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN:
            if e.key == 32: # 32 is spacebar
                sm["velocity"][1] = -100
                sm["freefalling"] = True
        if e.type == pygame.KEYUP:
            frame_idx = 0
            if "run_acceleration" in sm["forces"]:
                sm["forces"] = {}
                sm["forces"]["x_friction"] = x_friction

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        if not has_forces(sm, "run_acceleration", "x_friction"):
            sm["forces"]["run_acceleration"] = run_acceleration
            sm["action"] = Action.RUN
            sm["direction"] = Dir.RIGHT
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        if not has_forces(sm, "run_acceleration", "x_friction"):
            sm["forces"]["run_acceleration"] = run_acceleration
            sm["action"] = Action.RUN
            sm["direction"] = Dir.LEFT

    update_position(sm)

    for (level, layer) in bg_layers.items():
        #  Take head of buffer, it's position in the x direction
        if layer["buffer"][0]["position"][0] < -bg.IMAGE_WIDTH:
            bg_layers[level]["buffer"] = bg.buffer_rotate_right(layer["buffer"])
        if layer["buffer"][0]["position"][0] > 0:
            bg_layers[level]["buffer"] = bg.buffer_rotate_left(layer["buffer"])

    display.fill((0,0,0))

    # Q: is blitting, a waste, if it is not in display range?
    # A: NO -- https://stackoverflow.com/questions/39185187/
    # will-pygame-blit-sprites-with-a-rect-outside-the-display

    for (level, layer) in bg_layers.items():
        for rect in layer["buffer"]:
            display.blit(layer["surface"], rect["position"], rect["frame"])

    display.blit(ground["frame"], ground["position"])

    # SPRITE ANIMATION
    animation_timer += 1 / config.FPS

    (sprite, frames) = set_animation_frames(sm)

    # I think this is a naive way to interpolate
    animation_breakpoint = 0.0233 * math.exp(
        1.33 * (1 - (abs(sm["velocity"][0] / sm["max_speed"])))
    )

    if animation_timer >= animation_breakpoint:
        frame_idx = (frame_idx + sm["direction"].value) % len(frames)
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
