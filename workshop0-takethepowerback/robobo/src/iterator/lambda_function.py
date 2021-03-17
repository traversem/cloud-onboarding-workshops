import uuid

def lambda_handler(event, context):
    input = event
    iter = event['count']
    iterator = []
    while iter > 0:
        input['uid'] = str(uuid.uuid4())
        iterator.append(input)
        iter -= 1
    print(iterator)
    return iterator
