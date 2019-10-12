# Sintaxe do socket:
#
#	socket(familia_enderecos, tipo)
#
#   	- Familia de end:
#            - ipv4 ou ipv6 (AF_INET ou AF_INET6)
#       - Tipo:
#            - TCP OU UDP (SOCK_STREAM ou SOCK_DGRAM)
import socket, os, random
from datetime import date
from _thread import *

def helper(): # printa funções e funcionalidades
	pass

def createId(): # gera novo id unico para email
	iD = 0
	while True:
		iD = random.randint(0,1000000) # maximo 1 milhao de emails no sistema
		if uniqueValue(iD, "id"): # se o id for unico, salva e sai do loop
			arq = open("regs/id.txt", "a+") # id.txt guarda os ids, serve apenas para checar se um novo id ja existe
			arq.write(iD+"\n")
			arq.close()
			break
	return iD

def uniqueValue(var, file): # verifica se um valor é unico(id ou username), parametro file DEVE ser: "id" ou "username"
	arq = open("regs/"+file+".txt", "r")
	lines = arq.readlines()
	for line in lines:
		if str(line) == str(var):
			return False
	return True

class Email:
	def __init__(self, title, msg, recipients, sender):
		self.id = createId()
		self.title = title
		self.msg = msg
		self.recipients = recipients # tem que ser uma lista
		self.sender = sender
		self.read = 0 # 0 para nao lido
		self.fav = 0 # 0 para nao favorito
		self.date = date.today() # data que foi criado o email, year-month-day

def login(): # faz o login do cliente
	pass

def register(username, passw): # registra o cliente
	if uniqueValue(username, "username"):
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


def clientthread(conn): # quando cliente se conecta, essa thread é iniciada
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

	helper()

	while True:
		data = recvMsg(conn)
		if not data:
			break
		print(data)
	conn.close()

###### CRIANDO CONEXOES #######
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "" 
porta = 8291

s.bind((host,porta)) # ativando, dexando o socket em escuta
s.listen(5) # maximo de numero de conexoes suportada

while True: # laco infinito pro servidor fica sempre na escuta
	conexao, endereco = s.accept()
	print("Conectado com ", endereco)
	start_new_thread(clientthread, (conexao,))
	

	


