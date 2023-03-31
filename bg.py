import pygame
import os
import config

IMAGE_WIDTH = 1920

def _buffer_init(offset=72):
    return tuple(({
        "frame": pygame.Rect(0, 0, IMAGE_WIDTH, config.DISPLAY_HEIGHT),
        "position": pygame.math.Vector2((idx * IMAGE_WIDTH, offset))
    } for idx in range(0,3)))

def buffer_rotate_right(buffer):
    # This is fucking stupid, use a ring buffer,
    # keep track of the head of the tuple
    buffer[0]["position"][0] = buffer[2]["position"][0] + IMAGE_WIDTH
    return buffer[1:] + buffer[:1]

def buffer_rotate_left(buffer):
    # This is fucking stupid, use a ring buffer,
    # keep track of the head of the tuple
    buffer[2]["position"][0] = buffer[0]["position"][0] - IMAGE_WIDTH
    return buffer[-1:] + buffer[:-1]

def init(path_to_bgs, base_offset):
    return {
        f"layer-{num}": {
            "buffer": _buffer_init(num * base_offset),
            "surface": pygame.image.load(path_to_bgs
                                         + f"/{num}.png").convert_alpha(),
            "scroll_rate": (num + 1),
        }
        for num in range(0, len([fn for fn in os.listdir(path_to_bgs)
                                 if fn.endswith(".png")]))
    }
