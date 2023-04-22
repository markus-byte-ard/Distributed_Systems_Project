###################################################################################################################################################################
# CT30A3401 Distributed Systems
# Author: Markus Taulu
# Date: 21.04.2023
# Sources: https://docs.python.org/3/library/xmlrpc.server.html (basic structure)
#
# microservice_2.py (Calculation service)
###################################################################################################################################################################

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler

## Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

## Create server
with SimpleXMLRPCServer(('localhost', 8001),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    ## Add user inputs and return them
    def adder_function(x, y):
        return x + y
    server.register_function(adder_function, 'add')

    ## Subtract user inputs and return them
    def subtraction_function(x, y):
        return x - y
    server.register_function(subtraction_function, 'subtract')

    ## Multiply user inputs and return them
    def multiplier_function(x, y):
        return x * y
    server.register_function(multiplier_function, 'multiply')

    ## Divide user inputs and return them
    def divider_function(x, y):
        return x / y
    server.register_function(divider_function, 'divide')

    ## Power to the user inputs and return them
    def power_function(x, y):
        return x ** y
    server.register_function(power_function, 'power')

    ## Run the server's main loop
    server.serve_forever()