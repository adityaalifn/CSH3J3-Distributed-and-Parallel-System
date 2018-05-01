from xmlrpc.server import SimpleXMLRPCServer, SimpleXMLRPCRequestHandler
import socket


class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ("/RPC2",)


def getMasterIpAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))  # If the master have internet connection
    except:
        return "127.0.0.1"  # If the master have no internet connection, so it will return localhost
    ip = s.getsockname()[0]
    s.close()
    return ip


def registerIP(ip_address):
    with open("botnet_list.txt", "a") as file:
        file.write(ip_address+"\n")


def unregisterIP(ip_address):
    ip_list = []
    with open("botnet_list.txt", "r") as file:
        ip_list = file.readlines()
        ip_list = [x.strip() for x in ip_list]
        ip_list.remove(ip_address)

    with open("botnet_list.txt", "w") as file:
        for ip in ip_list:
            file.write(ip+"\n")


if __name__ == '__main__':
    server = SimpleXMLRPCServer(
        (getMasterIpAddress(), 8000), requestHandler=RequestHandler, allow_none=True)
    server.register_introspection_functions()
    server.register_function(registerIP, "register_ip")
    server.register_function(unregisterIP, "unregister_ip")
    server.serve_forever()