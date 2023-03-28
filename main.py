import pygame
import config
from enum import Enum

dx = 10

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

# background
# TODO: parallax scrolling
bg_imgs = (pygame.image.load("./assets/bg1_e.png").convert_alpha(),)
def bg_buffer_init(offset=0, damp=1):
    return tuple(({
        "frame": pygame.Rect(offset, offset, bg_imgs[0].get_width(), config.DISPLAY_HEIGHT),
        "position": pygame.math.Vector2((idx * bg_imgs[0].get_width(), 72)),
        "damp": damp
    } for idx in range(0,3)))

def bg_buffer_rotate(buffer):
    # This is fucking stupid, use a ring buffer,
    # keep track of the head of the tuple
    buffer[0]["position"][0] = buffer[2]["position"][0] + bg_imgs[0].get_width()
    return buffer[1:] + buffer[:1]

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

sm = stackman_init()
bgs = (bg_buffer_init(0,4),)

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
        for bg_buffer in bgs:
            for rect in bg_buffer:
                rect["position"] += (-rect["damp"] * dx,0)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        sm["position"] += (dx,0)
        sm["direction"] = Dir.LEFT
        sm["action"] = Action.RUN
        for bg_buffer in bgs:
            for rect in bg_buffer:
                rect["position"] += (rect["damp"] * dx,0)

    for bg_buffer in bgs:
        if bg_buffer[0]["position"][0] < -bg_imgs[0].get_width():
            bg_buffer = bg_buffer_rotate(bg_buffer)
            print(bg_buffer)

    display.fill((0,0,0))
    # Q: is blitting, a waste, if it is not in display range?
    # A: https://stackoverflow.com/questions/39185187/
    # will-pygame-blit-sprites-with-a-rect-outside-the-display
    for bg_buffer in bgs:
        for rect in bg_buffer:
            display.blit(bg_imgs[0], rect["position"], rect["frame"])

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
