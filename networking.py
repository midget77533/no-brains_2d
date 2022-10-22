import socket
import threading
import pickle

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connections = []
        self.players = []
        self.p_num = 0
        
    def start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.s.listen()
        print(f'server succsesfully made on ({self.host, self.port}')
        while True:
            conn, addr = self.s.accept()
            CT = threading.Thread(target=self.handle_clients, args=(conn, addr))
            CT.daemon = True
            CT.start()
            conn.send(pickle.dumps(addr))
            self.connections.append(conn)

    def handle_clients(self, c, a):
        while True:   
            data = c.recv(2048)
            data_v = pickle.loads(data)
            for p in range(len(self.players)):
                if self.players[p][0] == data_v[0]:
                    if self.players[p][1] == "[QUIT]":
                        self.players.remove(self.players[p])
            if data_v[0] == "[INIT]":
                aj = False
                for i in self.players:
                    if i[0] == c:
                        aj = True
                        break
                if not aj:
                    self.players.append([a, 0, 0, 0, 0, data_v[1]])
                    d = ["[URNUM]", a]
                    c.send(pickle.dumps(d))
            elif data_v == "[GET_DATA]":
                c.send(pickle.dumps(["[DATA]",self.players]))
            else:
                #print(data_v)
                for p in self.players:
                    if p[0] == data_v[0]:

                        p[0] = data_v[0]
                        p[1] = data_v[1]
                        p[2] = data_v[2]
                        p[3] = data_v[3]
                        p[4] = data_v[4]

                        break
            if not data:
                self.connections.remove(c)
                for p in self.players:
                    if p[0] == a:
                        self.players.remove(p)
                        break
                c.close()
                break
class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.connections = []
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.format = 'utf-8'
        self.id = None
        self.players = []
    def run(self):
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c.connect((self.host,self.port))
        t = threading.Thread(target=self.receive_msg)
        t.start()
    def send_msg(self, msg):
        self.c.send(pickle.dumps(msg))
    def receive_msg(self):
        while True:
            received_msg = self.c.recv(2048)
            msg = pickle.loads(received_msg)
            print(msg)
            if msg[0] == "[URNUM]":
                self.id = msg[1]
            if msg[0] == "[DATA]":
                self.players = msg[1]
def start_server(host, port):
    for a in range(10):
        try:
            server = Server(host, port)
            server.start()    
            break
        except:
            port += 1

if __name__ == "__main__":
    # host = input("HOST: ")
    # port = input("PORT: ")
    # start_server(host, int(port))
    start_server('10.0.0.10', 12345)
