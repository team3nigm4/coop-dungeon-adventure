# Class to print colored logs and store the errors in a file

import datetime

class Logger:

	frame = "0"

	# Method called every loop turn to update the frame number in the logs
	@staticmethod
	def setFrame(frame):
		Logger.frame = str(frame)

	# Method to print a log with a header
	@staticmethod
	def log(header, text): print('[' + header + '] ' + '[' + Logger.frame + '] ' + text)

	# Method to return a log string with a header
	@staticmethod
	def format(header, text): return '[' + header + '] ' + '[' + Logger.frame + '] ' + text

	# Method to print a log in blue (for informations messages)
	@staticmethod
	def info(header, text): print('[' + '\033[96m' + header  + '\033[0m' + '] ' + '[' + Logger.frame + '] ' + text)

	# Method to print a log in green (for success messages)
	@staticmethod
	def success(header, text): print('[' + '\033[92m' + header  + '\033[0m' + '] ' + '[' + Logger.frame + '] ' + text)

	# Method to print a log in orange (for warning messages)
	@staticmethod
	def warning(header, text): print('[' + '\033[9 3m' + header  + '\033[0m' + '] ' + '[' + Logger.frame + '] ' + text)

	# Method to print a log in red (for error messages) - also stored in "error.log" file
	@staticmethod
	def error(header, text):
		print('[' + '\033[91m' + header  + '\033[0m' + '] ' + '[' + Logger.frame + '] ' + text)
		logfile = open("error.log", "a+")
		logfile.write(datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S") + " - [" + header + "] " + text + "\n")
		logfile.close()

	# Method to print a log in bold
	@staticmethod
	def bold(text): print('[' + Logger.frame + '] ' + '\033[1m' + text + '\033[0m')
