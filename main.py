import pygame
import config
import animate

current_frame = 0
animation_timer = 0

pygame.init()
display = pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
pygame.display.set_caption("stackman -- dev")

stackman_x = animate.SPRITE_WIDTH * animate.SPRITE_SCALE / 2
stackman_y = animate.SPRITE_WIDTH * animate.SPRITE_SCALE / 2

running = True
while running:
    # event handling
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

    animation_timer += 1 / config.FPS

    (sprite, frames) = animate.run
    if animation_timer >= config.ANIMATION_SPEED:
        current_frame = (current_frame + 1) % len(frames)
        animation_timer = 0

    display.fill((0,0,0)) # color in RGB
    frame = pygame.Rect(frames[current_frame])
    display.blit(sprite, (stackman_x, stackman_y), frame)
    pygame.display.update()

pygame.quit()
