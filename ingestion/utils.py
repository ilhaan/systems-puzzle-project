import datetime

def parse_log(msg):
    # Retrieves relevant information from GET request
    decomposed_message = msg.split(" ")
    source = decomposed_message[0]
    status = decomposed_message[-2]
    time = decomposed_message[3][1:]
    day = datetime.datetime.strptime(time, "%d/%b/%Y:%X").date()
    return day, status, source

def is_get_request(msg):
    # Determines is msg is a GET request
    decomposed_message = msg.split(" ")
    return len(decomposed_message) >= 6 and decomposed_message[5] == "\"GET"
