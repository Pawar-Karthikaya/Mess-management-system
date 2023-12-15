import socket

class backend_handeling:
    def send_menue(self,string):
        self.string=string
        ip = "127.0.0.1"
        port = 6644
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind((ip, port))
        server.listen(5)

        while True:
            client, address = server.accept()
            print(f"Connection Established - {address[0]}:{address[1]}")
            
            #string = client.recv(1024)
            #string = string.decode("utf-8")
            client.send(bytes(self.string, "utf-8"))
            
            client.close()