###################################################################################################################################################################
# CT30A3401 Distributed Systems
# Author: Markus Taulu
# Date: 21.04.2023
# Sources: https://docs.python.org/3/library/xmlrpc.server.html (basic structure), https://docs.python.org/3/library/xml.etree.elementtree.html (element tree)
#
# microservice_1.py (Note service)
###################################################################################################################################################################

from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import xml.etree.ElementTree as ET
from datetime import datetime
from threading import Lock
import sys

## Create a lock and confirm the existance of the xml file
lock = Lock()
try:
    tree = ET.parse('db.xml')
    root = tree.getroot()
except FileNotFoundError as err:
    sys.exit("Xml file 'db.xml' does not exist")

## Restrict to a particular path.
class RequestHandler(SimpleXMLRPCRequestHandler):
    rpc_paths = ('/RPC2',)

## Create server
with SimpleXMLRPCServer(('localhost', 8000),
                        requestHandler=RequestHandler) as server:
    server.register_introspection_functions()

    ## xml_print takes in Topic as parameter and returns found notes
    def xml_print(param1):
        ## Returning "" results in Topic not found on client side
        result = ""
        
        ## Lock the process to enforce mutex
        with lock:
            ## Find all topics
            for topic in root.findall('topic'):
                ## If topic name = parameter
                name = topic.get('name')

                if(name==param1):
                    i = 0
                    for note in topic.findall('note'):
                        ## Multiple notes are possible, but each note has only one text and timestamp
                        notename = topic.findall('note')
                        text = note.find('text').text.strip()
                        time = note.find('timestamp').text.strip()

                        ## If else so that there are consisten newlines on client side
                        if (i == 0):
                            result = result + "Topic: " + name + "\nNote: " + notename[i].get('name') + "\nText: " + text + "\nTimestamp: " + time + "\n"
                        else:
                            result = result + "\nTopic: " + name + "\nNote: " + notename[i].get('name') + "\nText: " + text + "\nTimestamp: " + time + "\n"
                        i += 1
            

            print(datetime.now().strftime("%d/%m/%Y - %H:%M:%S"))

            return result
    
    server.register_function(xml_print, 'print')

    ## Prints all notes
    def xml_printall():
        ## Returning "" results in Topic not found on client side
        result = ""
        i = 0
        ## Save the first topic name as oldname
        oldname = root.find('topic').get('name')

        ## Lock the process to enforce mutex
        with lock:
            for topic in root.findall('topic'):
                name = topic.get('name')

                ## compare If topic name = parameter if the name is topic is changed reset index to 0
                if (oldname == name):
                    pass
                else:
                    i = 0
                    oldname = name
                
                for note in topic.findall('note'):
                    ## Multiple notes are possible, but each note has only one text and timestamp
                    notename = topic.findall('note')
                    text = note.find('text').text.strip()
                    time = note.find('timestamp').text.strip()

                    result = result + "\nTopic: " + name + "\nNote: " + notename[i].get('name') + "\nText: " + text + "\nTimestamp: " + time + "\n"
                    i += 1
            return result

    server.register_function(xml_printall, 'printall')

    ## Add function takes in Topicname, note and text as parameters
    def xml_add(param1, param2, param3):
        result = "Failure"
        topicName = param1
        note = param2
        text = param3
        ## Creating timestamp in the correct format
        time = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")
        
        ## Lock the process to enforce mutex
        with lock:
            ## Search all topics
            for topic in root.findall('topic'):
                ## Compare if topic already exists
                name = topic.get('name')

                if(name == topicName):
                    newNote = ET.fromstring('<note name="' + note + '"><text>' + text + '</text><timestamp>' + time + '</timestamp></note>')
                    topic.append(newNote)
                    ET.indent(tree, '    ')
                    
                    try:
                        tree.write("db.xml")
                        result = "Success"
                        break
                    except ET.ParseError:
                        result = "Failure"
            
            ## If loop didn't find topic creates a new topic to the end
            if (result == "Failure"):
                newTopic = ET.fromstring('<topic name="'+ topicName + '"><note name="' + note + '"><text>' + text + '</text><timestamp>' + time + '</timestamp></note></topic>')
                root.append(newTopic)
                ET.indent(tree, '    ')

                try:
                    tree.write("db.xml")
                    result = "Success"
                except ET.ParseError:
                    result = "Failure"
                    
            return result
    
    server.register_function(xml_add, 'add')

    ## Run the server's main loop
    server.serve_forever()