import socket


def tcp(host='www.google.com', port=80, data=None):
    target_host = host
    target_port = port

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((target_host, target_port))
    data = data or f'GET / HTTP/1.1\r\nHost: {target_host.strip("www.")}\r\n\r\n'
    client.send(bytes(data, 'utf-8'))
    response = client.recv(4096)

    print(response.decode())
    client.close()


def main():
    tcp()
    # tcp('0.0.0.0', 9998, 'HELLO') # send packets to tcp_server


if __name__ == '__main__':
    main()
