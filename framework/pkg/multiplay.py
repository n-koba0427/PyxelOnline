import asyncio

class EchoClientProtocol(asyncio.Protocol):
    def __init__(self, message, loop):
        self.message = message
        self.loop = loop
        self.data_received_event = asyncio.Event()
        self.received_data = None

    def connection_made(self, transport):
        transport.write(self.message.encode())

    def data_received(self, data):
        self.received_data = data.decode()
        self.data_received_event.set()

async def Request(request_type, message):
    loop = asyncio.get_event_loop()
    protocol = EchoClientProtocol(f"{request_type}:{message}", loop)
    coro = loop.create_connection(lambda: protocol, '3.104.38.31', 8888)
    await coro
    await protocol.data_received_event.wait()
    return protocol.received_data


async def Transmission(name, position, style):
    info = name + "," + ",".join(map(str, position + style))
    await Request("POST", info)
    all_info = await Request("GET", "ALL")
    return all_info