import time

class Run(object):
    def __init__(self):
        self.stopping = False

    def description(self):
        return [
            "Docker base image"
        ]

    def config(self):
        print ("config")

    def run(self):
        while not self.stopping:
            print ("Base image running")
            time.sleep(1)
        return 0

    def stop(self):
        self.stopping = True
