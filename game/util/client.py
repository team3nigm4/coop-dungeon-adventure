import socket
import simplejson
from game.util.logger import Logger

class Client:

	def __init__(self, ip, port):
		self.ip = ip
		self.port = port
		self.setTimeout(0.005)

		self.isConnect = False
		self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.data = []

		self.clientId = socket.gethostbyname(socket.gethostname())

	def setIp(self, ip):
		self.ip = ip

	def setPort(self, port):
		self.port = port

	def setTimeout(self, time):
		socket.setdefaulttimeout(time)

	def connection(self):
		try :
			self.conn.connect((self.ip, self.port))
			self.me = str(self.conn.getsockname()[1])
			self.isConnect = True
		except Exception as e:
			Logger.warning("Client", "Error when connection to the server(" + str(self.ip) + ":" + str(self.port))
			print(e)
			self.isConnect = False

	def send(self, message):
		if self.isConnect:
			self.conn.send(bytes(simplejson.dumps(message), 'utf-8'))

	def receive(self):
		if self.isConnect:
			try:
				self.data = simplejson.loads(self.conn.recv(2000))
			except socket.timeout as e:
				pass

	def connectState(self):
		return self.isConnect

	def getClientId(self):
		return self.clientId

	def disconnection(self):
		self.conn.close()
		self.isConnect = False
