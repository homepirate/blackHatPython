import ipaddress
import os
import socket
import struct
import sys
from config import HOST


#  sudo venv/bin/python sniffers/sniffer.py  FOR RUN CODE
# AND FOR EXAMPLE 'ping google.com' IN NEW TERMINAL


class IP:

    def __init__(self, buff=None):
        header = struct.unpack('<BBHHHBBH4s4s', buff)
        self.ver = header[0] >> 4
        self.ihl = header[0] & 0xF

        self.tos = header[1]
        self.len = header[2]
        self.id = header[3]
        self.offset = header[4]
        self.ttl = header[5]
        self.protocol_num = header[6]
        self.sum = header[7]
        self.src = header[8]
        self.dst = header[9]

        self.src_address = ipaddress.ip_address(self.src)
        self.dst_address = ipaddress.ip_address(self.dst)

        self.protocol_map = {1: 'ICMP', 6: 'TCP', 17: 'UDP'}
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except Exception as ex:
            print(f'{ex}\nNo protocol for {self.protocol_num}')


def sniff(host):
    if os.name == 'nt':
        socket_protocol = socket.IPPROTO_IP
    else:
        socket_protocol = socket.IPPROTO_ICMP

    shiffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
    shiffer.bind((host, 0))
    shiffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

    if os.name == 'nt':
        shiffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

    try:
        while True:
            raw_buffer = shiffer.recvfrom(65565)[0]
            ip_header = IP(raw_buffer[0:20])
            print(f'Protocol: {ip_header.protocol} {ip_header.src_address} -> {ip_header.dst_address}')
    except KeyboardInterrupt:
        if os.name == 'nt':
            shiffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)
        sys.exit()


def main():
    if len(sys.argv) == 2:
        host = sys.argv[1]
    else:
        host = HOST
    sniff(host)


if __name__ == '__main__':
    main()
