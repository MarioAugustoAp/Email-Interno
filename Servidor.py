# Sintaxe do socket:
#
#	socket(familia_enderecos, tipo)
#
#   	- Familia de end:
#            - ipv4 ou ipv6 (AF_INET ou AF_INET6)
#       - Tipo:
#            - TCP OU UDP (SOCK_STREAM ou SOCK_DGRAM)
import socket, os
from _thread import *

def login():
	pass

def existUsername(username): # retorna True se o username ja estiver sendo usado
	arq = open("regs/username.txt", "r")
	lines = arq.readlines()
	for line in lines:
		if str(line) == str(username):
			return True
	return False


def register(username, passw): # registra o cliente
	if existUsername(username):
		return False  #checa se ja existe o username
	arq1 = open("regs/username.txt", "a+")
	arq2 = open("regs/passw.txt", "a+")
	arq1.write(username+"\n")
	arq2.write(passw+"\n")
	arq1.close()
	arq2.close()
	return True


def clientthread(conn):
	while True:

		msgInicial = "\nWelcome\n\nType 1 to login\nType 2 to register" # primeira msg para cliente
		conn.send(msgInicial.encode('utf-8'))
		data = conn.recv(1024)

		if data.decode('utf-8') == '1': # fazendo o login do cliente
			login()
			break

		if data.decode('utf-8') == '2': # fazendo o registro do cliente
			msg = "Enter a username: "
			conn.send(msg.encode('utf-8'))
			username = (conn.recv(1024)).decode('utf-8')
			msg = "Enter a password: "
			conn.send(msg.encode('utf-8'))
			passw = (conn.recv(2014)).decode('utf-8')

			if not register(username, passw):
				msg = "Username already in use"
				conn.send(msg.encode('utf-8'))
				continue

			break

	while True:
		data = conn.recv(1024)
		if not data:
			break
		print(data.decode('utf-8'))
	conn.close()


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "" # quando eh vazio entende-se por localhost -> 127.0.0.1
porta = 8291 # pode ser quase qualquer porta

s.bind((host,porta)) # ativando, dexando o socket em escuta
s.listen(5) # maximo de numero de conexoes suportada


while True: # laco infinito pro servidor fica sempre na escuta
	conexao, endereco = s.accept()
	print("Conectado com ", endereco)
	start_new_thread(clientthread, (conexao,))
	

	


