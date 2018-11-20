import logging
import azure.functions as func
import platform
import sys
import time
import timeit
from datetime import datetime
import json
from decimal import Decimal, getcontext
#from azure.storage.queue import QueueService

class DocumentData(): pass

def main(msg: func.QueueMessage):
    startTime = datetime.utcnow()
    logging.info('Python QUEUE trigger function processed a request.')
    data = DocumentData()
    data.type = "queue"
    data.messageId = msg.id
    data.queueInsertionTime = f'{msg.insertion_time:%Y-%m-%d %H:%M:%S.%f%z}'
    data.msgInsertionTime = msg.get_body().decode('utf-8')

    processMessage(data, startTime)

    messageInsertionTime = datetime.strptime(data.msgInsertionTime, '%Y-%m-%d %H:%M:%S')
    data.delayInStartProcessingFromInserted = (startTime - messageInsertionTime).total_seconds()

    jsonData = json.dumps(data.__dict__)
    logging.info(jsonData)
    
def doMath():
    getcontext().prec=100

    for x in range(10000):
        result = sum(1/Decimal(16)**k * (Decimal(4)/(8*k+1) - Decimal(2)/(8*k+4) - Decimal(1)/(8*k+5) - Decimal(1)/(8*k+6)) for k in range(100))
        if x % 2000 == 0:
            logging.info(f"x is {x}")

    return str(result)

def processMessage(data: DocumentData, startTime: datetime):
    startTime = datetime.utcnow()
    result = doMath()
    result = 0

    args = sys.argv
   
    data.start = f'{startTime:%Y-%m-%d %H:%M:%S.%f%z}' 
    data.host = args[2]
    data.port = args[4]
    data.worker = args[6]
    data.request = args[8]
    data.plataform = sys.platform
    data.node = platform.node()
    data.result = result
    data.version = "12" # Identifyier to filter logs

    stopTime = datetime.utcnow()
    
    # Calculating queue size
    # queue_service = QueueService(account_name='funcpyqueue2storage', account_key='3oWbigAq2HDjcwXRkftTC8zm++rz7ToB6A0Ng9FwTN1e4tFS/lWIL4zF9cfE9UPvOO/j++vkpj44329W4nRNhA==')
    # metadata = queue_service.get_queue_metadata('fibonaccicalculatorqueue')
    # data.queuedMessages = metadata.approximate_message_count

    # Calculate times
    messageInsertionTime = datetime.strptime(data.msgInsertionTime, '%Y-%m-%d %H:%M:%S')
    data.stop = f'{stopTime:%Y-%m-%d %H:%M:%S.%f%z}'
    data.durationSeconds = (stopTime-startTime).total_seconds()
    data.delayInStartProcessingFromMessage = (startTime - messageInsertionTime).total_seconds()