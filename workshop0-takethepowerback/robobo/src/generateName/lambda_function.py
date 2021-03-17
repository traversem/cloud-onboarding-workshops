import random
import string

def define_os(os):
    if os == 'linux':
        return 'l'
    elif os == 'windows':
        return 'w'
    else:
        return 'x'

def generate_random_string(chartype, length):
    if chartype == 'letter':
        response = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    elif chartype == 'number':
        response = ''.join(random.choice(string.digits) for i in range(length))
    return response

def lambda_handler(event, context):
    print(event)
    section0 = 's'
    section1 = define_os(event['os'])
    section2 = generate_random_string('number', 2)
    section3 = generate_random_string('letter', 1)
    section4 = generate_random_string('number', 3)
    response = ''.join([section0, section1, section2, section3, section4])
    return response
