import logging
import azure.functions as func
import platform
import sys
import time
import timeit
from datetime import datetime
import json
from decimal import Decimal, getcontext

class DocumentData(): pass

def doMath():
    getcontext().prec=100

    for x in range(10000):
        result = sum(1/Decimal(16)**k * (Decimal(4)/(8*k+1) - Decimal(2)/(8*k+4) - Decimal(1)/(8*k+5) - Decimal(1)/(8*k+6)) for k in range(100))
        if x % 2000 == 0:
            logging.info(f"x is {x}")

    return str(result)

def main(req: func.HttpRequest, context: func.Context) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    try:
        startTime = datetime.utcnow()
        result = doMath()
        stopTime = datetime.utcnow()

        args = sys.argv

        data = DocumentData()
        data.type = "http"
        data.start = f'{startTime:%Y-%m-%d %H:%M:%S.%f%z}' 
        data.stop = f'{stopTime:%Y-%m-%d %H:%M:%S.%f%z}'
        data.durationSeconds = (stopTime-startTime).total_seconds()
        data.host = args[2]
        data.port = args[4]
        data.worker = args[6]
        data.request = args[8]
        data.plataform = sys.platform
        data.node = platform.node()
        data.result = result
        data.version = "9.HTTP" # Identifyier to filter logs

        jsonData = json.dumps(data.__dict__)
        logging.info(jsonData)
        return func.HttpResponse(jsonData)
    except Exception as e:
        return func.HttpResponse( f"<p>Error: {str(e)}</p>")
