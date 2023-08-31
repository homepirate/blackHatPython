import socket
import threading
import sys


HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])


def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()

    result = []

    for i in range(0, len(src), length):
        word = str(src[i:i + length])

        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(w):02X}' for w in word])
        hexwidth = length * 3
        result.append(f'{i:04x} {hexa:<{hexwidth}} {printable}')

    if show:
        for line in result:
            print(line)

    return result


def receive_from(connection):
    buffer = b''
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as ex:
        print(ex)
    finally:
        return buffer


def response_handler(buffer):
    return buffer


def request_handler(buffer):
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))
    remote_buffer = None

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)
    if remote_buffer:
        remote_buffer = response_handler(remote_buffer)

        if len(remote_buffer):
            print(f'[<==] Sending {len(remote_buffer)} bytes to localhost.')
            client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            line = f'[==>] Received {len(remote_buffer)} bytes to localhost.'
            print(line)
            hexdump(local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print('[==>] Send to remote.')

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print(f'[<==] Received {len(remote_buffer)} bytes from remote.')
            hexdump(remote_buffer)

            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print('[<==] Send to localhost.')

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()

            print('[*] No more data. Closing connections.')
            break


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as ex:
        print(f"[!] Failed to listen {local_host}:{local_port}")
        print(ex)
        sys.exit(0)

    print(f"[*] Listen {local_host}:{local_port}")
    server.listen(5)

    while True:
        client_socket, addr = server.accept()
        line = f"> Received incoming connection from {addr[0]}:{addr[1]}"
        print(line)

        proxy_thread = threading.Thread(target=proxy_handler, args=(client_socket, remote_host, remote_port,
                                                                    receive_first))
        proxy_thread.start()


def start():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./tcp_proxy.py [localhost] [localport]", end='')
        print('[remotehost] [remoteport] [receive_first]')
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5]
    if receive_first == True:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)


def main():
    start()


if __name__ == '__main__':
    main()
