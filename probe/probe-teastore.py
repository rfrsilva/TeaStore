import ast
import sys
import json
import time
from datetime import datetime
import requests
from tmalibrary.probes import *
import os

def create_message(avgrt,count):
    # the timestamp is the same for all metrics from this stat variable (Python is not compatible with nanoseconds,
    #  so [:-4] -> microseconds)

    # message to sent to the server API
    # follow the json schema
    # sentTime = current time? Or the same timestamp from the metrics?
    # need to change the probeId, resourceId and messageId

    message = Message(probeId=9, resourceId=15, messageId=0, sentTime=int(time.time()), data=None)


    # Response Time
    # append measurement data to message
    dt = Data(type="measurement", descriptionId=29, observations=None)


    obs = Observation(time=int(time.time()), value=avgrt)
    dt.add_observation(observation=obs)

    # append data to message
    message.add_data(data=dt)

    # Throughput
    # append event data to message
    dt = Data(type="measurement", descriptionId=30, observations=None)
    obs = Observation(time=int(time.time()), value=count)
    dt.add_observation(observation=obs)

    # append data to message
    message.add_data(data=dt)
    # return message formatted in json
    return json.dumps(message.reprJSON(), cls=ComplexEncoder)

if __name__ == '__main__':
    # server url as parameter
    url = "https://192.168.122.155:32025/monitor"
    communication = Communication(url)

    # Open file
    fo = open("mylogfile.log", "r")
    fo.seek(-1, os.SEEK_END)

    #Ignore first line
    buffer = fo.readline()
    while len(buffer) != 0 or buffer[-1] != '\n':
    	buffer = fo.readline()
    
    while 1:
    	line = None
        buffer = fo.readline()
        while len(buffer) != 0 or buffer[-1] != '\n':
        	line = line + buffer

        line = [x.strip() for x in line.split(',')]
        print line
        temp = line[0]
        count = 0
        responsetime = 0

        while temp == line[0]:
            responsetime = responsetime + int(line[1])
            count = count + 1
            buffer = fo.readline()
            line = None
            while len(buffer) != 0 or buffer[-1] != '\n':
            	line = line + buffer
            line = [x.strip() for x in line.split(',')]

        avgrt = responsetime/count
        temp = line[0]

        message_formated = create_message(avgrt,count)
        response = communication.send_message(message_formated)
        print (response.text)