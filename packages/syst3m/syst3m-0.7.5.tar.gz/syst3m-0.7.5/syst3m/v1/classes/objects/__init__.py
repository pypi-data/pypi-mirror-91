#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# imports.
from syst3m.v1.classes.config import *

# object.
class Object(object):
	def __init__(self):
		a=1
	# iterate over self keys & variables.
	def items(self):
		return vars(self).items()
	def keys(self):
		return list(vars(self).keys())
	def dict(self):
		dictionary = {}
		for key, value in self.items():
			dictionary[key] = value
		return dictionary
	# assign self variables by dictionary.
	def assign(self, dictionary):
		if not isinstance(dictionary, dict):
			raise TypeError("You can only self assign with a dictionary as parameter.")
		return list(vars(self).keys())
	# support item assignment.
	def __setitem__(self, key, value):
		setattr(self, key, value)
	def __getitem__(self, key):
		return getattr(self, key)
		