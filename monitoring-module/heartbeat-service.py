# app.py
from flask import Flask
import json
from datetime import datetime, timedelta
from threading import Thread
import os
from time import sleep

with open('hosts.json', 'r') as f:
    hosts = json.load(f)

results = {}
lastPulse = {}

for host in hosts:
    results[host["hostId"]] = 1
    lastPulse[host["hostId"]] = None

# Failure if no pulse for 1.2 minutes


def updateResults():
    while True:
        for host in hosts:
            hostId = host["hostId"]
            curTime = datetime.now()
            if (lastPulse[hostId] != None and curTime - lastPulse[hostId] < timedelta(minutes=1.2)):
                results[hostId] = 0
            else:
                results[hostId] = 1

        print("Result set: ")
        print(results)
        now = datetime.now()
        print(now)
        failure = False
        for host in hosts:
            if (results[host["hostId"]] == 1):
                failure = True
                break
        if (failure):
            results_file = open('results.csv', 'a')
            for host in hosts:
                host_status = results[host['hostId']]
                results_file.write(f"{host_status}, ")
            results_file.write(f"{now}\n")
            results_file.close()
        sleep(10)
        os.system('clear')


t_UpdateResults = Thread(target=updateResults)
t_UpdateResults.start()


app = Flask(__name__)


@app.get("/notify/<vm_id>")
def get_notify(vm_id):
    print("Notify message from: ", vm_id)
    lastPulse[vm_id] = datetime.now()
    return f"OK-{vm_id}"
