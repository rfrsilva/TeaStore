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
    file_obj = open("mylogfile.log", "r")
    file_obj.seek(0, os.SEEK_END) # End-of-file


    # Experiments of 20 minutes
    stoptime = datetime.datetime.now() + datetime.timedelta(minutes=20)
    
    while datetime.datetime.now() < stoptime:
    	line = file_obj.readline()

        if len(line) != 0:

            if line[-1] != '\n':
                time.sleep(0.1) # Sleep briefly
                continue

            line = [x.strip() for x in line.split(',')]

            if len(line) > 2:

                temp = line[0]
                count = 0
                responsetime = 0
                log = line

                while log[0] <= temp+1000:

                    responsetime = responsetime + int(log[1])
                    count = count + 1
                    line = file_obj.readline()

                    if len(line) != 0:

                        if line[-1] != '\n':
                            time.sleep(0.1) # Sleep briefly
                            continue
                        line = [x.strip() for x in line.split(',')]

                        if len(line) > 2:
                            log=line

                avgrt = responsetime/count
                temp = log[0]

                message_formated = create_message(avgrt,count)
                response = communication.send_message(message_formated)
                print (response.text)