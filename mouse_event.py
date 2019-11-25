import pygame

MOUSE1 = "L"
MOUSE2 = "R"
MOUSE3 = "M"

mouse_x, mouse_y = 0, 0

pressed = {MOUSE1: False, MOUSE2: False, MOUSE3: False}
mouse_at = { MOUSE1: [0,0], MOUSE2: [0,0], MOUSE3: [0,0]} #0=x,1=y
mouse_prev_at = { MOUSE1: [0,0], MOUSE2: [0,0], MOUSE3: [0,0]} #0=x,1=y

def mouse_down():
    b1, b2, b3 = pressed[MOUSE1], pressed[MOUSE2], pressed[MOUSE3]
    pressed[MOUSE1], pressed[MOUSE2], pressed[MOUSE3] = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    for k in pressed:
        if pressed[k]:
            mouse_at[k] = [mouse_x, mouse_y]
    return not b1 and pressed[MOUSE1], not b2 and pressed[MOUSE2], not b3 and pressed[MOUSE3]

def mouse_up():
    b1, b2, b3 = pressed[MOUSE1], pressed[MOUSE2], pressed[MOUSE3]
    pressed[MOUSE1], pressed[MOUSE2], pressed[MOUSE3] = pygame.mouse.get_pressed()
    mouse_x, mouse_y = pygame.mouse.get_pos()
    return b1 and not pressed[MOUSE1], b2 and not pressed[MOUSE2], b3 and not pressed[MOUSE3]

def mouse_dragged():
    b1, b2, b3 = pressed[MOUSE1], pressed[MOUSE2], pressed[MOUSE3]
    for k in pressed:
        if pressed[k]:
            mouse_prev_at[k] = [mouse_x, mouse_y]
            mouse_at[k] = [mouse_x, mouse_y]
    return b1, b2, b3

def mouse_moved():
    global mouse_x, mouse_y
    mouse_x, mouse_y = pygame.mouse.get_pos()

def get_mouse():
    return mouse_x, mouse_y

def get_mouse_dragged(button):
    assert (button is MOUSE1 or button is MOUSE2 or button is MOUSE3)
    return mouse_prev_at[button]
