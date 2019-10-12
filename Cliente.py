
import socket
import threading

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "127.0.0.1"
porta = 8291

s.connect((host, porta))

def sendMsg():
	while True:
		s.send(input("").encode('utf-8'))

t = threading.Thread(target=sendMsg)
t.daemon = True
t.start()

while True:
	data = s.recv(1024)
	print(data.decode('utf-8'))
	if not data:
		break
#dados = (s.recv(1024)).decode('utf-8')
#print(dados)
#while True:
#	msg = str(input("input: ")) # envia msg para o servidor
#	s.send(msg.encode('utf-8'))

#	if msg == "stahp":
#		break
