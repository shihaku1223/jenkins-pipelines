#!env python3

from optparse import OptionParser

import sys
import requests
import time
import json

from pathlib import Path
from urllib.parse import urljoin

API_BASE_URL = 'http://10.121.88.122:8000/api/API'

FILE_API = 'file'
PECKER_API = 'pecker'

print(urljoin(API_BASE_URL, FILE_API))

def uploadFile(logPath):

    logFile = open(logPath, 'rb')
    fileAPIUrl = urljoin(API_BASE_URL, FILE_API)

    files = {
     'file': logFile
    }

    data = {
     'remark': 'hello'
    }

    response = requests.post(fileAPIUrl + '/', data=data, files=files)

    logFile.close()

    obj = json.loads(response.text)

    return obj

def analyzeLog(log_id):
    peckerAPIUrl = urljoin(API_BASE_URL, PECKER_API)

    data = {
     'log_id': log_id
    }

    response = requests.post(peckerAPIUrl + '/', data=data)
    obj = json.loads(response.text)

    return obj

def waitPeckerTaskEnd(task_id):
    peckerTaskAPIUrl = urljoin(API_BASE_URL, PECKER_API) + '/{}'.format(task_id)

    retry = True

    while(retry):
        try:
            response = requests.get(peckerTaskAPIUrl)
            print(response.text)
            obj = json.loads(response.text)
            status = obj['status']
            retry = False
        except:
            retry = True

    while(status == 'running'):
        time.sleep(5)
        response = requests.get(peckerTaskAPIUrl)
        obj = json.loads(response.text)
        status = obj['status']
        print(status)


if __name__ == '__main__':
    parser = OptionParser()  

    parser.add_option("-b", "--binary", default = None,
        action = "store", dest = "binary",
        help = "log binary file")

    (options, args) = parser.parse_args()  

    if not options.binary:
        sys.exit(0)

    response = uploadFile(options.binary)
    log_id = response['id']
    print(log_id)

    response = analyzeLog(log_id)
    print(response)

    with open(Path(options.binary).stem, 'w') as f:
        f.write(response['task_id'])

    waitPeckerTaskEnd(response['task_id'])
