import pygame
import config
import animate

fr_run = 0
fr_icrouch = 0
fr_idle = 0
fr_jump = 0
fr_land = 0
fr_ledge = 0
fr_pull = 0
fr_push = 0
fr_roll = 0
fr_spin = 0
fr_sneak = 0
animation_timer = 0

# TIME
clock = pygame.time.Clock()
dt = 0

pygame.init()
display = pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
pygame.display.set_caption("stackman -- dev")

running = True
while running:
    # event handling
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    animation_timer += 1 / config.FPS

    (run_sprite,     run_frames)     = animate.run
    (idle_sprite,    idle_frames)    = animate.idle
    (icrouch_sprite, icrouch_frames) = animate.icrouch
    (jump_sprite,    jump_frames)    = animate.jump
    (land_sprite,    land_frames)    = animate.land
    (ledge_sprite,   ledge_frames)   = animate.ledge
    (pull_sprite,    pull_frames)    = animate.pull
    (push_sprite,    push_frames)    = animate.push
    (roll_sprite,    roll_frames)    = animate.roll
    (spin_sprite,    spin_frames)    = animate.spin
    (sneak_sprite,   sneak_frames)   = animate.sneak

    if animation_timer >= config.ANIMATION_SPEED:
        fr_run = (fr_run + 1) % len(run_frames)
        # fr_icrouch = (fr_icrouch + 1) % len(icrouch_frames)
        # fr_idle = (fr_idle + 1) % len(idle_frames)
        # fr_jump = (fr_jump + 1) % len(jump_frames)
        # fr_land = (fr_land + 1) % len(land_frames)
        # fr_ledge = (fr_ledge + 1) % len(ledge_frames)
        # fr_pull = (fr_pull + 1) % len(pull_frames)
        # fr_push = (fr_push + 1) % len(push_frames)
        # fr_roll = (fr_roll + 1) % len(roll_frames)
        # fr_spin = (fr_spin + 1) % len(spin_frames)
        # fr_sneak = (fr_sneak + 1) % len(sneak_frames)
        animation_timer = 0

    display.fill((0,0,0)) # color in RGB
    frame_run = pygame.Rect(run_frames[fr_run])
    # frame_icrouch = pygame.Rect(icrouch_frames[fr_icrouch])
    # frame_idle = pygame.Rect(idle_frames[fr_idle])
    # frame_jump = pygame.Rect(jump_frames[fr_jump])
    # frame_land = pygame.Rect(land_frames[fr_land])
    # frame_ledge = pygame.Rect(ledge_frames[fr_ledge])
    # frame_pull = pygame.Rect(pull_frames[fr_pull])
    # frame_push = pygame.Rect(push_frames[fr_push])
    # frame_roll = pygame.Rect(roll_frames[fr_roll])
    # frame_spin = pygame.Rect(spin_frames[fr_spin])
    # frame_sneak = pygame.Rect(sneak_frames[fr_sneak])
    display.blit(run_sprite, (0, 0), frame_run)
    # display.blit(icrouch_sprite, (0, 48 * 5), frame_icrouch)
    # display.blit(idle_sprite, (0, 48 * 5 * 2), frame_idle)
    # display.blit(jump_sprite, (0, 48 * 5 * 3), frame_jump)
    # display.blit(land_sprite, (48 * 5, 0), frame_land)
    # display.blit(ledge_sprite, (48 * 5, 48 * 5), frame_ledge)
    # display.blit(pull_sprite, (48 * 5, 48 * 5 * 2), frame_pull)
    # display.blit(push_sprite, (48 * 5, 48 * 5 * 3), frame_push)
    # display.blit(sneak_sprite, (48 * 5 * 2, 0), frame_sneak)
    pygame.display.update()

    # limits FPS to 60
    # dt is delta time in seconds since last frame, used for framerate-
    # independent physics.
    dt = clock.tick(config.FPS) / 1000
    print(dt)

pygame.quit()
