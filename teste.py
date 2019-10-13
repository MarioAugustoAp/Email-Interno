import os, pickle

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


arq = open("regs/email.txt", "rb")

try:
	while arq:
		email = pickle.load(arq)
		print(email.iD)
except EOFError:
	break
#emails = pickle.load(arq)
#print(emails.iD)
#emails = pickle.load(arq)
#print(emails.iD)