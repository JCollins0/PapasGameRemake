import pygame
from os.path import join
from constants import Constants
import colors

import sys
import os
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

constants = Constants()

pygame.font.init()
font = pygame.font.Font(resource_path('data/calibri.ttf'), constants.FONT_SIZE)
big_font = pygame.font.Font(resource_path('data/calibri.ttf'), constants.FONT_SIZE*2)
small_font = pygame.font.Font(resource_path('data/calibri.ttf'), constants.FONT_SIZE_SMALL)


screen = None
def init_utils(screen_ref):
    global screen
    screen = screen_ref

def load_image(name):
    if '.png' not in name and '.jpg' not in name:
        name = name + '.png'
    try:
        return [pygame.image.load(resource_path(join("images",name)))]
    except:
        print("EXCEPTION LOADING")
        return None

def load_image_and_rotate(name, rotation):
    image = load_image(name)[0]
    image = pygame.transform.rotate(image, rotation)
    return [image]

def load_sprite_sheet(name,im_width, im_height):
    images = list()
    sheet = load_image(name)[0]
    if sheet is None:
        return [None]
    w, h = sheet.get_size()
    for y in range(h // im_height ):
        for x in range(w // im_width):
            rect = pygame.Rect(x*im_width, y*im_height, im_width, im_height)
            image = pygame.Surface(rect.size,flags=0x00010000).convert_alpha()
            image.blit(sheet, (0,0), rect)
            images.append(image)
    return images

def draw_circle(c_x, c_y, radius,width=1, color=colors.black):
    pygame.draw.circle(screen,color, (int(c_x),int(c_y)),int(radius),width)

def draw_rect(color, x, y, width, height,outline_width=0):
    pygame.draw.rect(screen, color, (x,y,width,height), outline_width)

def draw_image(image, x,y):
    screen.blit(image,(x,y))

def draw_image_scaled(image, x,y, width,height, s_width, s_height):
    rect = pygame.Rect(x, y, width, height)
    surface = pygame.Surface(rect.size,flags=0x00010000).convert_alpha()
    surface.blit(image,(0,0))
    surface = pygame.transform.scale(surface, (s_width,s_height))
    screen.blit(surface, (x,y))

def get_font_size(text):
    return font.size(text)

def get_small_font_size(text):
    return small_font.size(text)

def draw_text(text, x,y,color=colors.black):
    textsurface = font.render(text, True, color)
    screen.blit(textsurface,(x,y))

def draw_text_scaled(text, x,y, s_width, s_height,color=colors.black):
    textsurface = font.render(text, True, color)
    textsurface = pygame.transform.scale(textsurface, (int(textsurface.get_width()*s_width),int(textsurface.get_height()*s_height)))
    screen.blit(textsurface,(x,y))

def draw_big_text(text, x,y,color=colors.black):
    textsurface = big_font.render(text, True, color)
    screen.blit(textsurface,(x,y))

def draw_big_text_scaled(text, x,y, s_width, s_height,color=colors.black):
    textsurface = big_font.render(text, True, color)
    textsurface = pygame.transform.scale(textsurface, (int(textsurface.get_width()*s_width),int(textsurface.get_height()*s_height)))
    screen.blit(textsurface,(x,y))

def draw_small_text(text, x,y,color=colors.black):
    textsurface = small_font.render(text, True, color)
    screen.blit(textsurface,(x,y))

def draw_small_text_scaled(text, x,y, s_width, s_height,color=colors.black):
    textsurface = small_font.render(text, True, color)
    textsurface = pygame.transform.scale(textsurface, (s_width,s_height))
    screen.blit(textsurface,(x,y))
