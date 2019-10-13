# Sintaxe do socket:
#
#	socket(familia_enderecos, tipo)
#
#   	- Familia de end:
#            - ipv4 ou ipv6 (AF_INET ou AF_INET6)
#       - Tipo:
#            - TCP OU UDP (SOCK_STREAM ou SOCK_DGRAM)
import socket, os, random, pickle
from datetime import date
from _thread import *

import os.path

maX = 1000 # maximo de emails no sistema

aux=0
lidos=[]

class Email:
	def __init__(self, iD, title, msg, sender):
		self.iD = iD
		self.title = title
		self.msg = msg
		self.recipients = []
		self.sender = sender
		self.read = 0 # 0 para nao lido
		self.fav = 0 # 0 para nao favorito
		self.date = date.today() # data que foi criado o email, year-month-day


def helper(conn): # printa funções e funcionalidades
	sendMsg('\n	del - Deleta um email',conn)
	sendMsg('\n	email - Cria e envia um email',conn)
	sendMsg('\n	exit - Sai do programa',conn)
	sendMsg('\n	fav - marca um email como favorito',conn)
	sendMsg('\n	help - Mostra este manual',conn)
	sendMsg('\n	show inbox- Exibe os emails na caixa de entrada',conn)
	sendMsg('\n	show [id] - Exibe o email com determinado id',conn)
	sendMsg('\n	show fav - Exibe os emails favoritos',conn)
	sendMsg('\n	show notread - Exibe os emails não lidos',conn)
	sendMsg('\n	show sent - Exibe os emails enviados',conn)
	pass

def createId(): # gera novo id unico para email
	iD = 0
	while True:
		iD = random.randint(0,maX) 
		if uniqueValue(iD, "id"): # se o id for unico, salva e sai do loop
			arq = open("regs/id.txt", "a+") # id.txt guarda os ids, serve apenas para checar se um novo id ja existe
			arq.write(str(iD)+"\n")
			arq.close()
			break
	return iD

def uniqueValue(var, file): # verifica se um valor é unico(id de mail ou username), parametro file DEVE ser: "id" ou "username"
	arq = open("regs/"+file+".txt", "r")
	lines = arq.readlines()
	for line in lines:
		if str(line) == str(var)+'\n':
			return False
	return True

def createEmail(conn, username): # cria e salva um email. retorna id do mesmo
	sendMsg("Type the subject: ", conn)
	title = recvMsg(conn)
	sendMsg("Type the message: ", conn)
	msg = recvMsg(conn)
	iD = createId()
	email = Email(iD, title, msg, username)

	while True:
		sendMsg("Send to:", conn)
		recipient = recvMsg(conn)
		(email.recipients).append(recipient)
		sendMsg("Someone more? (y/n): ", conn)
		if recvMsg(conn) == 'n':
			break
		
	# para salvar o objeto email em um arquivo é preciso usar pickle para serializar o objeto em bytes
	serializedEmail = pickle.dump(email, open("regs/email.txt", "ab")) 
	return iD

def addFav(iD):
	arq = open("regs/fav.txt", "a+")
	if not isfav(iD):
		arq.write(str(iD)+'\n')
		return True
	return True

def isfav(iD):
	if os.path.exists("regs/fav.txt"):
		arq = open("regs/fav.txt", "r")
		lines = arq.readlines()
		for line in lines:
			if str(line) == str(str(iD)+'\n'):
				return True
	return False

def isread(emailID):
	arq =open("regs/lidos.txt",'r')
	lines = arq.readlines()

	for line in lines:
		if str(line) == str(str(emailID)+'\n'):
			return True
	return False
	pass

def showCommand(data, conn, username):
	#show inbox, show notread, show fav, show draft, show sent, show id
	arq = open("regs/email.txt", "rb")	

	try:
		while True:
			email = pickle.load(arq) # des-serializa o objeto email
			
			if data == 'inbox': # mostra a caixa de entrada
				if username in email.recipients:
					sendMsg('e-mail-> id: '+str(email.iD)+'. Subject: '+str(email.title), conn)

			if data == 'fav': # mostra os emails favoritos
				if (username in email.recipients) and isfav(email.iD) :
					sendMsg('e-mail-> id: '+str(email.iD)+'. Subject: '+str(email.title), conn)

			if data == 'sent': # mostra os emails enviados
				if (email.recipients) and (email.sender == username):
					sendMsg('e-mail-> id: '+str(email.iD)+'. Subject: '+str(email.title), conn)

			if data == 'notread':
				if (username in email.recipients) and (email.read == 0)and not isread(email.iD):
					sendMsg('e-mail-> id: '+str(email.iD)+'. Subject: '+str(email.title), conn)

			if data.isdigit(): # mostra um email baseado no seu id
				if email.iD == int(data):
					#email.read=1 # email é marcado como lido
					lidos=open('regs/lidos.txt','a+')
					lidos.write(str(email.iD)+'\n')
					sendMsg('e-mail-> Sender: '+str(email.sender)+'. Subject: '+str(email.title), conn)
					sendMsg('e-mail-> Msg: '+str(email.msg), conn)

	except EOFError:
		pass
	


def login(name,password,conn): # faz o login do cliente

	if not uniqueValue(name,'username'):#se encontrar usuario, ve se senha eh compativel
		resultado=compareNamepass(name,password)
		if resultado:
			sendMsg("Bem vindo, "+name,conn)
			return True
		else :
			sendMsg("Nome ou senha errados.",conn)
			return False
	else :
		sendMsg("Nome de usuário não encontrado.",conn)
		return False	
	pass

def compareNamepass(username,password):#ve se nome corresponde a senha
	i=0
	arq = open("regs/username.txt", "r")
	lines = arq.readlines()

	for line in lines:
		i=i+1
		if str(line) == str(username+'\n'):
			break
	j=0
	arq = open("regs/passw.txt", "r")
	lines = arq.readlines()
	for line in lines:
		j=j+1
		if j == i:
			if str(line) == str(password+'\n'):
				return True
			if str(line) != str(password+'\n'):
				return False
	return False
	pass


def register(username, passw): # registra o cliente
	if not uniqueValue(username, "username"):
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
	username = ""

	########################### LOGIN #################################
	while True: # só sairá desse looping se o usuário digitar 1 ou 2
		sendMsg("\nType 1 to login\nType 2 to register\n", conn)
		data = recvMsg(conn)

		if data == '1': # fazendo o login do cliente
			sendMsg("Enter your username: ", conn)
			username = recvMsg(conn)
			sendMsg("Enter your password: ", conn)
			passw = recvMsg(conn)
			if login(username, passw, conn):
				break

		if data == '2': # fazendo o registro do cliente
			sendMsg("Enter a username: ", conn)
			username = recvMsg(conn)
			sendMsg("Enter a password: ", conn)
			passw = recvMsg(conn)

			if not register(username, passw):
				sendMsg("Username already in use", conn)
				continue

			sendMsg("Cadastro feito!",conn)
			if login(username, passw, conn):
				break
			
		else : # se nao receber 1 ou 2, reportar erro
			sendMsg("Error: Invalid command.", conn)
    ###################################################################
	
	helper(conn) # printa os comandos pro cliente

    ################ TRATAMENTO DOS COMANDOS DO CLIENTE ###############
	while True:
		sendMsg("\nWaiting command:", conn)
		data = (recvMsg(conn)).split() # quebra o comando em uma lista

		if str(data[0]) == "show": # mostra email
			
			showCommand(str(data[1]), conn, username)

		if str(data[0]) == "email": # cria email

			try:
				iD = createEmail(conn, username)
				sendMsg("\nE-mail id: "+str(iD), conn)
			except:
				sendMsg("\nError. Could not create E-mail.", conn)

		if str(data[0]) == "del": # deleta email
			pass

		if str(data[0]) == "fav": # marca como favorito
			#sendMsg('Digite o id do email que você quer marcar como favorito:',conn)
			#iD=recvMsg(conn)
			addFav(data[1])
			

		if str(data[0]) == "help":
			helper()

		if str(data[0]) == "exit": # para o cliente sair
			sendMsg("Bye o/.", conn)
			break

	conn.close()
	###################################################################	
		


##################################
###### CRIANDO AS CONEXOES #######
##################################

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "" 
porta = 8291

s.bind((host,porta)) # ativando, dexando o socket em escuta
s.listen(5) # maximo de numero de conexoes suportada

while True: # laco infinito pro servidor fica sempre na escuta
	conexao, endereco = s.accept()
	print("Conectado com ", endereco)
	start_new_thread(clientthread, (conexao,))

	

	

