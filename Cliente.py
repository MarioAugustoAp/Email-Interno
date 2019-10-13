import socket, threading, sys

##################################################
############# CABEÇALHO DA CONEAXO ###############
##################################################
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "127.0.0.1"
porta = 8291
##################################################

try: # tentativa de conexao
	s.connect((host, porta))

except ConnectionRefusedError:
	print("Failed to connect.")
	sys.exit()

def sendMsg(): # metodo para enviar msg
		while True:
			s.send(input("").encode('utf-8'))

try:
	# cria uma thread para poder enviar as mensagens ao mesmo tempo que recebe:
	t = threading.Thread(target=sendMsg)
	t.daemon = True
	t.start()

	while True: # recebe e printa as mensagens
		data = s.recv(1024)
		if not data:
			break
		print(data.decode('utf-8'))

except:
	print("Server internal error.")
