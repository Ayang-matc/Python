#Adam Yang

#Unit 10 Lab: Asking the user for a interface and IP Address that they will like to change in the router (dist-rtr01).

import requests
import json
import urllib3
urllib3.disable_warnings()

#The following function is getting the API call from the IOS XE Router (10.10.20.175). It requires the router's management IP address and returns the json interface (ip and subnetmask address) using the YANG format.
def getInts(mgmtIP):
    
    url = f"https://{mgmtIP}:443/restconf/data/ietf-interfaces:interfaces"
    username = 'cisco'
    password = 'cisco'
    payload={}
    headers = {
      'Content-Type': 'application/yang-data+json',
      'Accept': 'application/yang-data+json',
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'
    }

    response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=payload)

    #Assigning a variable to the request.
    int_addr = response.json()['ietf-interfaces:interfaces']['interface']
    #Empty list
    ipList = []
    #The following for loop is going through the API call from the router and getting the name, ip, and subnet mask address:
    for port in int_addr:
        #Due to the Loopback interface not having an IP address, it will only take the routers that have the 'type' of 'ethernetCsmacd':
        if port ['type'] == 'iana-if-type:ethernetCsmacd':
        #The for loop will go into the 'ietf-ip:ipv4' values and get the interface of 'ip address' and 'netmask' address.
            for address in port['ietf-ip:ipv4'].values():
                #Lastly, it will append the correct values ('name', 'ip', and 'netmask'):
                ipList.append({"name" : port['name'], "ip" : address[0]['ip'], "netmask" : address[0]['netmask']})
    #Returns the new list:          
    return ipList
    
#The following function is getting the API call from the IOS XE Router (10.10.20.175). It requires the router's management IP address and returns the json of the interface state ('name' and 'phys-address') using the YANG format.
def getIntRestMAC(ipAddr):

    url = "https://" + ipAddr + ":443/restconf/data/interfaces-state"
    username = 'cisco'
    password = 'cisco'
    payload={}
    headers = {
      'Accept': 'application/yang-data+json',
      'Content-Type': 'application/yang-data+json',
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'
    }

    response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=payload)

    #Assigning a variable to the request:
    int_name = response.json()['ietf-interfaces:interfaces-state']['interface']
    #Empty list
    stateList = []

    #The following for loop is going through the the API call from the router and getting the 'name' and 'phys-address'.
    for info in int_name:
        if info ['type'] == 'iana-if-type:ethernetCsmacd':
            #Append the correct values ('name' and 'phys-address')
            stateList.append({"name" : info['name'], "phys-address" : info['phys-address']})
    #Returns the new list:   
    return stateList

#The following function is combining the two interface list together into one list of dictionaries. It will be getting the correct interfaces, name, IP address, and MAC Address. It returns the new list of dictionaries.
def combineIntLists(intStateList, intList):
    #Empty list
    CombinedList = []

    #The following for loop will be going into both list of dictionaries and assigning a variable to each of the values. Then it will append it to the empty list to combine both of them into one listed dictionary. It returns the new combined list of dictionaries.
    #For loop going into the 'intList' and getting the ip, netmask, and name:
    for addr in intList:
        intIP = addr['ip']
        intMask = addr['netmask']

        ipintname = addr["name"]
        #For loop going into the 'intStateList' and getting the name and phys-address.
        for state in intStateList:
            intName = state['name']
            intMAC = state['phys-address']
            #If the 'ipintname' equals to the intName, append the new list:
            if ipintname == intName: 
                #Appending both list of dictionaries into the empty list:
                CombinedList.append({"name" : intName, "phys-address" : intMAC, "ip" : intIP, "netmask" : intMask})
    
    return CombinedList

#The following function is creating the header for the 'printList' function.
def printListHeader():

    print('Int \t\t\t\t IP \t\t Subnet \t\t Physical')
    print('-'*90)

#The following function is printing out the correct output for the table that is being created.
def printList(combinedList):
    newCombinedList = combinedList
    #The header from the function above:
    printListHeader()
    #The for loop is going into the list of dictionaries and printing out the correct format.
    for interface in newCombinedList:
        print (interface['name'] + ' ' * 10 + interface['ip'] + ' ' * 10 + interface['netmask'] + ' ' * 10 + interface['phys-address'])


#The following function is updating the router's (dist-rtr01) interface IP Address that was given from the user. It requires the management IP, interface name, and the user's ip address that was given.
def updateDevInt(ipAddr,interface,intIP):
    url = "https://" + ipAddr + ":443/restconf/data/ietf-interfaces:interfaces/interface=" + interface
    username = 'cisco'
    password = 'cisco'
    payload={"ietf-interfaces:interface": {
                        "name": interface,
                        "description": "Configured by RESTCONF",
                        "type": "iana-if-type:ethernetCsmacd",
                        "enabled": "true",
                                         "ietf-ip:ipv4": {
                                                                "address": [{
                                                                    "ip": intIP,
                                                                    "netmask": "255.255.255.252"
                                                                    
                                                                            }   ]
                                                            }
                                            }
             }

    headers = {
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm',
      'Accept': 'application/yang-data+json',
      'Content-Type': 'application/yang-data+json'
    }

    response = requests.request("PUT", url, auth=(username,password),headers=headers, verify = False, data=json.dumps(payload)
    )

#The following function is getting the interface name from the 'combineList'. It returns the port interface name.
def getIntNames(intList):

    interfaces = intList

    int_name = [intf['name'] for intf in interfaces]
    
    return int_name
        
#The following function is going into the list and ensuring that it is a valid interface name from the list (return True). If not, it will return False.
def checkInt(user_int, intList):
    valid_int = False
    
    if user_int in intList:
        valid_int = True
    else:
        print("Invalid interface! (NOTE: The port interface is case-sensitive!)")
    return valid_int


#The following function is checking if the user's IP Address is valid. If not, it will return False.
def checkIP(ip):
    
    ip_list = ip.split(".")
    validIP = True
    if len(ip_list) == 4:
        for valid_ip in ip_list:
            if valid_ip.isnumeric() == True:
                if int(valid_ip) < 0 or int(valid_ip) > 255:
                    validIP = False
            else:
                validIP = False
    else:
        validIP = False
        
    return validIP
    
###MAIN

#The deviceIP will be the management IP address for dist-rtr01:
ipAddr = '10.10.20.175'

#Giving the variables to the getInt function that will get the API call from the dist-rtr01:
intList = getInts(ipAddr)
intStateList = getIntRestMAC(ipAddr)

#Giving the variable to the 'combineIntLists' function which will take both API calls from the function above:
combinedList = combineIntLists(intStateList, intList)

#Print out the correct table output from the 'combinedList':
printList(combinedList)

print(" ")

#while loop
valid_input = False
#The following while loop is asking the user for an interface that they would like to change their IP Address. If the interface is not correctly spelled or invalid, it will ask the user to try again. It will also check if the IP Address is valid, if not, then it will tell the user that the IP is invalid:
while valid_input == False:
    valid_input = True
    user_int = input("What port interface would you like to change their IP Address?: ")
    
    intNames = getIntNames(combinedList)
    valid_user_int = checkInt(user_int, intNames)
    
    valid_interface = False
    #If the user interface is valid, it will ask the user for a new IP address for the interface:  
    if valid_user_int == True:
        while valid_interface == False:
            valid_interface = True
            
            user_ip = input("Type in the new IP Address for your interface: ")
            
            valid_ip = checkIP(user_ip)
            #If the ip and interface are valid, it will change the IP Address and printout the table again to show that it had been changed:
            if valid_ip == True:
                updateDevInt(ipAddr,user_int,user_ip)
                print(" ")
                print("Success! The new IP Address of " + user_ip + " " + "has been added to " + user_int + "!")
                print(" ")
                intList = getInts(ipAddr)
                intStateList = getIntRestMAC(ipAddr)
                combinedList = combineIntLists(intStateList, intList)
                printList(combinedList)

            #Otherwise, it will print that both are invalid:
            else:
                print("Invalid IP Address! The given input of " + user_ip + " cannot be added to " + user_int + "!")
                valid_interface = False
    else:
        valid_input = False

        

