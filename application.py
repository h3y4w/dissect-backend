import multiprocessing
import requests
from functools import partial
import os
import time
from queuehandler import DissectQueue

def checkQueues():
    DQ = DissectQueue()
    DQ.connectToQueues()
    while True:
        DQ.checkUploadQueue()


p = multiprocessing.Process(target=checkQueues)
p.start()
