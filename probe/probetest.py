import os
import time
import datetime
"""
Based on the amazing guide
http://www.dabeaz.com/generators/Generators.pdf
Works as tail -f

:param file_obj:
:return
"""
file_obj = open("mylogfile.log", "r")
file_obj.seek(0, os.SEEK_END) # End-of-file
count = 0
stoptime = datetime.datetime.now() + datetime.timedelta(minutes=20)
while datetime.datetime.now() < stoptime:
    line = file_obj.readline()
    if len(line) != 0:
        if line[-1] != '\n':
            time.sleep(0.1) # Sleep briefly
            continue
        print "\n"
        print "Linha:" + line
        line = [x.strip() for x in line.split(',')]
        print "Tamanho da linha:" + str(len(line))
        if len(line) > 2:
            print line[1]
