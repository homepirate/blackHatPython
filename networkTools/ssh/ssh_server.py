import os
import sys
import paramiko
import socket
import threading

from config import USERNAME, PASSWORD


CWD = os.path.dirname(os.path.realpath(__file__))
HOSKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_channel_request(self, kind: str, chanid: int) -> int:
        if kind == 'session':
            return paramiko.common.OPEN_SUCCEEDED
        return paramiko.common.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username: str, password: str) -> int:
        if username == USERNAME and password == PASSWORD:
            return paramiko.common.AUTH_SUCCESSFUL


def main():
    server = '192.168.0.112'
    port = 2222

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((server, port))
        sock.listen(100)
        print('[*] LIstening for connection...')
        client, addr = sock.accept()
    except Exception as ex:
        print(f'[*] Listening failed {ex}')
        sys.exit(1)
    else:
        print('[*] Got a connection', client, addr)

    bhSession = paramiko.Transport(client)
    bhSession.add_server_key(HOSKEY)

    server = Server()
    bhSession.start_server(server=server)

    chan = bhSession.accept(20)
    if not chan:
        print('*** No channel!')
        sys.exit(1)

    print('[*] Authenticated!')
    print(chan.recv(1024).decode())
    chan.send('Welcome to bh_ssh')

    try:
        while True:
            command = input('Command: ')
            if command != 'exit':
                chan.send(command)
                r = chan.recv(8192)
                print(r.decode())
            else:
                chan.send('exit')
                print('Exiting')
                bhSession.close()
                break
    except KeyboardInterrupt:
        bhSession.close()


if __name__ == '__main__':
    main()
