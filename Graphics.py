import pygame
from pygame.locals import *

WHITE      = (255, 255, 255)
BLACK      = (  0,   0,   0)
RED        = (255,   0,   0)
BLUE       = (  0,   0, 255)
GREEN      = (  0, 255,   0)
GREY       = (173, 173, 173)
DARK_GREY  = ( 88,  88,  88)
LIGHT_GREY = (200, 200, 200)

class Init:
    def __init__(self, width, height):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = width, height
        self.UI_Component = []
 
    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        print('Loading font...')
        self._font = pygame.font.Font(pygame.font.match_font("serif"), 15)
        self._running = True

    def on_mouseDown (self):
        pass

    def uiIntercept (self, mouseState, pos) :
        for uiElement in self.UI_Component:
                elementRight  = uiElement['x'] + uiElement['w']
                elementBottom = uiElement['y'] + uiElement['h']
                if pos[0] > uiElement['x'] and pos[0] < elementRight and pos[1] > uiElement['y'] and pos[1] < elementBottom:
                    uiElement['hover'] = True
                    if mouseState == pygame.MOUSEBUTTONUP:
                        uiElement['clicked'] = False
                        uiElement['clickAction'](uiElement)
                        return 1
                    elif mouseState == pygame.MOUSEBUTTONDOWN:
                        uiElement['clicked'] = True
                        return 1
                    elif mouseState == pygame.MOUSEMOTION:
                        pass
                else:
                    uiElement['hover'] = False
 
    def on_event(self, event):
        pos = pygame.mouse.get_pos()
        
        # Check if click lands in a UI element
        if self.uiIntercept(event.type, pos) == 1:
            return

        if event.type == pygame.MOUSEBUTTONUP:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.on_mouseDown(pos)
        elif event.type == pygame.MOUSEMOTION:
            pass
        if event.type == pygame.QUIT:
            self._running = False
    def on_loop(self, g):
        pass
    def on_render(self, g):
        pass
    def on_cleanup(self):
        pygame.quit()

    def button(self, x, y, w, h, label, clickAction):
        newButton = {
            'x': x,
            'y': y,
            'w': w,
            'h': h,
            'clickAction': clickAction,
            'label': label,
            'clicked': False,
            'hover': True
        }
        self.UI_Component.append(newButton)
        return newButton

    def render_UI(self):
        for element in self.UI_Component:
            buttonColor = GREY

            if element['hover'] == True:
                buttonColor = LIGHT_GREY
                
            if element['clicked'] == False and element['hover'] == False:
                buttonColor = GREY
            elif element['clicked'] == True:
                buttonColor = DARK_GREY
                
            pygame.draw.rect(self._display_surf, buttonColor, [
                element['x'],
                element['y'],
                element['w'],
                element['h']], 0)
            pygame.draw.rect(self._display_surf, DARK_GREY, [
                element['x'],
                element['y'],
                element['w'],
                element['h']], 3)
                
            label = self._font.render(element['label'], 1, BLACK)
            
            self._display_surf.blit(label, [element['x'] + 10, element['y'] + 10])
 
    def on_execute(self):
        if self.on_init() == False:
            self._running = False
 
        while( self._running ):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop(self)
            self.on_render(self)

            # Render UI element on top of everything
            self.render_UI()
            
            pygame.display.update()
        self.on_cleanup()
