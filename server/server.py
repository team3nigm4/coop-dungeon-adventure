#!/usr/bin/python

import socket
import select
import time
import sys
import simplejson
import datetime
import colorama
from threading import Thread

colorama.init()

is_running = True
reset = False
do_reset = True

buffer_size = 2000
delay = 0
clients = {}
class Logger:
	def log(text):
		print("[" + datetime.datetime.now().strftime("%H:%M:%S") + "] " + text)

	def format(text):
		return '[' + datetime.datetime.now().strftime("%H:%M:%S") + '] ' + text

	def info(text):
		print('[' + '\033[96m' + datetime.datetime.now().strftime("%H:%M:%S") + '\033[0m' + '] ' + text)

	def success(text):
		print('[' + '\033[92m' + datetime.datetime.now().strftime("%H:%M:%S") + '\033[0m' + '] ' + text)

	def warning(text):
		print('[' + '\033[93m' + datetime.datetime.now().strftime("%H:%M:%S") + '\033[0m' + '] ' + text)

	def error(text):
		print('[' + '\033[91m' + datetime.datetime.now().strftime("%H:%M:%S") + '\033[0m' + '] ' + text)

	def bold(text):
		print('\033[1m' + text + '\033[0m')

	def rec(text):
		print('[← IN] :')
		print(text)

	def send(text):
		print('[→ OUT] :')
		print(text)

class Commands():

	def do_echo(*args):
		print(' '.join(args))

	def do_raise(*args):
		Logger.error("Ceci est une erreur")

	def do_stop(*args):
		global is_running
		is_running = False
		Logger.error("Stopped !")

	def do_data(*args):
		Logger.bold('\nData of the clients :\n' + simplejson.dumps(clients) + '\n')

	def do_help(*agrs):
		Logger.warning('echo - raise  - stop - data - help')

	def do_reset(*agrs):
		Logger.warning('Restarting server')
		global reset
		reset = True
		Commands.do_stop()

class CdaServer(Commands):

	def __init__(self, host, port):
		self.host = host
		self.port = port

		self.input_list = []
		self.channel = {}

		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.server.bind((host, port))
		self.server.listen(200)

		self.gameBegin = False
		self.reset(0)
		self.reset(1)

		# to_send -> gameState = 0, inputs = 1, player pos = 2, player attrib = 3
			# gameState -> play = 0, stop = 1, disconnect = 2

		# players -> state = 0, info = 1
			# state -> connection = 0, player = 1, wait = 2
			# info -> inputs = 0, player pos = 1
		self.to_send = [{}, {}]
		self.to_send[0]['0'] = 1
		self.to_send[1]['0'] = 1
		print(self.to_send)

	def main_loop(self):

		print("---------------------------------------------")
		print("")
		print("   ___ ___   _     ___")
		print("  / __|   \\ /_\\   / __| ___ _ ___ _____ _ _ ")
		print(" | (__| |) / _ \\  \\__ \\/ -_) '_\\ V / -_) '_|")
		print("  \\___|___/_/ \\_\\ |___/\\___|_|  \\_/\\___|_|  ")
		print("")
		print("---------------------------------------------")
		Logger.success("Server started on " + str(self.host) + ":" + str(self.port) + "!")
		self.input_list.append(self.server)
		Logger.warning('Waiting for players...')

		while 1:
			inputr, outputr, exceptr = select.select(self.input_list, [], [])
			for self.s in inputr:
				if self.s == self.server:
					self.on_accept()
					break
				else:
					self.data = self.s.recv(buffer_size)
				if len(self.data) == 0:
					self.on_close()
				else:
					self.on_recv()

	def on_accept(self):
		if self.player1 == "":

			clientsock, clientaddr = self.server.accept()
			Logger.warning(clientaddr[0] + ":" + str(clientaddr[1]) + " has connected as Player 1")
			clients[clientaddr[1]] = {}
			self.input_list.append(clientsock)
			self.player1 = clientaddr[1]
			self.to_send[0]['1'] = [0, 0, 0, 0, 0, 0, 0, 0]


		elif self.player2 == "":
			clientsock, clientaddr = self.server.accept()
			Logger.warning(clientaddr[0] + ":" + str(clientaddr[1]) + " has connected as Player 2")
			clients[clientaddr[1]] = {}
			self.input_list.append(clientsock)
			self.player2 = clientaddr[1]

			self.to_send[1]['1'] = [0, 0, 0, 0, 0, 0, 0, 0]

		else:
			Logger.warning("An other person want to go in our private room !!")

	def on_close(self):
		clientaddr = self.s.getpeername()
		Logger.warning(
			"Player#" + str(clientaddr[1]) + " (" + clientaddr[0] + ":" + str(clientaddr[1]) + ") has disconnected")

		_id = self.s.getpeername()[1]

		# Send disconnect -> 2
		self.disconnection(_id)

		del (clients[clientaddr[1]])
		self.input_list.remove(self.s)

	def on_recv(self):
		# Receive data
		_id = self.s.getpeername()[1]
		try:
			clients[_id] = simplejson.loads(self.data)
		except simplejson.errors.JSONDecodeError:
			Logger.error("JSON tronqué reçu")
		Logger.rec(clients[_id])

		# Create the answer
		if self.gameBegin:
			# State of players
			if '0' in clients[_id]:
				if _id == self.player1:
					Logger.send(self.to_send[0])
				else:
					Logger.send(self.to_send[1])
			# information by player
			if '1' in clients[_id]:
				# inputs
				if '0' in  clients[_id]['1']:
					if _id == self.player1:
						self.to_send[1]['1'] = clients[_id]['1']['0']
						self.sendTo(self.player2)
					else:
						self.to_send[0]['1'] = clients[_id]['1']['0']
						self.sendTo(self.player1)

				if '1' in clients[_id]['1'] :
					pass

		else:
			if '0' in clients[_id]:
				# Connection
				if clients[_id]['0'] == 0:
					if _id == self.player1 :
						self.player1Client = self.s
					elif _id == self.player2:
						self.player2Client = self.s
				# Player attribution
				elif clients[_id]['0'] == 1:
					if _id == self.player1:
						self.to_send[0]['3'] = 0
						self.sendTo(self.player1)
					elif _id == self.player2:
						self.to_send[1]['3'] = 1
						self.sendTo(self.player2)
				# Wait to server play
				elif clients[_id]['0'] == 2:
					# If both players are ok, send play -> 0
					if _id == self.player1:
						self.player1_ok = True
						if self.player2_ok:

							self.to_send[0]['0'] = 0
							self.to_send[1]['0'] = 0
							del self.to_send[0]['3']
							del self.to_send[1]['3']
							self.gameBegin = True
							self.sendToEveryone()
					elif _id == self.player2:
						self.player2_ok = True
						if self.player1_ok:
							self.to_send[0]['0'] = 0
							self.to_send[1]['0'] = 0
							del self.to_send[0]['3']
							del self.to_send[1]['3']
							self.gameBegin = True
							self.sendToEveryone()

	def sendToEveryone(self):
		if self.player1Client != None:
			self.sendTo(self.player1)
		if self.player2Client != None:
			self.sendTo(self.player2)

	def sendTo(self, id):
		if id == "":
			return
		if id == self.player1:
			try:
				self.player1Client.send(bytes(simplejson.dumps(self.to_send[0]), 'utf-8'))
			except ConnectionAbortedError:
				self.disconnection(id)

		elif id == self.player2:
			try:
				self.player2Client.send(bytes(simplejson.dumps(self.to_send[1]), 'utf-8'))
			except ConnectionAbortedError:
				self.disconnection(id)

	def disconnection(self, id):
		if id == self.player1 :
			self.reset(0)
			if self.player2 != "":
				self.to_send[1]['0'] = 2
				self.sendTo(self.player2)
		elif id == self.player2:
			self.reset(1)
			if self.player1 != "":
				self.to_send[0]['0'] = 2
				self.sendTo(self.player1)

	def reset(self, player):
		if player == 0:
			self.player1 = ""
			self.player1Client = None
			self.player1_ok = False
			self.gameBegin = False
		else:
			self.player2 = ""
			self.player2Client = None
			self.player2_ok = False
			self.gameBegin = False

try:
	while do_reset:
		server = CdaServer('0.0.0.0', 34141)

		t = Thread(target=server.main_loop)
		t.daemon = True
		t.start()
		time.sleep(0.2)
		is_running = True

		while is_running:
			line = input("")
			tokens = line.split()
			cmd = tokens[0].lower()
			args = tokens[1:]
			if hasattr(CdaServer, 'do_' + cmd):
				getattr(CdaServer, 'do_' + cmd)(*args)
			else:
				Logger.error("Unknown command !")

		do_reset = False
		if reset:
			do_reset = True
			reset = False

except KeyboardInterrupt:
	Logger.bold(
		"\n\nThe server has been shut down with Ctrl+C. Prefer typing the 'stop' command to close it cleanly.")
sys.exit(1)
