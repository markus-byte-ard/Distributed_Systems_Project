###################################################################################################################################################################
# CT30A3401 Distributed Systems
# Author: Markus Taulu
# Date: 21.04.2023
# Sources: 
#
# client.py
###################################################################################################################################################################

import xmlrpc.client
import sys

## microservice 1 (functions print all, print topic, add topic)
def microservice_notes():
    ## Initialize connection to the server
    s = xmlrpc.client.ServerProxy('http://localhost:8000')
    loop = 1

    while (loop == 1):
        ## Interface
        print("This is the notes service!")
        print("Select Option:")
        print("1: Print all notes")
        print("2: Search topic from notes")
        print("3: Add topic")
        print("4: Exit")
        selectInput = input('\nEnter option: ')

        ## Check input
        ## Calls 
        if (selectInput == "1"):
            ## Calls the printall function from microservice 1
            try:
                result = s.printall()
                if (result == ""):
                    print("No notes were found!")
                else:
                    print(result)

            ## No connection for example not running server.py
            except ConnectionRefusedError as err1:
                sys.exit("Connection error")
            
            ## Built in xmlrpc fault errors
            except xmlrpc.client.Fault as err2:
                print("A fault occurred")
                print("Fault code: %d" % err2.faultCode)
                print("Fault string: %s" % err2.faultString)

        ## Calls the print function from microservice 1
        elif (selectInput == "2"):
            topicInput = input('\nEnter topic to search: ')
            print()

            ## Call print function
            try:
                result = s.print(topicInput)
                if (result == ""):
                    print("Topic was not found!")
                else:
                    print(result)

            ## No connection for example not running server.py
            except ConnectionRefusedError as err1:
                sys.exit("Connection error")
            
            ## Built in xmlrpc fault errors
            except xmlrpc.client.Fault as err2:
                print("A fault occurred")
                print("Fault code: %d" % err2.faultCode)
                print("Fault string: %s" % err2.faultString)

        ## Calls the add function from microservice 1
        elif (selectInput == "3"):
            ## Gather inputs
            titleInput = input("\nEnter title: ")
            noteInput = input("Enter note: ")
            textInput = input("Enter text: ")

            ## Call add function
            try:
                result = s.add(titleInput, noteInput, textInput)
                
                if (result == "Failure"):
                    print("Topic was not added succesfully!\n")
                else:
                    print("Topic was added succesfully!\n")
            
            ## No connection for example not running server.py
            except ConnectionRefusedError as err1:
                sys.exit("Connection error")
            
            ## Built in xmlrpc fault errors
            except xmlrpc.client.Fault as err2:
                print("A fault occurred")
                print("Fault code: %d" % err2.faultCode)
                print("Fault string: %s" % err2.faultString)
        
        ## Exit program
        elif (selectInput == "4"):
            print("\nExiting service\n")
            loop = 0
        
        ## Invalid input
        else:
            print("Input suitable option\n")

## Calls microservice 2 (functions add, subtract, multiply, divide, power to)
def microservice_calculator():
    s = xmlrpc.client.ServerProxy('http://localhost:8001')
    loop = 1

    while (loop == 1):
        ## Interface
        print("This is the calculator service!")
        print("Select Operation:")
        print("1: Add")
        print("2: Subtract")
        print("3: Multiply")
        print("4: Divide")
        print("5: Power to")
        print("6: Quit")
        selectInput = input('\nEnter option: ')
        print()

        ## If input is 6 or invalid no need to ask for input
        if selectInput in ("1", "2", "3", "4", "5"):
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
            except ValueError:
                print("Invalid input. Please enter a number.\n")
                continue

            ## Calls the add function from microservice 2
            if (selectInput == '1'):
                try:
                    print("Result: %f \n" % s.add(num1, num2))
                except xmlrpc.client.Fault as err:
                    print("A fault occurred")
                    print("Fault code: %d" % err.faultCode)
                    print("Fault string: %s" % err.faultString)

            ## Calls the subtract function from microservice 2
            elif (selectInput == '2'):
                try:
                    print("Result: %f \n" % s.divide(num1, num2))
                except xmlrpc.client.Fault as err:
                    print("A fault occurred")
                    print("Fault code: %d" % err.faultCode)
                    print("Fault string: %s" % err.faultString)

            ## Calls the multiply function from microservice 2
            elif (selectInput == '3'):
                try:
                    print("Result: %f \n" % s.multiply(num1, num2))
                except xmlrpc.client.Fault as err:
                    print("A fault occurred")
                    print("Fault code: %d" % err.faultCode)
                    print("Fault string: %s" % err.faultString)

            ## Calls the divide function from microservice 2
            elif (selectInput == '4'):
                try:
                    print("Result: %f \n" % s.divide(num1, num2))
                except xmlrpc.client.Fault as err:
                    print("A fault occurred")
                    print("Fault code: %d" % err.faultCode)
                    print("Fault string: %s" % err.faultString)

            ## Calls the power to function from microservice 2
            elif (selectInput == '5'):
                try:
                    print("Result: %f \n" % s.power(num1, num2))
                except xmlrpc.client.Fault as err:
                    print("A fault occurred")
                    print("Fault code: %d" % err.faultCode)
                    print("Fault string: %s" % err.faultString)

        ## Quits the service    
        elif (selectInput == "6"):
            print("Quitting service\n")
            loop = 0
            break
        else:
            print("Input suitable option\n")

## Calls microservice 3 (functions current weather and current air pollution 60 times every minute for free)
## Other free OpenWeatherMap API features like forecast I wasn't sure if they ment 
## that new data is coming every 3 hours or you can call it every 3 hours so I didn't try it           
def microservice_weather():
    s = xmlrpc.client.ServerProxy('http://localhost:8002')
    loop = 1

    while (loop == 1):
        ## Interface
        print("This is the weather service!")
        print("Select Option:")
        print("1: Current weather")
        print("2: Pollution")
        print("3: Quit")
        selectInput = input('\nEnter option: ')
        if selectInput in ("1", "2"):
            location = input('\nEnter city name: ')

            ## Calls the current weather function from microservice_1
            if (selectInput == '1'):
                try:
                    print(f"\n{s.weather(location)}\n")
                except xmlrpc.client.Fault as err:
                    print("A fault occurred")
                    print("Fault code: %d" % err.faultCode)
                    print("Fault string: %s" % err.faultString)

            ## Calls the current air pollution function from microservice_1
            elif (selectInput == '2'):
                try:
                    print(f"\n{s.pollution(location)}\n")
                except xmlrpc.client.Fault as err:
                    print("A fault occurred")
                    print("Fault code: %d" % err.faultCode)
                    print("Fault string: %s" % err.faultString)

        ## Exit service
        elif (selectInput == "3"):
            print("Quitting service\n")
            loop = 0
            break
        else:
            print("Input suitable option\n")

def main_loop():
    ## While loop when the loop = 1
    loop = 1
    while (loop == 1):
        ## Interface
            print("Select service:")
            print("1: Topics")
            print("2: Calculator")
            print("3: Weather")
            print("4: Quit")
            selectInput = input('\nEnter option: ')
            print()

            ## Check input
            ## Search topic
            ## Note service
            if (selectInput == "1"):
                microservice_notes()

            ## Calculator service
            elif (selectInput == "2"):
                microservice_calculator()         

            ## Weather service
            elif (selectInput == "3"):
                microservice_weather()

            ## Exit program
            elif (selectInput == "4"):
                print("Exiting program")
                loop = 0

            else:
                print("Input suitable option")

main_loop()