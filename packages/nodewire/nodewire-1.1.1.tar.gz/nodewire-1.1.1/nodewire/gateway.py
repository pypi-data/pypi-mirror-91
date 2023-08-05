#!/usr/bin/env python
import asyncio
import time
import sys
import glob
from serial import Serial
from nodewire.client import client
from nodewire.splitter import split, getnode, getsender, getinstance, getfulladdress, getsenderonly, getnodeonly, getfullsender
import requests
import configparser

instancename = ""
cp = ""
user = None
password = None
baudrate = 38400
server = 'http://cloud1.nodewire.org'

serialport = None

class ucolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class wcolors:
    HEADER = ''
    OKBLUE = ''
    OKGREEN = ''
    WARNING = ''
    FAIL = ''
    ENDC = ''
    BOLD = ''
    UNDERLINE = ''

if sys.platform.startswith('win'):
    bcolors = wcolors
else:
    bcolors = ucolors

def start():
    global instancename, cp, user, password, server
    config = configparser.RawConfigParser()
    try:
        config.read('nw.cfg')
        if 'server' in config: server = 'http://' + config['server']['address']
    except:
        print('could not find cp.cfg')
        print('please run from a directory that contains this file')
        quit()

    user = str(config.get('user', 'account_name'))
    password = str(config.get('user', 'password'))
    while True:
        with requests.Session() as s:
            try:
                res = s.post(server + '/login', data={'email': user, 'pw': password})
                if res.ok:
                    r = s.get(server + '/config').json()
                    instancename = str(r['instance'])
                    cp = r['server']
                    break
                else:
                    print(bcolors.FAIL + 'authentication failure' + bcolors.ENDC)
                    quit()
            except Exception as ex:
                print(
                    bcolors.WARNING + 'could not connect to cloud service. will retry after 30 seconds.' + bcolors.ENDC)
                time.sleep(30)

def openSerial():
    global serialport
    tries = 10
    print('searching for serial port...')

    while True:
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')
        sys.stdout.write(".")
        sys.stdout.flush()
        for port in ports:
            try:
                serialport = Serial(port, baudrate, timeout=1, write_timeout=1)
                serialport.reset_input_buffer()
                serialport.write('any ping cp\n'.encode())
                time.sleep(2)
                msg = serialport.readline().decode()
                serialport.write('any ping cp\n'.encode())
                msg = serialport.readline().decode()
                if msg.startswith('cp ThisIs') or msg.startswith('re ThisIs'):
                    print(bcolors.BOLD + 'serialport is on ' + port + bcolors.ENDC)
                    return serialport
                serialport.close()
            except Exception as exc:
                pass
        tries -= 1
        if tries == 0:
            print(bcolors.FAIL + 'giving up on serial port. will not support serial devices in this run' + bcolors.ENDC)
            return None
        time.sleep(30)


class Gateway():
    def __init__(self, client):
        self.scmd = bytearray()
        self.whenLastReceived = time.time()
        self.client = client
        self.sendqueue = asyncio.Queue()
        self.connected = False
        self.terminate = False
        self.ack = False

    async def keepalive(self):
        await asyncio.sleep(60)
        while True:
            self.ack = False
            try:
                if self.connected:
                    print('keepalive')
                    self.client.send('cp keepalive ' + user+'\n')
                else:
                    await self.start(asyncio.get_event_loop())
            except:
                await self.start(asyncio.get_event_loop())
            await asyncio.sleep(10)
            if not self.ack:
                print('didn\'t recieve ack')
                self.client.close_connection()
                await self.start(asyncio.get_event_loop())
            await asyncio.sleep(200)

    async def get_byte_async(self):
        while True:
            c = s.read(1)
            if c == b'' :
                await asyncio.sleep(0)
            else:
                s.write(c)
                self.whenLastReceived = time.time()
                return c

    async def uart_receive(self):
        while not self.terminate:
            b = await self.get_byte_async()
            if b!= b'\r' and b!=b'\n':
                self.scmd+=b
            elif len(self.scmd) != 0:
                print(bcolors.HEADER + self.scmd.decode('ascii') + bcolors.ENDC)
                if self.connected:
                    self.client.send(self.scmd.decode('ascii')+'\n')
                del self.scmd[:]


    async def start(self, loop):
        await self.client.sendasync('cp Gateway user={} pwd={} {}\n'.format(user,password,instancename))
        self.connected = True
        print('connected')
        serialport.write('any ping cp\n'.encode())

    def tcp_received(self, data):
        if data == 'disconnected':
            print(bcolors.WARNING + 'Lost Connection to Gateway' + bcolors.ENDC)
            self.connected = False
            # time.sleep(10)
            # tcp()
        else:
            self.ack = True
            datas = data.splitlines()
            for data in datas:
                node = getnode(data)
                if ':' in node:
                    nodeonly = node.split(':')[1]
                    data = data.replace(node, nodeonly).strip()
                self.sendqueue.put_nowait(data)

    async def uart_send(self):
        while not self.terminate:
            response = await self.sendqueue.get()
            #while time.time() - self.whenLastReceived < 0.01: await asyncio.sleep(0.01)
            s.write((response + '\n').encode())
            print(bcolors.OKBLUE + response + bcolors.ENDC)
            self.sendqueue.task_done()
            await asyncio.sleep(0)

if __name__ == '__main__':
    print(bcolors.BOLD + 'NodeWire Gateway' + bcolors.ENDC)
    print('version 1.0')
    print('Copyright 2020 nodewire.org')
    print('starting...')
    while True:
        start()
        s = openSerial()
        c = client()
        g = Gateway(c)
        c.received = g.tcp_received

        loop = asyncio.get_event_loop()

        tasks = [
            loop.create_task(c.connect(cp)),
            loop.create_task(g.start(loop)),
            loop.create_task(g.uart_receive()),
            loop.create_task(g.uart_send()),
            loop.create_task(g.keepalive())
        ]

        wait_tasks = asyncio.wait(tasks)
        try:
            loop.run_until_complete(wait_tasks)
        except KeyboardInterrupt:
            g.terminate = True