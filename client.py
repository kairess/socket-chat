import socket
import select
import sys

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('127.0.0.1', 8000))

name = None

while True:
    read, write, fail = select.select((s, sys.stdin), (), ())

    for desc in read:
        if desc == s:
            data = s.recv(4096)
            print(data.decode())

            if name is None:
                name = data.decode()
                s.send(f'{name} is connected!'.encode())
        else:
            msg = desc.readline()
            msg = msg.replace('\n', '')
            s.send(f'{name} {msg}'.encode())
