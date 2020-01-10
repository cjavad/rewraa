import json # import json for json.dumps

"""
Socket tools. here is some functions that makes sending
and reciving data via sockets easier.
"""

# write that can select correct data type and send it
def write(data, sock):
    # takes data and socket as args
    if type(data) == bytes:
        # if it's just binary send it as it is
        sock.sendall(data)

    elif type(data) == str:
        # if it's a string send it ad utf8
        sock.sendall(data.encode())

    elif type(data) == dict:
        # if it's a dict convert it to a json 
        # string an send as utf8
        sock.sendall(json.dumps(data).encode())
    else:
        # else just convert to a string
        # and send it as utf8
        sock.sendall(str(data).encode())

# read for sock
def read(sock):
    # read the first 1024 bytes
    data = sock.recv(1024)
    # and add them to out
    out = data
    # if there is more data
    while not data:
        # keep reading
        data = sock.recv(1024)
        # and adding
        out += data
    # when you're done
    # return out
    return out
