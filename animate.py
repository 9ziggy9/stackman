import pygame

SPRITE_SCALE = 5
SPRITE_WIDTH = 48

def _scale_frames(frames, scale):
    return [(x*scale,y*scale,w*scale,h*scale) for (x,y,w,h) in frames]

def _construct_frames(num, length):
    return [(length * x, 0, length, length) for x in range(0,num)]

_sprite_sheet_run = pygame.image.load("./assets/run.png").convert_alpha()
_sprite_run = pygame.transform.scale(
    _sprite_sheet_run,
    (_sprite_sheet_run.get_width() * SPRITE_SCALE,
     _sprite_sheet_run.get_height() * SPRITE_SCALE)
)
_frames_run = _scale_frames(_construct_frames(8, SPRITE_WIDTH), SPRITE_SCALE)

# IDLE
_sprite_sheet_idle = pygame.image.load("./assets/idle.png").convert_alpha()
_sprite_idle = pygame.transform.scale(
    _sprite_sheet_idle,
    (_sprite_sheet_idle.get_width() * SPRITE_SCALE,
     _sprite_sheet_idle.get_height() * SPRITE_SCALE)
)
_frames_idle = _scale_frames(_construct_frames(10, SPRITE_WIDTH), SPRITE_SCALE)

# JUMP
_sprite_sheet_jump = pygame.image.load("./assets/jump.png").convert_alpha()
_sprite_jump = pygame.transform.scale(
    _sprite_sheet_jump,
    (_sprite_sheet_jump.get_width() * SPRITE_SCALE,
     _sprite_sheet_jump.get_height() * SPRITE_SCALE)
)
_frames_jump = _scale_frames(_construct_frames(3, SPRITE_WIDTH), SPRITE_SCALE)

# LAND
_sprite_sheet_land = pygame.image.load("./assets/land.png").convert_alpha()
_sprite_land = pygame.transform.scale(
    _sprite_sheet_land,
    (_sprite_sheet_land.get_width() * SPRITE_SCALE,
     _sprite_sheet_land.get_height() * SPRITE_SCALE)
)
_frames_land = _scale_frames(_construct_frames(9, SPRITE_WIDTH), SPRITE_SCALE)

# ROLL
_sprite_sheet_roll = pygame.image.load("./assets/roll.png").convert_alpha()
_sprite_roll = pygame.transform.scale(
    _sprite_sheet_roll,
    (_sprite_sheet_roll.get_width() * SPRITE_SCALE,
     _sprite_sheet_roll.get_height() * SPRITE_SCALE)
)
_frames_roll = _scale_frames(_construct_frames(7, SPRITE_WIDTH), SPRITE_SCALE)

# IDLE CROUCH
_sprite_sheet_icrouch = pygame.image.load("./assets/idle_crouch.png").convert_alpha()
_sprite_icrouch = pygame.transform.scale(
    _sprite_sheet_icrouch,
    (_sprite_sheet_icrouch.get_width() * SPRITE_SCALE,
     _sprite_sheet_icrouch.get_height() * SPRITE_SCALE)
)
_frames_icrouch = _scale_frames(_construct_frames(10, SPRITE_WIDTH), SPRITE_SCALE)

# LEDGE
_sprite_sheet_ledge = pygame.image.load("./assets/ledge.png").convert_alpha()
_sprite_ledge = pygame.transform.scale(
    _sprite_sheet_ledge,
    (_sprite_sheet_ledge.get_width() * SPRITE_SCALE,
     _sprite_sheet_ledge.get_height() * SPRITE_SCALE)
)
_frames_ledge = _scale_frames(_construct_frames(5, SPRITE_WIDTH), SPRITE_SCALE)

# PULL
_sprite_sheet_pull = pygame.image.load("./assets/pull.png").convert_alpha()
_sprite_pull = pygame.transform.scale(
    _sprite_sheet_pull,
    (_sprite_sheet_pull.get_width() * SPRITE_SCALE,
     _sprite_sheet_pull.get_height() * SPRITE_SCALE)
)
_frames_pull = _scale_frames(_construct_frames(6, SPRITE_WIDTH), SPRITE_SCALE)

# PUSH
_sprite_sheet_push = pygame.image.load("./assets/push.png").convert_alpha()
_sprite_push = pygame.transform.scale(
    _sprite_sheet_push,
    (_sprite_sheet_push.get_width() * SPRITE_SCALE,
     _sprite_sheet_push.get_height() * SPRITE_SCALE)
)
_frames_push = _scale_frames(_construct_frames(10, SPRITE_WIDTH), SPRITE_SCALE)

# SPIN
_sprite_sheet_spin = pygame.image.load("./assets/spin.png").convert_alpha()
_sprite_spin = pygame.transform.scale(
    _sprite_sheet_spin,
    (_sprite_sheet_spin.get_width() * SPRITE_SCALE,
     _sprite_sheet_spin.get_height() * SPRITE_SCALE)
)
_frames_spin = _scale_frames(_construct_frames(6, SPRITE_WIDTH), SPRITE_SCALE)

# WALL LAND
_sprite_sheet_wland = pygame.image.load("./assets/w_land.png").convert_alpha()
_sprite_wland = pygame.transform.scale(
    _sprite_sheet_wland,
    (_sprite_sheet_wland.get_width() * SPRITE_SCALE,
     _sprite_sheet_wland.get_height() * SPRITE_SCALE)
)
_frames_wland = _scale_frames(_construct_frames(6, SPRITE_WIDTH), SPRITE_SCALE)

# WALL SLIDE
_sprite_sheet_wslide = pygame.image.load("./assets/w_slide.png").convert_alpha()
_sprite_wslide = pygame.transform.scale(
    _sprite_sheet_wslide,
    (_sprite_sheet_wslide.get_width() * SPRITE_SCALE,
     _sprite_sheet_wslide.get_height() * SPRITE_SCALE)
)
_frames_wslide = _scale_frames(_construct_frames(3, SPRITE_WIDTH), SPRITE_SCALE)

# SNEAK
_sprite_sheet_sneak = pygame.image.load("./assets/walk_crouch.png").convert_alpha()
_sprite_sneak = pygame.transform.scale(
    _sprite_sheet_sneak,
    (_sprite_sheet_sneak.get_width() * SPRITE_SCALE,
     _sprite_sheet_sneak.get_height() * SPRITE_SCALE)
)
_frames_sneak = _scale_frames(_construct_frames(10, SPRITE_WIDTH), SPRITE_SCALE)

run     = (_sprite_run,     _frames_run)
idle    = (_sprite_idle,    _frames_idle)
jump    = (_sprite_jump,    _frames_jump)
land    = (_sprite_land,    _frames_land)
roll    = (_sprite_roll,    _frames_roll)
icrouch = (_sprite_icrouch, _frames_icrouch)
ledge   = (_sprite_ledge,   _frames_ledge)
pull    = (_sprite_pull,    _frames_pull)
push    = (_sprite_push,    _frames_push)
spin    = (_sprite_spin,    _frames_spin)
wland   = (_sprite_wland,   _frames_wland)
wslide  = (_sprite_wslide,  _frames_wslide)
sneak   = (_sprite_sneak,   _frames_sneak)
