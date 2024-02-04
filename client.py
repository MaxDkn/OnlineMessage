import pygame
import connection
from draw_management import Draw
import Pygame_GUI_Tools as P_GUI_T
pygame.init()
"""
TO DO LIST: 
    Rework the server for add account and more (friends, online)
    - Do the MainApp
    
    - Print the error when the password is wrong
    - print if the server is not start or the client is not connected
    
    Rework the prompt for a better aesthetic
    Ameliorate the button of login page
    Rework the PasswordPage for look like ChatGPT because i like the aesthetic
    Join the function that returns friends' information with the one that returns its own information
    Redo the cross
"""


def get_connection(addr):
    run = True
    clock = pygame.time.Clock()
    window = pygame.display.set_mode((1500, 900))
    draw = Draw(window)
    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if draw.login_page(event):
                try:
                    conn = connection.Connect(draw.input_name.get_value().lower(),
                                              draw.input_password.get_value(), addr)
                except Exception as e:
                    print(f'Error, {e.__str__()}')
                else:
                    return window, conn

            #  input_pygame.update(event)

        #  input_pygame.draw()
        clock.tick(125)
        pygame.display.update()

    return window, None


class MainApp:
    def __init__(self, display: pygame.display, connect: connection.Connect):
        self.display = display
        self.connection = connect
        print(self.connection.get_friend_information('arthur'))

        pygame.display.set_caption('Client Message')
        pygame.display.set_icon(pygame.image.load('./assets/icon/e-mail.png'))

        self.clock = pygame.time.Clock()

        self.prompt = P_GUI_T.Prompt(self.display, (750, 900 - 50), 800, 43, ('Liberation Serif', False, False),
                                     'Write a message...', 'center')
        self.navigation_bar = P_GUI_T.IDNavBar(self.display, [1320, 15], [160, 872], 'topleft')

    def run(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                self.prompt.update(event)
            self.draw()
            pygame.display.update()
            self.clock.tick(20)

    def update(self):
        self.navigation_bar.update(self.connection)

    def draw(self):
        self.display.fill((53, 53, 65))
        self.prompt.draw()
        self.navigation_bar.draw()


#  screen, connect = get_connection(('192.168.1.26', 5519))
#  MainApp(screen, connect).run()
window, co = get_connection(('192.168.1.26', 5519))

MainApp(window, co).run()
