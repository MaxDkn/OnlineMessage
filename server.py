import os
import socket
from _thread import *
import pickle
from datetime import datetime

"""
password data = {
                 name: password
                 }

data account = {
                name: {
                        'online': bool
                        'friend requests': {
                                            received: [], 
                                            sent: []
                                            }
                        'friends': []
                        'current game': str
                        }
                }
mails = [
         {'from': name, 'to': name, 'body': None, 'time': time},
         {'from': name, 'to': name, 'body': None, 'time': time},
        ]
"""


class DataBaseService:
    def __init__(self, root):
        self.path = root
        self.user = None
        self.init()

    def load_file(self, name_file):
        return pickle.loads(open(fr'{self.path}/data/{name_file}', 'rb').read())

    def save_file(self, name_file, data):
        pickle.dump(data, open(fr'{self.path}/data/{name_file}', 'wb'))

    def set_user(self, user):
        self.user = user

    def check_password(self, user, password):
        data = self.load_file('password data')

        try:
            if data[user] == password:
                return True
            else:
                return False
        except KeyError:
            return False
        except Exception as e:
            print(e)
            return False

    def check_user(self, user):
        data = self.load_file('password data')
        try:
            data[user]
        except KeyError:
            return False
        else:
            return True

    def write_mail(self, mail):
        mails = self.load_file('mails')
        mails.append(mail)
        self.save_file('mails', mails)

    def read_my_mails(self):
        mails = self.load_file('mails')
        my_mails = []
        for mail in mails:
            if mail['from'] == self.user or mail['to'] == self.user:
                my_mails.append(mail)

        return my_mails

    def check_if_friend(self, friend):
        data = self.load_file('data account')
        try:
            if friend in data[self.user]['friends']:
                return True
            else:
                return False
        except Exception as e:
            return e

    def get_friend_profile(self, friend):
        if self.check_if_friend(friend):
            return self.load_file('data account')[friend]
        else:
            return f'{friend} is not your friend! '

    def get_profile(self):
        return self.load_file('data account')[self.user]

    def set_online(self, boolean):
        data = self.load_file('data account')
        data[self.user]['online'] = boolean
        self.save_file('data account', data)

    def send_invitation(self, friend):
        data = self.load_file('data account')
        if not (friend in data[self.user]['friend requests']['received']):
            if not ((friend in data[self.user]['friend requests']['sent']) or (friend in data[self.user]['friends'])):
                data[self.user]['friend requests']['sent'].append(friend)
                data[friend]['friend requests']['received'].append(self.user)

                self.save_file('data account', data)
                return f'You have send a invitation to {friend}! '
            else:
                return f'You have already sent a friend request to {friend}'

        else:
            data[self.user]['friends'].append(friend)
            data[friend]['friend requests']['send'].remove(self.user)

            self.save_file('data account', data)
            print(f'{friend} is now your friend! ({self.user})')
            return f'{friend} is now your friend! '

    def accept_invitation(self, friend):
        data = self.load_file('data account')
        if friend in data[self.user]['friends']:
            if friend in data[self.user]['friend requests']['received']:
                data[self.user]['friend requests']['received'].remove(friend)
                data[friend]['friends'].append(self.user)
                data[self.user]['friends'].append(friend)
                data[friend]['friend requests']['sent'].remove(self.user)
                self.save_file('data account', data)
                return f'You have add {friend}'
            else:
                return f'Error: {friend} don\'t have do a request !'
        else:
            return f'{friend} is already your friend'

    def init(self):
        if not os.path.exists(fr'{self.path}/data'):
            os.mkdir(fr'{self.path}/data')

        if not os.path.exists(fr'{self.path}/data/mails'):
            self.save_file('mails', [])

        if not os.path.exists(fr'{self.path}/data/password data'):
            self.save_file('password data', {'max': 'PasswordOfMax',
                                             'arthur': 'PasswordOfArthur'
                                             })

        if not os.path.exists(fr'{self.path}/data/data account'):
            self.save_file('data account', {'max': {'pseudo': 'MaxDkn',
                                                    'online': False,
                                                    'friends': [],
                                                    'friend requests': {
                                                        'received': [],
                                                        'sent': []
                                                    },
                                                    'current game': None},

                                            'arthur': {'pseudo': 'Arthur',
                                                       'online': False,
                                                       'friends': [],
                                                       'friend requests': {
                                                           'received': [],
                                                           'sent': []
                                                       },
                                                       'current game': None, }
                                            })


class MailServer:
    def __init__(self, port, data_path):
        self.address_ip = socket.gethostbyname(socket.gethostname())
        self.port = port

        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.database_service = DataBaseService(data_path)

        try:
            self.server.bind((self.address_ip, self.port))
        except socket.error as e:
            str(e)

        self.server.listen()
        print(f'Waiting for a connection, Server Started in {self.address_ip} {self.port}')

    def threaded_client(self, connection, _):
        connection.send(str.encode(str(25)))
        user = None
        run = True

        while run:
            try:
                data = pickle.loads(connection.recv(4096))

                if not data:
                    run = False
                else:
                    self.database_service.init()

                    if data == 'CLOSE CONNECTION':
                        run = False
                        data_to_send = 'Connection Closed! '

                    elif data[:len('CHECK PASSWORD')] == 'CHECK PASSWORD':
                        data = data[len('CHECK PASSWORD'):]
                        user, password = data.split('|')
                        answer = self.database_service.check_password(user, password)
                        if answer:
                            self.database_service.set_user(user)
                            self.database_service.set_online(True)

                        data_to_send = answer

                    elif data[:len('MAIL')] == 'MAIL':
                        to, body = data[len('MAIL'):].split('|')

                        mail = {'from': user, 'to': to, 'body': body, 'time': str(datetime.now())[:-7]}
                        self.database_service.write_mail(mail)

                        data_to_send = 'Mail sent without difficult'

                    elif data == 'READ':
                        data_to_send = self.database_service.read_my_mails()

                    elif data[:len('GET FRIEND INFORMATION')] == 'GET FRIEND INFORMATION':
                        friend = data[len('GET FRIEND INFORMATION'):]

                        data_to_send = self.database_service.get_friend_profile(friend)

                    elif data == 'GET MY PROFILE':
                        data_to_send = self.database_service.get_profile()

                    elif data[:len('ADD')] == 'ADD':
                        friend = data[len('ADD'):]

                        data_to_send = self.database_service.send_invitation(friend)

                    elif data[:len('ACCEPT INVITATION')] == 'ACCEPT INVITATION':
                        friend = data[len('ACCEPT INVITATION'):]

                        data_to_send = self.database_service.accept_invitation(friend)

                    else:
                        data_to_send = data

                    connection.sendall(pickle.dumps(data_to_send))

            except EOFError:
                run = False

        connection.close()
        self.database_service.set_online(False)

    def run(self):
        while True:
            conn, addr = self.server.accept()
            print('Connected to:', addr)

            start_new_thread(self.threaded_client, (conn, None))


path = os.getcwd()
server = MailServer(5519, path)
server.run()
