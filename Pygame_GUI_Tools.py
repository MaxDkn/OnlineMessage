import pygame

import connection


class IDNavBar:
    def __init__(self,
                 window: pygame.display,
                 pos: tuple[int or float, int or float] or list[int or float, int or float],
                 size: tuple[int or float, int or float] or list[int or float, int or float],
                 side: str,
                 ):

        self.window = window
        self.pos_x, self.pos_y = pos
        self.width, self.height = size
        self.color = (32, 33, 36)

        self.rect = pygame.rect.Rect([0, 0, self.width, self.height])
        setattr(self.rect, side, [self.pos_x, self.pos_y])

    def update(self, conn: connection.Connect):
        for friend_count, friend in enumerate(conn.get_my_profile()['friends']):
            rect = pygame.rect.Rect([self.width * 0.85, 65])
            rect.center = self.width / 2 + self.pos_x, self.pos_y + (friend_count + 5) * 65
            pygame.draw.rect(self.window, (0, 0, 0), rect)

    def draw(self):
        pygame.draw.rect(self.window, self.color, self.rect, 0, 25)

        # Outline
        pygame.draw.rect(self.window, (255, 255, 255), self.rect, 5, 25)


class Prompt:
    def __init__(self,
                 window: pygame.display,  # The Surface to Display different Components
                 pos: tuple[int, int],  # Pos x | Pos y
                 width: int,  # The Width of the prompt
                 height: int,  # The Height of the prompt
                 font: tuple[str, bool, bool],  # Font Family Name | Bold | Italic
                 text: str = None,
                 side: str = 'topleft',
                 ):

        self.window = window
        self.pos_x, self.pos_y = pos
        self.width = width
        self.height = height
        self.font_name, bold, italic = font
        self.font_size = int(self.height / 2.657142857142857)
        self.default_text_obj = pygame.font.SysFont('Liberation Serif', self.font_size)\
            .render(text, True, (83, 87, 100))

        #  self.font = pygame.font.SysFont(self.font_name, int(self.height / 1.6), bold, italic)
        self.font = pygame.font.SysFont('Liberation Serif', int(self.height / 2.657142857142857))

        self.rect = pygame.rect.Rect([0, 0, self.width, self.height])
        setattr(self.rect, side, (self.pos_x, self.pos_y))

        self.active = True
        self.prompt_value = ''
        self.delay = 1000

        self.cross_obj = pygame.transform.scale(pygame.image.load('./assets/icon/marque-de-croix.png'), (20, 20))
        self.cross_rect = self.cross_obj.get_rect(center=(self.rect.left + 22, self.rect.top + 22.5))

        self.send_obj = pygame.transform.scale(pygame.image.load('./assets/icon/avion-en-papier (1).png'), (40, 40))
        self.send_rect = self.send_obj.get_rect(center=(self.rect.right - 20, self.rect.top + 21))

    def update(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.cross_rect.collidepoint(pygame.mouse.get_pos()):
                self.reset_value()

            elif self.rect.collidepoint(pygame.mouse.get_pos()):
                self.active = True

            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_BACKSPACE:
                self.prompt_value = self.prompt_value[:-1]

            elif 27 <= event.key <= 122:
                self.prompt_value += event.unicode

    def get_value(self):
        return self.prompt_value

    def reset_value(self):
        self.prompt_value = ''

    def draw(self):

        pygame.draw.rect(self.window, (65, 65, 80), self.rect, 0, 25)
        self.window.blit(self.send_obj, self.send_rect)
        prompt_obj = self.font.render(self.prompt_value, True, 'white')

        if self.prompt_value != '':
            self.window.blit(prompt_obj, (self.rect.left + 40, self.rect.top + 12))
            if self.active:
                self.window.blit(self.cross_obj, self.cross_rect)
                if pygame.time.get_ticks() % self.delay > self.delay / 2:
                    pygame.draw.line(self.window, 'white',
                                     (self.rect.left + 40 + prompt_obj.get_width(), self.rect.top + 12),
                                     (self.rect.left + 40 + prompt_obj.get_width(), self.rect.top + 30))

        else:
            self.window.blit(self.default_text_obj, (self.rect.left + 40, self.rect.top + 12))
            if self.active:
                if pygame.time.get_ticks() % self.delay > self.delay / 2:
                    pygame.draw.line(self.window, 'white',
                                     (self.rect.left + 40, self.rect.top + 12),
                                     (self.rect.left + 40, self.rect.top + 30))


class Input:
    def __init__(self,
                 window: pygame.display,
                 rect: tuple[tuple[float, float], tuple[float, float]],
                 font: tuple[str, bool, bool],
                 character_allowed: tuple[int, int],
                 cross_side: str,
                 show: str = None,
                 border_radius=3):

        self.window = window
        self.pos, self.size = rect
        self.font_name, self.bold, self.italic = font
        self.character_allowed = character_allowed
        self.show_character = show
        self.border_radius = border_radius
        self.cross_side = cross_side

        if self.border_radius <= 0:
            self.border_radius = 1
        self.font = pygame.font.SysFont(self.font_name, int(self.size[1] - 16), self.bold, self.italic)
        self.rect = pygame.rect.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])
        self.active = False
        self.input_value = ''
        self.input_text = self.font.render(self.input_value, True, 'white')
        self.cross_img = pygame.transform.scale(pygame.image.load(r'./assets/icon/cross.png'),
                                                (self.size[1] - 7, self.size[1] - 7))

        if self.cross_side == 'left':
            self.cross_rect = self.cross_img.get_rect(center=(self.rect.left - (self.size[1] - 5) / 2 - 8,
                                                              self.rect.centery))
        else:
            self.cross_rect = self.cross_img.get_rect(center=(self.rect.right + (self.size[1] + 5) / 2 + 6,
                                                              self.rect.centery))

        if self.show_character is not None:
            self.show = False
            self.show_open = pygame.transform.scale(pygame.image.load('./assets/icon/eye_open.png'),
                                                    (self.size[1] - 7, self.size[1] - 7))
            self.show_close = pygame.transform.scale(pygame.image.load('./assets/icon/eye_close.png'),
                                                     (self.size[1] - 7, self.size[1] - 7))

            self.show_img = self.show_close.copy()
            #  setattr(self.text_rect, self.side, self.pos)
            if self.cross_side == 'left':
                self.show_rect = self.show_img.get_rect(center=(self.rect.right + (self.size[1] + 5) / 2 + 6,
                                                                self.rect.centery))
            else:
                self.show_rect = self.show_img.get_rect(center=(self.rect.left - (self.size[1] - 5) / 2 - 8,
                                                                self.rect.centery))

    def update(self, event):
        if self.show_character is not None:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.show_rect.collidepoint(pygame.mouse.get_pos()):
                    if self.show == True:
                        self.show = False
                        self.show_img = self.show_close.copy()

                    else:
                        self.show = True
                        self.show_img = self.show_open.copy()

            if self.show:
                self.input_text = self.font.render(self.input_value, True, 'white')
            else:
                self.input_text = self.font.render(len(self.input_value) * self.show_character, True, 'white')
        else:
            self.input_text = self.font.render(self.input_value, True, 'white')

        rect_input_text = self.input_text.get_rect()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                self.active = True
            elif self.cross_rect.collidepoint(pygame.mouse.get_pos()):
                self.input_value = ''
            else:
                self.active = False

        if event.type == pygame.KEYDOWN and self.active:
            if self.character_allowed[0] <= event.key <= self.character_allowed[1] \
                    and rect_input_text.width + 40 < self.rect.width:
                self.input_value += event.unicode
            if event.key == pygame.K_BACKSPACE:
                self.input_value = self.input_value[:-1]
            if event.key == pygame.K_RETURN:
                self.active = False

    def get_value(self):
        return self.input_value

    def draw(self):
        if self.active:
            pygame.draw.rect(self.window, 'black', self.rect, 0, 10)

        pygame.draw.rect(self.window, 'white', self.rect, self.border_radius, 10)
        self.window.blit(self.input_text, (self.rect.x + 20, self.rect.top + 5))

        if self.show_character:
            self.window.blit(self.show_img, self.show_rect)
        self.window.blit(self.cross_img, self.cross_rect)


class Text:
    def __init__(self,
                 window: pygame.display,
                 text: str,
                 pos: tuple[int, int],
                 side: str,
                 font: tuple[str, int, str or tuple[int or tuple, int or tuple, int or tuple], bool, bool]
                 ):
        self.window = window
        self.text = text
        self.pos = pos
        self.side = side
        self.font_name, self.font_size, self.color, self.bold, self.italic = font

        self.font = pygame.font.SysFont(self.font_name, self.font_size, self.bold, self.italic)
        self.text_obj = self.font.render(self.text, True, self.color)
        self.rect = self.text_obj.get_rect()
        self.rect.topleft = self.pos
        #  setattr(self.rect, self.side, self.pos)

    def draw(self):
        self.window.blit(self.text_obj, self.rect)


class ButtonText:
    def __init__(self,
                 window: pygame.display,
                 text: tuple[str, str or tuple[int, int, int]],  # Text
                 font: tuple[str, int, bool, bool],  # Name of FontFamily | Size | Bold | Italic
                 color: str or tuple[int, int, int],  # Name of Color or RGB Color
                 rect: tuple[int, int, int, int],  # Pos x | Pos y | Width | Height
                 radius_rect: int = 8,
                 ):
        self.window = window
        self.text, color_text = text
        font_name, font_size, bold, italic = font
        self.color = color
        #  self.rect = rect
        self.rect = pygame.rect.Rect(rect)
        self.radius_rect = radius_rect

        self.font = pygame.font.SysFont(font_name, font_size, bold, italic)

        self.text_obj = self.font.render(self.text, True, color_text)
        self.text_rect = self.text_obj.get_rect(center=(self.rect.x + self.rect.width / 2,
                                                        self.rect.y + self.rect.height / 2))

    def get_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
            else:
                return False
        else:
            return False

    def draw(self):
        pygame.draw.rect(self.window, self.color, self.rect, 0, 25)
        self.window.blit(self.text_obj, self.text_rect)


class Button:
    def __init__(self, window, text, font: tuple[str, int, bool, bool], width, height, pos, elevation):
        # Core attributes
        self.window = window
        font_name, font_size, bold, italic = font

        self.pressed = False
        self.elevation = elevation
        self.dynamic_elevation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        # text
        self.font = pygame.font.SysFont(font_name, font_size, bold, italic)

        self.text_surf = self.font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(self.window, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(self.window, self.top_color, self.top_rect, border_radius=12)
        self.window.blit(self.text_surf, self.text_rect)

        return self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elevation = 0
                self.pressed = True
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed == True:
                    self.pressed = False
                    return True
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'
