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

def help(): # printa funções e funcionalidades
	pass

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

def sendMsg(text, conn): # envia mensagem
	conn.send(text.encode('utf-8'))

def recvMsg(conn): # recebe mensagem
	return (conn.recv(1024)).decode('utf-8')


def clientthread(conn): # quando cliente se conecta essa thread é iniciada
	sendMsg("\nWelcome user.\n", conn)
	while True: # só sairá desse looping se o usuário digitar 1 ou 2
		sendMsg("\nType 1 to login\nType 2 to register", conn)
		data = recvMsg(conn)

		if data == '1': # fazendo o login do cliente
			login()
			break

		if data == '2': # fazendo o registro do cliente
			sendMsg("Enter a username: ", conn)
			username = recvMsg(conn)
			sendMsg("Enter a password: ", conn)
			passw = recvMsg(conn)

			if not register(username, passw):
				sendMsg("Username already in use", conn)
				continue
			break
			
		else : # se nao receber 1 ou 2, reportar erro
			sendMsg("Error: Invalid command.", conn)

	help()

	while True:
		data = recvMsg(conn)
		if not data:
			break
		print(data)
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
	

	


