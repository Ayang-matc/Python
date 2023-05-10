#Adam Yang

#Unit 10 Lab: Asking the user for a interface and IP Address that they will like to change in the router (dist-rtr01).

import requests
import json
import urllib3
urllib3.disable_warnings()

#The function gets API call from the device and returns the interface and IP Address.
def getIntRest(mgmtIP):
    url = f'https://{mgmtIP}/restconf/data/ietf-interfaces:interfaces'
    username = 'cisco'
    password = 'cisco'
    payload = {}
    headers = {'Accept': 'application/yang-data+json', 
               'Content-Type': 'application/yang-data+json',
               'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'}
    
    response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=payload)
    return response.json()

#The function gets API call from the device and returns MAC Address.
def getIntMacRest(mgmtIP):
    url = f"https://{mgmtIP}:443/restconf/data/interfaces-state"
    
    username = 'cisco'
    password = 'cisco'
    payload={}
    headers = {
      'Accept': 'application/yang-data+json',
      'Content-Type': 'application/yang-data+json',
      'Authorization': 'Basic cm9vdDpEX1ZheSFfMTAm'}

    response = requests.request("GET", url, auth = (username,password), verify = False, headers=headers, data=payload)
    return response.json()

#This function takes response from getIntRest and returns a list of interfaces, IP Addresses and subnetmask. append the correct values ('name', 'ip', and 'netmask')
def getIntList(intRest):
    intList = []
    for port in intRest["ietf-interfaces:interfaces"]["interface"]:
        if port ['type'] == 'iana-if-type:ethernetCsmacd':
            for address in port ['ietf-ip:ipv4'].values():
                intList.append({"name" : port['name'], "ip" : address[0]['ip'], "netmask" : address[0]['netmask']})
    
    return intList

#This function takes response from getIntMacRest and returns a list of interfaces and MAC Addresses.
def getIntStateList(intMacRest):
    intStateList = []
    for state in intMacRest["ietf-interfaces:interfaces-state"]["interface"]:
        if state ['type'] == 'iana-if-type:ethernetCsmacd':
            intStateList.append({'name' : state['name'], "phys-address" : state['phys-address']})
    
    return intStateList

#This function combines lists in desired format
def combineIntLists(intStateList, intList):
     for addr in intList:
        intIP = addr['ip']
        intMask = addr['netmask']

        ipintname = addr["name"]
        for state in intStateList:
            intName = state['name']
            intMAC = state['phys-address']
            if intName == ipintname:
                combineList = {"name" : intName, "ip" : intIP, "netmask" : intMask, "mac" : intMAC, 'pysical-address' : intMAC}
                return combineList


#Main function
def main():
   mgmtIP = '10.10.20.175'
   intListResponse = getIntRest(mgmtIP)
   intList = getIntList(intListResponse)
   intStateListResponse = getIntMacRest(mgmtIP)
   intStateList = getIntStateList(intStateListResponse)
   combineIntLists(intStateList, intList)

main()
