import socket
import simplejson
from game.util.logger import Logger

from threading import Thread

class Client(Thread):

	def __init__(self, ip, port):
		Thread.__init__(self)
		self.ip = ip
		self.port = port
		self.timeout = 0
		self.setTimeout(0.0145)

		self.isConnect = False
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.data = ""

		self.clientId = socket.gethostbyname(socket.gethostname())
		self.wantSend = False
		self.loop = False

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
			Logger.warning("Client", "Error when connection to the server(" + str(self.ip) + ":" + str(self.port))
			print(e)
			self.isConnect = False

		self.setTimeout(0.0145)
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
			self.conn.send(bytes(simplejson.dumps(self.message), 'utf-8'))

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

	def connectState(self):
		return self.isConnect

	def getId(self):
		return self.clientId

	def getPort(self):
		return self.me

	def end(self):
		self.loop = False

	def disconnection(self):
		if self.isConnect:
			self.conn.close()
			self.isConnect = False
