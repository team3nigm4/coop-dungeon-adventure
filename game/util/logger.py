class Logger:

	@staticmethod
	def log(header, text): print('[' + header + '] ' + text)

	@staticmethod
	def format(header, text): return '[' + header + '] ' + text

	@staticmethod
	def info(header, text): print('[' + '\033[96m' + header  + '\033[0m' + '] ' + text)

	@staticmethod
	def success(header, text): print('[' + '\033[92m' + header  + '\033[0m' + '] ' + text)

	@staticmethod
	def warning(header, text): print('[' + '\033[33m' + header  + '\033[0m' + '] ' + text)

	@staticmethod
	def error(header, text): print('[' + '\033[91m' + header  + '\033[0m' + '] ' + text)

	@staticmethod
	def bold(text): print('\033[1m' + text + '\033[0m')