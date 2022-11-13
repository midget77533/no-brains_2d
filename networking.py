import socket
import threading
import pickle

class Server:
    def __init__(self, host, port, game):
        self.host = host
        self.port = port
        self.connections = []
        self.players = []
        self.p_num = 0
        self.GAME = game
        self.pfn = 0
        self.current_level = 0
    def start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.bind((self.host, self.port))
        self.s.listen(2)
        print(f'server succsesfully made on {self.host, self.port}')
        while self.GAME.running:
            conn, addr = self.s.accept()
            CT = threading.Thread(target=self.handle_clients, args=(conn, addr))
            CT.daemon = True
            CT.start()
            conn.send(pickle.dumps(addr))
            self.connections.append(conn)
    def handle_clients(self, c, a):
        while self.GAME.running:   
            try:
                data = c.recv(2048)
                data_v = pickle.loads(data)
                for p in range(len(self.players)):
                    if self.players[p][0] == data_v[0]:
                        if data_v[1] == "[QUIT]":
                            for conn in self.connections:
                                conn.send(pickle.dumps(["[MSG]",f"[SERVER]: {data_v[2]} left"]))
                            self.players.remove(self.players[p])
                if data_v[0] == "[INIT]":
                    aj = False
                    for i in self.players:
                        if i[0] == c:
                            aj = True
                            break
                    if not aj:
                        self.players.append([a, -300, 0, 0, 0, data_v[1]])
                        d = ["[URNUM]", a, len(self.players)]
                        c.send(pickle.dumps(d))
                    for conn in self.connections:
                        conn.send(pickle.dumps(["[MSG]",f"[SERVER]: {data_v[1]} joined"]))

                elif data_v[0] == "[MSG]":
                    for conn in self.connections:
                        conn.send(pickle.dumps(["[MSG]",f"{data_v[1]}"]))
                elif data_v[0] == "[MAP_CHANGE]":
                    if data_v[1] == "[1]":
                        self.pfn = 0
                    if data_v[1] == "[3]":
                        self.pfn += 1
                        print('PLAYER FINISHED')
                        if self.pfn >= len(self.players):
                            self.current_level += 1
                        data_v[2] = self.current_level
                    if (data_v[1] == "[3]" and self.pfn >= len(self.players)) or data_v[1] != "[3]":
                        if data_v[1] == "[3]":
                            self.pfn = 0
                            print("FINISHED")
                        for conn in self.connections:
                            conn.send(pickle.dumps(data_v))
                elif data_v == "[GET_DATA]":
                    c.send(pickle.dumps(["[DATA]",self.players]))
                elif data_v == "[PLAY]":
                    for conn in self.connections:
                        conn.send(pickle.dumps("[PLAY]"))
                else:
                    for p in self.players:
                        if p[0] == data_v[0]:
                            p[0] = data_v[0]
                            p[1] = data_v[1]
                            p[2] = data_v[2]
                            p[3] = data_v[3]
                            p[4] = data_v[4]
                            break
                    for conn in self.connections:
                        conn.send(pickle.dumps(["[DATA]",self.players]))
                if not data:
                    self.connections.remove(c)
                    for p in range(len(self.players)):
                        if self.players[p][0] == a:
                            for conn in self.connections:
                                conn.send(pickle.dumps(["[MSG]",f"[SERVER]: {self.players[p][5]} left"]))
                            self.players.remove(self.players[p])
                            break
                    c.close()
                    break
            except:
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
        self.messages = []
        self.visible_messages = []
        self.new_cmds = []
        self.running = False
        self.rsm = False
        self.lmc = []
        self.num = 0
    def run(self):
        self.running = True
        self.c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.c.connect((self.host,self.port))
        t = threading.Thread(target=self.receive_msg)
        t.start()

    def send_msg(self, msg):
        self.c.send(pickle.dumps(msg))
    def receive_msg(self):
        while self.running:
            received_msg = self.c.recv(2048)
            msg = pickle.loads(received_msg)
            if msg == "[PLAY]":
                self.rsm = True
            if msg[0] == "[URNUM]":
                self.id = msg[1]
                self.num = msg[2]
            if msg[0] == "[DATA]":
                self.players = msg[1]
            if msg[0] == "[MSG]":
                self.messages.append(msg[1])
                self.visible_messages.append([msg[1], 5])
                try:
                    for i in range(len(self.visible_messages)):
                        m = self.visible_messages[i]
                        if m[1] < 0:
                            self.visible_messages.remove(m)
                except:
                    pass
            if msg[0] == "[MAP_CHANGE]":
                self.lmc.append(msg)
def start_server(host, port, g):
    server = Server(host, port, g)
    server.start()    


if __name__ == "__main__":
    start_server(socket.gethostbyname(socket.gethostname()), 56354)
    
