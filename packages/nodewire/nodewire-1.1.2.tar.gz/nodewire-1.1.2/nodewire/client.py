import asyncio
import inspect

class client():
    def __init__(self):
        self.reader = None
        self.writer = None
        self.received = None
        self.managed = True

    async def connect(self, serverHost='cloud1.nodewire.org', failed=None):
        while True:
            try:
                print('connecting to {} ...'.format(serverHost))
                self.reader, self.writer = await asyncio.open_connection(serverHost, 10001)
                while True:
                    try:
                        data = await self.reader.readline()
                        if len(data)==0 and self.received:
                            if inspect.iscoroutinefunction(self.received):
                                asyncio.create_task(self.received('disconnected'))
                            else:
                                self.received('disconnected')
                            break
                        if self.received:
                            try:
                                if inspect.iscoroutinefunction(self.received):
                                    asyncio.create_task(self.received(data.decode().strip()))
                                else:
                                    self.received(data.decode().strip())
                            except Exception as ex1:
                                print(str(ex1))
                                if not self.managed: raise
                    except ConnectionError as ex: # todo use specified exception type
                        print(str(ex))
                        if self.received:
                            if inspect.iscoroutinefunction(self.received):
                                await self.received('disconnected')
                            else:
                                self.received('disconnected')
                        break
                print('Close the socket')
                if failed!=None:
                    failed(serverHost)
                self.writer.close()
                self.writer = None
                await asyncio.sleep(10)
                print('trying to reconnect...')
            except Exception as Ex: # todo get the relevant exceptions: TimeoutError
                print(f'failed to connect:{Ex}')
                if failed!=None:
                    failed(serverHost)
                    break
                await asyncio.sleep(30)
                print('trying to reconnect...')

    def close_connection(self):
        if not self.writer is None:
            self.writer.close()
            self.writer = None

    async def sendasync(self, message):
        while(self.writer==None): await asyncio.sleep(1)
        self.writer.write(message.encode())

    def send(self, message):
        self.writer.write(message.encode())

if __name__ == '__main__':
    c = client()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(c.connect())
    except KeyboardInterrupt:
        pass
    loop.close()