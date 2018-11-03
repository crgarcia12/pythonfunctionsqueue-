import logging

import azure.functions as func


def main(msg: func.QueueMessage) -> func.Document:
    logging.info('Python queue trigger function processed a queue item: %s', msg.get_body().decode('utf-8'))

    processeditem = '{"id":"' + msg.get_body().decode('utf-8') + '"}'
    doc = func.Document.from_json(processeditem)

    return doc
