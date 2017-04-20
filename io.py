from sets import Set
import os

class io:

	def __init__(self):
		return

	def read_lines(self, in_file):
		lines = open(in_file, 'r').readlines()
		lines = [line.rstrip('\r\n') for line in lines]
		return lines