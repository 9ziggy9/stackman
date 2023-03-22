import pygame

DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 960
SPRITE_SCALE = 5
SPRITE_LEN = 48
FRAME_RATE = 60
ANIMATION_SPEED = 0.33 # this is in seconds

current_frame = 0
animation_timer = 0

pygame.init()
display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
pygame.display.set_caption("stackman")

def scale_frames(frames, scale):
    return [(x*scale,y*scale,w*scale,h*scale) for (x,y,w,h) in frames]

def construct_frames(num, length):
    return [(length * x, 0, length, length) for x in range(0,num)]

# SPRITES AND FRAMES
# RUN
sprite_sheet_run = pygame.image.load("./assets/run.png")
sprite_run = pygame.transform.scale(
    sprite_sheet_run,
    (sprite_sheet_run.get_width() * SPRITE_SCALE,
     sprite_sheet_run.get_height() * SPRITE_SCALE)
)
FRAMES_RUN = scale_frames(construct_frames(8, SPRITE_LEN), SPRITE_SCALE)

# IDLE
sprite_sheet_idle = pygame.image.load("./assets/idle.png")
sprite_idle = pygame.transform.scale(
    sprite_sheet_idle,
    (sprite_sheet_idle.get_width() * SPRITE_SCALE,
     sprite_sheet_idle.get_height() * SPRITE_SCALE)
)
FRAMES_IDLE = scale_frames(construct_frames(10, SPRITE_LEN), SPRITE_SCALE)

# JUMP
sprite_sheet_jump = pygame.image.load("./assets/jump.png")
sprite_jump = pygame.transform.scale(
    sprite_sheet_jump,
    (sprite_sheet_jump.get_width() * SPRITE_SCALE,
     sprite_sheet_jump.get_height() * SPRITE_SCALE)
)
FRAMES_JUMP = scale_frames(construct_frames(3, SPRITE_LEN), SPRITE_SCALE)

# LAND
sprite_sheet_land = pygame.image.load("./assets/land.png")
sprite_land = pygame.transform.scale(
    sprite_sheet_land,
    (sprite_sheet_land.get_width() * SPRITE_SCALE,
     sprite_sheet_land.get_height() * SPRITE_SCALE)
)
FRAMES_LAND = scale_frames(construct_frames(9, SPRITE_LEN), SPRITE_SCALE)

# END SPRITES AND FRAMES

stackman_x = SPRITE_LEN * SPRITE_SCALE / 2
stackman_y = SPRITE_LEN * SPRITE_SCALE / 2

running = True
while running:
    # event handling
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    animation_timer += 1 / FRAME_RATE

    if animation_timer >= ANIMATION_SPEED:
        current_frame = (current_frame + 1) % len(FRAMES_LAND)
        animation_timer = 0

    display.fill((0,0,0)) # color in RGB
    frame_rect = pygame.Rect(FRAMES_LAND[current_frame])
    display.blit(sprite_land, (stackman_x, stackman_y),frame_rect)
    pygame.display.update()

pygame.quit()
