from itertools import product
import socket
import sys

args = sys.argv

def recvest():
    address = (hostname, port)
    g = gen_pass()
    with socket.socket() as sock:
        try:
            sock.connect(address)
            while True:
                msg = ''.join(next(g))
                sock.send(msg.encode())
                resp = sock.recv(1024)
                resp = resp.decode()
                if resp != "Wrong password!":
                    break
            if resp == "Connection success!":
                print(msg)
            else:
                print(resp)
        except ConnectionRefusedError:
            print("No connection!")

def gen_pass():
    with open('passwords.txt', 'r') as file:
        for word in file.readlines():
            word = word.strip()
            if word.lower() == word.upper():
                yield word
            else:
                yield from map(lambda x: ''.join(x), product(*([l.lower(), l.upper()] for l in word)))


hostname = args[1]
port = int(args[2])
recvest()
