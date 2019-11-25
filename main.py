import pygame
from constants import Constants
constants = Constants()
pygame.init()
window = pygame.display
screen = window.set_mode((constants.SCREEN_WIDTH,constants.SCREEN_HEIGHT))

import sys
from objects import init_objects
import utils
from states import get_menu_state, init_states, update_states
from mouse_event import mouse_up, mouse_down, mouse_dragged,mouse_moved, get_mouse, get_mouse_dragged


# setup

window.set_caption("Papas Waffle House")

# pass screen to other files
init_objects(screen)
init_states(screen)
utils.init_utils(screen)
# starting state is menu
state = get_menu_state()

# create clock object to cap framerate
clock = pygame.time.Clock()
# Game Loop
running = True
color = (128,0,128)
while running:


    # clear screen
    screen.fill(color)
    # draw stuff related to current state
    state.draw()
    # special case for menu state
    if state is get_menu_state():
        state.update()
    else:
        # update all other states
        update_states()

    x, y = get_mouse()
    utils.draw_text(f"({x},{y})", x,y)
    # event polling
    for event in pygame.event.get():
        # exit event
        if event.type == pygame.QUIT:
            sys.exit()
        # mouse button down
        if event.type == pygame.MOUSEBUTTONDOWN:
            b1, b2, b3 = mouse_down()
            (mouse_x, mouse_y) = get_mouse()
            if b1:
                next_state, _ = state.interact_mouse_down(state, mouse_x, mouse_y)
                state = next_state
            elif b3: # temporary
                state = get_menu_state()
        elif event.type == pygame.MOUSEBUTTONUP:
            next_state, _ = state.interact_mouse_up(state, mouse_x, mouse_y)
            state = next_state
            (b1, b2, b3) = mouse_up()
            # color= (200, 100, 100)
        elif event.type == pygame.MOUSEMOTION:
            mouse_moved()
            # color = (100,100,200)
            mouse_x, mouse_y = get_mouse()
            b1, b2, b3 = mouse_dragged()

            if b1:
                nx, ny = get_mouse_dragged("L")
                next_state, _ = state.interact_drag(state, x,y,nx,ny)
                # color = (100,200,100)



            # if b1_down:
            #     color = (100,200,100)
            #     (mouse_x, mouse_y) = pygame.mouse.get_pos()
            #     next_state, _ = state.interact(state, mouse_x, mouse_y)
            #     state = next_state



    # update window
    window.update()
    clock.tick(60)
