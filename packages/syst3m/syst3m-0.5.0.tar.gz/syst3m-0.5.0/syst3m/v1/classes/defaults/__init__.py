#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.v1.classes.config import *
import platform 

# functions.
def get_argument(id, empty=None):
	match = False
	for i in sys.argv:
		if id == i: match = True
		elif match == True: return i
	return empty
class Defaults(object):
	def __init__(self):

		# variables.
		self.os = platform.system().lower()
		if self.os in ["darwin"]: self.os = "osx"
		self.home = "/home/"
		self.media = "/media/"
		self.group = "root"
		self.user = os.environ.get("USER")
		if self.os in ["osx"]:
			self.home = "/Users/"
			self.media = "/Volumes/"
			self.group = "staff"

		#
	def check_operating_system(self, supported=["osx", "linux"]):
		if self.os in ["osx"] and self.os in supported: return "osx"
		elif self.os in ["linux"] and self.os in supported: return "linux"
		else: raise ValueError(f"Unsupported operating system: [{self.os}].")
	def check_alias(self, 
		# the source name.
		alias=None, 
		# the source path.
		executable=None,
	):
		present = "--create-alias" in sys.argv and get_argument("--create-alias") == alias
		base = f"/usr/local/bin"
		if not os.path.exists(base):
			base = f"/usr/bin/"
		path = f"{base}/{alias}"
		if present or not os.path.exists(path):
			#file = f"""package={executable}/\nargs=""\nfor var in "$@" ; do\n   	if [ "$args" == "" ] ; then\n   		args=$var\n   	else\n   		args=$args" "$var\n   	fi\ndone\npython3 $package $args\n"""
			file = f"""#!/usr/bin/env python3\nimport os, sys\npackage="{executable}"\nsys.argv.pop(0)\narguments = sys.argv\ns = ""\nfor i in arguments:\n	if s == "": \n		if " " in i: s = "'"+i+"'"\n		else: s = i\n	else: \n		if " " in i: s += " '"+i+"'"\n		else: s += " "+i\nos.system("python3 "+package+" "+s)"""
			os.system(f"touch {path}")
			os.system(f"chmod +x {path}")
			os.system(f"chown {self.user}:{self.group} {path}")
			try:
				Files.File(path=f"{path}", data=file).save()
			except:
				print(f"Unable to create alias $ {alias}.")
				return None
			os.system(f"chmod +x {path}")
			if '--silent' not in sys.argv:
				print(f'Successfully created alias: {alias}.')
				print(f"Check out the docs for more info $: {alias} -h")
		if present:
			quit()
	def get_source_path(self, path, back=1):
		return Formats.FilePath(path).base(back=back)

# initialized classes.
defaults = Defaults()