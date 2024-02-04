import pickle
import socket


class PasswordWrong(Exception):
    def __str__(self):
        return 'The Password or The Name Wrong!'


class Network:
    def __init__(self, addr: tuple):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.addr = addr
        self.player_count = self.connect()

    def get_player_count(self):
        return self.player_count

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except Exception as e:
            return e

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            return pickle.loads(self.client.recv(4096))
        except socket.error as e:
            return e


class Connect:
    def __init__(self, name: str, password: str, address: tuple):
        self.name = name
        self.password = password

        self.addr = address
        self.network = Network(address)

        if self.check_password(self.name, self.password) == True:
            pass
        else:
            raise PasswordWrong

    def check_password(self, user, password):
        result = self.network.send(f'CHECK PASSWORD{user}|{password}')
        return result

    def write_mail(self, to: str, body: str):
        result = self.network.send(f'MAIL{to}|{body}')
        return result

    def read_mails(self):
        mails = self.network.send('READ')
        return mails

    def get_friend_information(self, friend):
        result = self.network.send(f'GET FRIEND INFORMATION{friend}')
        return result

    def get_my_profile(self):
        result = self.network.send('GET MY PROFILE')
        return result

    def add_friend(self, friend):
        result = self.network.send(f'ADD{friend}')
        return result

    def accept_invitation(self, friend):
        result = self.network.send(f'ACCEPT INVITATION{friend}')
        return result

    def close_connection(self):
        result = self.network.send('CLOSE CONNECTION')
        return result
