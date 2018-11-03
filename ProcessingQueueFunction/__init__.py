import logging
import azure.functions as func
import timeit
import json
from datetime import datetime

def fibonacci(n):
    a,b = 1,1
    for i in range(n-1):
        a,b = b,a+b
    return a 

class DocumentData(): pass

def main(msg: func.QueueMessage) -> func.Document:
    start = datetime.utcnow()

    requestedValue = int(msg.get_body().decode('utf-8'))
    logging.info('Python queue trigger function processed a queue item: %s', msg.get_body().decode('utf-8'))
    
    # Create some CPU load
    fibo =  fibonacci(requestedValue) 

    stop = datetime.utcnow()

    data = DocumentData()
    data.id = msg.id
    data.insertionTime = f'{msg.insertion_time:%Y-%m-%d %H:%M:%S.%f%z}' 
    data.start = f'{start:%Y-%m-%d %H:%M:%S.%f%z}' 
    data.stop = f'{stop:%Y-%m-%d %H:%M:%S.%f%z}'
    data.requestedValue = requestedValue
    data.fibonacci = fibo
    data.durationSeconds = (stop-start).total_seconds()

    # Create the document in Cosmos DB
    # processeditem = '{"id":"' + msg.get_body().decode('utf-8') + '","fiboNumber":"' + fibo + '"}'
    jsonData = json.dumps(data.__dict__)
    doc = func.Document.from_json(jsonData)
    
    logging.info(jsonData)
    logging.info(doc)

    return doc
