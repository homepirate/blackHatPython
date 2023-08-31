import os
import paramiko
import socket
import shlex
import threading

CWD = os.path.dirname(os.path.realpath(__file__))
HOSKEY = paramiko.RSAKey(filename=os.path.join(CWD, 'test_rsa.key'))


class Server(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event