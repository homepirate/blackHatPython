import socket


def udp(host='127.0.0.1', port=9997, data='AAABBBCCC'):
    target_host = host
    target_port = port

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client.sendto(bytes(data, 'utf-8'), (target_host, target_port))
    result, addr = client.recvfrom(4096)

    print(result.decode(), addr)
    client.close()


def main():
    udp()


if __name__ == '__main__':
    main()
