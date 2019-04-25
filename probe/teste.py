#!/usr/bin/python

# Open a file

import os


fo = open("mylogfile3.log", "r")

fo.seek(-1, os.SEEK_END)

# Ignore first line read
buffer = fo.readline()
print buffer[-1]
buffer = fo.readline()
if len(buffer) == 0 or buffer[-1] == '\n':
  processMessage()

#while buffer[-1] != '\n':
#buffer = fo.readline()
#print len(buffer)

#buffer = fo.readline()
#print buffer
#print fo.tell()
