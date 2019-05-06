import datetime

class Logger:

	frame = "0"

	@staticmethod
	def setFrame(frame):
		Logger.frame = str(frame)

	@staticmethod
	def log(header, text): print('[' + header + '] ' + '[' + Logger.frame + '] ' + text)

	@staticmethod
	def format(header, text): return '[' + header + '] ' + '[' + Logger.frame + '] ' + text

	@staticmethod
	def info(header, text): print('[' + '\033[96m' + header  + '\033[0m' + '] ' + '[' + Logger.frame + '] ' + text)

	@staticmethod
	def success(header, text): print('[' + '\033[92m' + header  + '\033[0m' + '] ' + '[' + Logger.frame + '] ' + text)

	@staticmethod
	def warning(header, text): print('[' + '\033[9 3m' + header  + '\033[0m' + '] ' + '[' + Logger.frame + '] ' + text)

	@staticmethod
	def error(header, text):
		print('[' + '\033[91m' + header  + '\033[0m' + '] ' + '[' + Logger.frame + '] ' + text)
		logfile = open("error.log", "a+")
		logfile.write(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " - [" + header + "] " + text + "\n")
		logfile.close()

	@staticmethod
	def bold(text): print('[' + Logger.frame + '] ' + '\033[1m' + text + '\033[0m')
