from twisted.internet import protocol, reactor
import names

COLORS = [
    '\033[31m', # RED
    '\033[32m', # GREEN
    '\033[33m', # YELLOW
    '\033[34m', # BLUE
    '\033[35m', # MAGENTA
    '\033[36m', # CYAN
    '\033[37m', # WHITE
    '\033[4m',  # UNDERLINE
]

transports = set()
users = set()

class Chat(protocol.Protocol):
    def connectionMade(self):
        name = names.get_first_name()
        color = COLORS[len(users) % len(COLORS)]
        users.add(name)
        transports.add(self.transport)

        self.transport.write(f'{color}{name}\033[0m'.encode())

    def dataReceived(self, data):
        for t in transports:
            if self.transport is not t:
                t.write(data)

class ChatFactory(protocol.Factory):
    def buildProtocol(self, addr):
        return Chat()

print('Server started!')
reactor.listenTCP(8000, ChatFactory())
reactor.run()
