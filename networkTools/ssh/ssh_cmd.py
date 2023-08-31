import paramiko


def ssh_command(ip, port, user, password, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=password)

    _, stdout, stderr = client.exec_command(cmd)

    output = stdout.readlines() + stderr.readlines()

    if output:
        print('---Output---')
        for line in output:
            print(line.strip())


def main():
    import getpass
    user = input('Username: ')
    passwd = getpass.getpass()

    ip = input("Enter ip: ") or '192.168.0.112'
    port = input('Enter port: ') or 2222
    cmd = input('Enter command: ') or 'id'

    ssh_command(ip, int(port), user, passwd, cmd)


if __name__ == '__main__':
    main()