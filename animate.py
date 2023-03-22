import pygame
import config

def _scale_frames(frames, scale):
    return [(x*scale,y*scale,w*scale,h*scale) for (x,y,w,h) in frames]

def _construct_frames(num, length):
    return [(length * x, 0, length, length) for x in range(0,num)]

_sprite_sheet_run = pygame.image.load("./assets/run.png")
_sprite_run = pygame.transform.scale(
    _sprite_sheet_run,
    (_sprite_sheet_run.get_width() * config.SPRITE_SCALE,
     _sprite_sheet_run.get_height() * config.SPRITE_SCALE)
)
_frames_run = _scale_frames(_construct_frames(8, config.SPRITE_LEN),
                            config.SPRITE_SCALE)

# IDLE
_sprite_sheet_idle = pygame.image.load("./assets/idle.png")
_sprite_idle = pygame.transform.scale(
    _sprite_sheet_idle,
    (_sprite_sheet_idle.get_width() * config.SPRITE_SCALE,
     _sprite_sheet_idle.get_height() * config.SPRITE_SCALE)
)
_frames_idle = _scale_frames(_construct_frames(10, config.SPRITE_LEN),
                             config.SPRITE_SCALE)

# JUMP
_sprite_sheet_jump = pygame.image.load("./assets/jump.png")
_sprite_jump = pygame.transform.scale(
    _sprite_sheet_jump,
    (_sprite_sheet_jump.get_width() * config.SPRITE_SCALE,
     _sprite_sheet_jump.get_height() * config.SPRITE_SCALE)
)
_frames_jump = _scale_frames(_construct_frames(3, config.SPRITE_LEN),
                             config.SPRITE_SCALE)

# LAND
_sprite_sheet_land = pygame.image.load("./assets/land.png")
_sprite_land = pygame.transform.scale(
    _sprite_sheet_land,
    (_sprite_sheet_land.get_width() * config.SPRITE_SCALE,
     _sprite_sheet_land.get_height() * config.SPRITE_SCALE)
)
_frames_land = _scale_frames(_construct_frames(9, config.SPRITE_LEN),
                             config.SPRITE_SCALE)

run = (_sprite_run, _frames_run)
idle = (_sprite_idle, _frames_idle)
jump = (_sprite_jump, _frames_jump)
land = (_sprite_land, _frames_land)
# END SPRITES AND FRAMES
