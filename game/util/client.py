# This class will make a connection with a server

import socket
import simplejson
import time

from threading import Thread

from game.util.logger import Logger


class Client(Thread):

	def __init__(self, ip, port):
		Thread.__init__(self)
		self.data = ""
		self.ip = ip
		self.port = port
		self.timeout = 0
		
		self.wantSend = False
		self.loop = False
		self.isConnect = False
		
		self.setTimeout(0.02)
		
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.clientId = socket.gethostbyname(socket.gethostname())

	def setIp(self, ip):
		self.ip = ip

	def setPort(self, port):
		self.port = port

	def setTimeout(self, time):
		self.timeout = time
		socket.setdefaulttimeout(time)

	def run(self):
		self.loop = True
		try :
			self.conn.connect((self.ip, self.port))
			self.me = str(self.conn.getsockname()[1])
			self.isConnect = True
		except socket.timeout as e:
			Logger.warning("Client", "Error when connecting to the server (" + str(self.ip) + ":" + str(self.port) + ")")
			print(e)
			self.isConnect = False
		except ConnectionRefusedError as e:
			Logger.warning("Client", "Connection refused")
			print(e)
			self.isConnect = False


		self.setTimeout(0.02)
		
		# Loop where at each time, client will see if
		# it must send a message to the server and will try
		# to receive data from the server
		while self.loop:
			if self.wantSend:
				self.theadSend()
				self.wantSend = False
			self.receive()

		self.disconnection()

	def send(self, message):
		self.wantSend = True
		self.message = message

	def theadSend(self):
		if self.isConnect:
			try:
				self.conn.send(bytes(simplejson.dumps(self.message), 'utf-8'))
			except OSError:
				self.isConnect = False
				self.end()

	def receive(self):
		if self.isConnect:
			try:
				tempData = self.conn.recv(2000)
				try:
					tempData = simplejson.loads(tempData)
					self.data = tempData
				except:
					pass
			except socket.timeout as e:
				pass
			except OSError:
				pass

	def end(self):
		self.loop = False
		time.sleep(0.3)
		self.join()

	def disconnection(self):
		if self.isConnect:
			self.conn.close()
			self.isConnect = False
			
	
	def connectState(self):
		return self.isConnect

	def getId(self):
		return self.clientId

	def getPort(self):
		return self.me
