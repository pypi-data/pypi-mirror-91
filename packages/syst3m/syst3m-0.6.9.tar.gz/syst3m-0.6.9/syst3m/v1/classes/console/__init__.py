
# imports
from syst3m.v1.classes.config import *
from syst3m.v1.classes.color import color

# the loader object class.
class Loader(threading.Thread):
	def __init__(self, message, autostart=True):
		threading.Thread.__init__(self)
		self.message = self.__clean_message__(message)
		self.last_message = str(self.message)
		if autostart: 
			try:
				self.start()
			except KeyboardInterrupt:
				self.stop(success=False)
	def run(self):
		self.running = True
		self.released = True
		while self.running:
			if not self.released:
				time.sleep(1)
			else:
				for i in ["|", "/", "-", "\\"]:
					if self.message != self.last_message:
						print(self.__empty_message__(length=len(f"{self.message} ...   ")), end="\r")
						self.message = self.__clean_message__(self.message)
					print(f"{self.message} ... {i}", end="\r")
					self.last_message = self.message
					if not self.running: break
					time.sleep(0.33)
		self.running = "stopped"
	def stop(self, message=None, success=True, response=None, quiet=False):
		if response == None:
			if message == None: message = self.message
		else:
			if response["error"] == None:
				message = response["message"]
			else:
				success = False
				message = "Error: "+response["error"]
		self.running = False
		for i in range(120):
			if self.running == "stopped": break
			time.sleep(0.5)
		if self.running != "stopped": raise ValueError(f"Unable to stop loader [{self.message}].")
		if not quiet:
			print(self.__empty_message__(length=len(f"{self.last_message} ...   ")), end="\r")
			if success:
				print(f"{message} ... done")
			else:
				print(f"{message} ... {color.red}failed{color.end}")
	def mark(self, old_message=None, new_message=None, success=True, response=None):
		if response != None:
			if response["error"] == None:
				success = True
			else:
				success = False
		if old_message == None: old_message = self.message
		print(self.__empty_message__(length=len(f"{self.last_message} ...   ")), end="\r")
		if success:
			print(f"{old_message} ... done")
		else:
			print(f"{old_message} ... {color.red}failed{color.end}")
		if new_message != None: self.message = new_message
	def hold(self):
		self.released = False
		time.sleep(0.33)
	def release(self):
		self.released = True
		time.sleep(0.33)
	# system functions.
	def __clean_message__(self, message):
		if message[-len(" ..."):] == " ...": message = message[:-4]
		if message[-len("."):] == ".": message = message[:-1]
		if message[0].upper() != message[0]: message = message[1:]+message[0].upper()+message[1:]
		return message
	def __empty_message__(self, length=len("hello world")):
		s = ""
		for i in range(length): s += " "
		return s

# the loader object class.
class ProgressLoader(threading.Thread):
	def __init__(self, message, index=0, max=10):
		threading.Thread.__init__(self)
		self.message = message
		if self.message[-len(" ..."):] == " ...": self.message = self.message[:-4]
		if self.message[-len("."):] == ".": self.message = self.message[:-1]
		if self.message[0].upper() != self.message[0]: self.message = self.message[1:]+self.message[0].upper()+self.message[1:]
		self.index = index
		self.max = max
		self.progress = None
	def next(self, count=1, decimals=2):
		self.index += count
		p = round((self.index / self.max) * 100, decimals)
		if p != self.progress:
			self.progress = p
			print(f"{self.message} ... {self.progress}", end="\r")
	def stop(self, message=None, success=True, response=None):
		if response == None:
			if message == None: message = self.message
		else:
			if response["error"] == None:
				message = response["message"]
			else:
				success = False
				message = "Error: "+response["error"]
		if success:
			print(f"{message} ... done")
		else:
			print(f"{message} ... {color.red}failed{color.end}")
