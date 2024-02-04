import pygame
from Pygame_GUI_Tools import Input, Text, Button


class Draw:
    def __init__(self, window: pygame.display):
        self.window = window

        #  ##########################|LOGIN PAGE|##########################
        self.font_32 = pygame.font.SysFont('Segoe Print', 32, True)

        self.name_text = Text(self.window, 'Name', (445, 200), 'topleft', ('Segoe Print', 28, 'white', True, False))
        self.input_name = Input(self.window, ((445, 250), (580, 50)), ('Liberation Serif', False, False), (96, 122),
                                'right')

        self.password_text = Text(self.window, 'Password', (1165, 300), 'left',
                                  ('Segoe Print', 28, 'white', True, False))
        self.input_password = Input(self.window, ((714, 360), (580, 50)), ('Liberation Serif', False, False), (33, 122),
                                    'left', '•')
        '''self.submit_button = ButtonText(self.window, ('SUBMIT', (44, 44, 44)), ('Segoe Print', 48, True, False),
                                        (0, 255, 0), (600, 517, 400, 80))'''
        self.submit_button = Button(self.window, 'SUBMIT', ('Segoe Print', 48, True, False), 400, 80, (600, 517), 10)

        #  self.r1 = pygame.rect.Rect(445, 250, 400, 50)
        self.r2 = pygame.rect.Rect(714, 360, 580, 50)
        self.r3 = pygame.rect.Rect(600, 517, 400, 80)

        #  self.font_70 = pygame.font.SysFont('Segoe Print', 70)

        #  ##########################|LOGIN PAGE|##########################

    def login_page(self, event=None):
        self.window.fill((25, 25, 25))
        pygame.draw.rect(self.window, (163, 73, 164), (390, 167, 1017, 400), 8, 25)

        self.name_text.draw()

        self.input_name.update(event)
        self.input_name.draw()

        self.password_text.draw()

        self.input_password.update(event)
        self.input_password.draw()

        if self.submit_button.draw():
            return 'click'
