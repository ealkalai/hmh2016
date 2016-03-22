import sys
import hashlib
if sys.version_info < (3, 4):
    import sha3
# in: function_name, param_types[], params[]


def sha3_convert(function_name, param_types):
    data = function_name + "("
    param_string = param_types[0]
    for i in range(1, len(param_types)):
        param_string += ","
        param_string += param_types[i]
    data += param_string
    data += ")"

    # Do conversion send first 8 characters [0:8] (+ 0x)
    s = hashlib.sha3_256() # alternative
    s.update(data)
    return s.hexdigest()[0:8]

def convert_offset(offset):
    offset_hex = str(hex(offset))
    offset_hex = offset_hex.replace("0x","")
    offset_hex += "0"
    return offset_hex.rjust(64,"0")

def convert_int(int):
    offset_hex = str(hex(int))
    offset_hex = offset_hex.replace("0x","")
    return offset_hex.rjust(64,"0")

def convert_string(string):
    offset_hex = string.encode("hex")
    offset_hex = offset_hex.replace("0x","")
    return offset_hex.ljust(64,"0")


def create_data(function, param_types, params):
    data = sha3_convert(function, param_types)
    offset = len(params)*2

    for i in range(0, len(params)):
        if param_types[i] != "string":
            data += convert_int(params[i])
        else:
            data += convert_offset(offset)
            offset += 4

    for i in range(0, len(params)):
        if param_types[i] == "string":
            data += convert_int(len(params[i]))
            data += convert_string(params[i])

    data = "0x" + data

    get = "eth_call"
    set = "eth_sendTransaction"

    if function[0:3] == "get":
        use = get
    if function[0:3] == "set":
        use = set

    final = "curl -X POST --data '{\"jsonrpc\": \"2.0\",\"method\": %s , \"params\": [{ \"data\": %s, \"from\": \"0xf76cdecc25fe182017bff058431dd4b3ed6a51e0\", \"to\": \"0xd2a1a8b4a044876c9648126cc20f7b3954ecd365\", \"gas\": \"50000000000\" }], \"id\": 1}' localhost:8101" % (use, data)

    print final

create_data("setDeal", ["string","int"], ["www.ing.nl",100])
