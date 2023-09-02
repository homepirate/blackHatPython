import socket
import os
from config import HOST


#  sudo venv/bin/python sniffers/sniffer.py  FOR RUN CODE
# AND FOR EXAMPLE 'ping google.com' IN NEW TERMINAL

def sniff():
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    shiffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    shiffer.bind((HOST, 0))
    shiffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name == 'nt':
        shiffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    print(shiffer.recvfrom(65565))

    if os.name == 'nt':
        shiffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)


def main():
    sniff()


if __name__ == '__main__':
    main()

