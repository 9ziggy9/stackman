import pygame
import config
import animate

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

BTNS_UP = {119, 1073741906}
BTNS_LEFT = {97, 1073741904}
BTNS_DOWN = {115, 1073741905}
BTNS_RIGHT = {100, 1073741903}

ACTION_IDLE = 0
ACTION_RUN = 1
ACTION_PUSH = 2
ACTION_PULL = 3

DIR_RIGHT = 0
DIR_LEFT = 1

def stackman_init():
    return {
        "action": ACTION_IDLE,
        "direction": DIR_RIGHT,
        "position": pygame.math.Vector2((0,0))
    }

def set_animation_frames(sm):
    if (sm["action"] == ACTION_RUN):
        (sprite, frames) = animate.run
        if (sm["direction"] == DIR_LEFT):
            return (pygame.transform.flip(sprite, True, False),
                    frames)
        return (animate.run[0], animate.run[1])
    if (sm["action"] == ACTION_IDLE):
        frame_idx = 0
        return (animate.idle[0], animate.idle[1])

sm = stackman_init()

running = True
while running:
    (sprite, frames) = (None, None)
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYUP:
            frame_idx = 0
            sm["action"] = ACTION_IDLE

    keys = pygame.key.get_pressed()
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        sm["position"] += (10,0)
        sm["direction"] = DIR_RIGHT
        sm["action"] = ACTION_RUN
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        sm["position"] -= (10,0)
        sm["direction"] = DIR_LEFT
        sm["action"] = ACTION_RUN

    animation_timer += 1 / config.FPS

    (sprite, frames) = set_animation_frames(sm)

    if animation_timer >= config.ANIMATION_SPEED:
        frame_idx = (frame_idx + 1) % len(frames)
        animation_timer = 0

    display.fill((0,0,0)) # color in RGB
    if frame_idx > len(frames) - 1:
        frame_idx = 0
    frames = pygame.Rect(frames[frame_idx])
    display.blit(sprite, sm["position"], frames)

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
