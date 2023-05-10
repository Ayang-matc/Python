#Adam Yang, Chee Yeng Thao, and Josh Sainsbury
#5/2/23


#Creating a VLAN 120 that includes OSPF, HSRP, and SVI interface for the switches. Also, changing the IP address (172.31.x.x)for each interface on all devices.

import requests
import json
import urllib3
import os.path
import xmltodict
from ncclient import manager
urllib3.disable_warnings()


#The following function is getting a token/cookie from the request. It requires the url of the API aaaLogin from the switch that wants to be authenticated. It returns the token number.
def getCookie(addr) : #Gets the token
    url = "https://"+ addr + "/api/aaaLogin.json"
    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }
    response = requests.post(url, json=payload, verify = False)
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

#The following function is loading the inventory.json file. It returns the inventory after loading the file
def loadInventory(): #Function used to load the inventory file
    if not os.path.isfile("inventory.json"):#Checks is file exists, if not creates one
        f = open("inventory.json", "x")
        print("-"*60+"\nError: File not found\nCreating file")
        f.close()
    f = open("inventory.json", "r")
    if not f.read(): #Returns an empty dict when the file is empty to stop the program from breaking
        print("Error loading inventory: File seems to be empty")
        return {}
    else:
        f = open("inventory.json", "r")
        inv = json.load(f)#Seems to break if I dont reopen the file after f.read()
        return inv
    
#The following function is creating the VLAN 120 for the NXOS switches:
def createVlan(addr,vlan,vname,cookie): #Creates and names a vlan
    url = "https://"+addr+"/api/mo/sys.json"
    payload = {
                "topSystem": {
                    "children": [
                    {
                        "bdEntity": {
                        "children": [
                            {
                            "l2BD": {
                                "attributes": {
                                "fabEncap": vlan,
                                "name": vname
                                }}}]}}]}}
    headers = {
    'Content-Type': 'text/plain',
    'Cookie': 'APIC-cookie='+cookie
    }
    response = requests.request("POST", url, verify = False, headers=headers, data=json.dumps(payload))

#The following function is creating the VLAN 120 SVI interface.
def createSVI(addr,SVI,SVIaddr,cookie): #Creates an SVI and adds an address
    url = "https://"+addr+"/api/mo/sys.json"
    payload = {
  "topSystem": {
    "children": [
      {
        "ipv4Entity": {
          "children": [
            {
              "ipv4Inst": {
                "children": [
                  {
                    "ipv4Dom": {
                      "attributes": {
                        "name": "default"
                      },
                      "children": [
                        {
                          "ipv4If": {
                            "attributes": {
                              "id": SVI
                            },
                            "children": [
                              {
                                "ipv4Addr": {
                                  "attributes": {
                                    "addr": SVIaddr
        }}}]}}]}}]}}]}},
      {
        "interfaceEntity": {
          "children": [
            {
              "sviIf": {
                "attributes": {
                  "adminSt": "up",
                  "id": SVI
        }}}]}}]}}  
    headers = {
    'Content-Type': 'text/plain',
    'Cookie': 'APIC-cookie='+cookie
    }
    response = requests.request("POST", url, verify = False, headers=headers, data=json.dumps(payload))

#Gets the interfaces from a NXOS device and returns a list of them
def getInterfaces(addr,cookie): #Gets the interfaces from a NXOS device
    url = "https://"+addr+"//api/node/mo/sys/ipv4/inst/dom-default.json?query-target=children"


    payload={}
    headers = {
    'Cookie': 'APIC-cookie='+cookie
    }


    response = requests.request("GET", url, verify=False, headers=headers, data=json.dumps(payload)).json()
    interfaces = []
    for var in response["imdata"]:
        if var["ipv4If"]["attributes"]["id"]:
            interfaces.append(var["ipv4If"]["attributes"]["id"])
    return interfaces

#Uses the list of interfaces from getInterfaces to get the addresses and returns a dictionary of the interface and ip
def getAddress(addr,interfaces,cookie): #Gets the addresses from a NXOS device
    addresses={}
    for interface in interfaces:
        url = "https://"+addr+"//api/node/mo/sys/ipv4/inst/dom-default/if-["+interface+"].json?query-target=children"


        payload={}
        headers = {
        'Cookie': 'APIC-cookie='+cookie
        }


        response = requests.request("GET", url, verify=False, headers=headers, data=json.dumps(payload)).json()
        addresses[interface] = response["imdata"][0]["ipv4Addr"]["attributes"]["addr"]
    return addresses

#The following function is creating the OSPF from the API call. It requires the mgmtIP, ospf proccess id, ospf area number, svi name, and the cookie. It will create the new OSPF in the SVI interface for the API switches
def createOSPF(addr, ospf_process_id, ospf_area, svi_name, cookie):
   
    url = "https://"+addr+"/api/mo/sys.json"
   
    payload = {
    "topSystem": {
        "children": [
        {
            "ospfEntity": {
            "children": [
                {
                "ospfInst": {
                    "attributes": {
                    "name": ospf_process_id
                    },
                    "children": [
                    {
                        "ospfDom": {
                        "attributes": {
                            "name": "default"
                        },
                        "children": [
                            {
                            "ospfIf": {
                                "attributes": {
                                "advertiseSecondaries": "yes",
                                "area": ospf_area,
                                "id": svi_name
                                }
                            }
                            }
                        ]
                        }
                    }
                    ]
                }
                }
            ]
            }
        },
        {
            "interfaceEntity": {
            "children": [
                {
                "sviIf": {
                    "attributes": {
                    "id": svi_name
                    }
                }
                }
            ]
            }
        }
        ]
    }
    }
   
    headers = {
    'Content-Type': 'text/plain',
    'Cookie': 'APIC-cookie=' + cookie
    }




    response = requests.request("POST", url, verify = False, headers=headers, data=json.dumps(payload))

#The following function is creating the HSRP from the API call. It requires the mgmtIP, svi name, hsrp group, hsrp ip address, and the cookie. It will create the new HSRP in the VLAN's SVI interface for the API switches
def createHSRP(addr, svi_name, hsrp_grp, hsrp_add, cookie):
    
    
    url = "https://"+addr+"/api/mo/sys.json"
    
    payload = {
    
      "topSystem": {
        "children": [
          {
            "interfaceEntity": {
              "children": [
                {
                  "sviIf": {
                    "attributes": {
                      "id": svi_name
                    }
                  }
                }
              ]
            }
          },
          {
            "hsrpEntity": {
              "children": [
                {
                  "hsrpInst": {
                    "children": [
                      {
                        "hsrpIf": {
                          "attributes": {
                            "id": svi_name,
                            "version": "v2"
                          },
                          "children": [
                            {
                              "hsrpGroup": {
                                "attributes": {
                                  "af": "ipv4",
                                  "ctrl": "preempt",
                                  "id": hsrp_grp,
                                  "ip": hsrp_add,
                                  "ipObtainMode": "admin"
                                }
                              }
                            }
                          ]
                        }
                      }
                    ]
                  }
                }
              ]
            }
          }
        ]
      }
    }
    
    headers = {
      'Content-Type': 'text/plain',
      'Cookie': 'APIC-cookie=' + cookie
    }

    response = requests.request("POST", url, verify = False, headers=headers, data=json.dumps(payload))



#The following function is creating the new IP address for the switches by adding 1 to the 4th octet for VLAN 120. It returns the new IP address.
def updateSVIIP(ip):
    
	octets = ip.split(".")


	new_value = int(octets[4-1]) + 1 #Adding 1 to the 4th octet


	octets[4-1] = str(new_value) #Turning it to a string


	newSVIIP = (octets[0] + '.' + octets[1] + '.' + octets[2] + '.' + octets[3]) #Creating the new IP address
   	 
	return newSVIIP

#Changes the addresses from 172.16.x.x to 172.31.x.x and also can reset them back to 172.16 for the purpose of testing
def changeAddr(addresses,devtype): #Changes the addresses from 172.16 to 172.31
    if (devtype=="NXOS"):
        for var in addresses:
            addrSplit = addresses[var].split(".")
            if (addrSplit[1]=="16"):
                addrSplit[1] = "31"
            elif(addrSplit[1]=="31"):#Used to reset the addresses to 16
                addrSplit[1] = "16"
            addresses[var] = '.'.join(addrSplit)
        return addresses
    elif(devtype=="IOS-XE"):
        for var in addresses:
            addrSplit = addresses[var]["address"].split(".")
            if (addrSplit[1]=="16"):
                addrSplit[1] = "31"
            elif(addrSplit[1]=="31"):#Used to reset the addresses to 16
                addrSplit[1] = "16"
            addresses[var]["address"] = '.'.join(addrSplit)
        return addresses

#Sets the new addresses on a NXOS device
def setAddr(addr,newAddr,interface,cookie): #Sets the address on a NXOS device
    url = "https://"+addr+"//api/node/mo/sys/ipv4/inst/dom-default/if-["+interface+"].json?query-target=children"


    payload={
            "ipv4Addr": {
                "attributes": {
                    "addr": newAddr
                }
            }
        }
    headers = {
    'Cookie': 'APIC-cookie='+cookie
    }
    response = requests.request("POST", url, verify=False, headers=headers, data=json.dumps(payload)).json()


#Info needed for netconf
netconf_filter = """
 
<interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface></interface>
</interfaces>
 
"""


info = { "port" : "830",
          "username":"cisco","password":"cisco"}

#Used to get interfaces from an IOS-XE device
def getInt(device):
    with manager.connect(host=device,port=info['port'],username=info['username'],password=info['password'],hostkey_verify=False) as m:
 
        netconf_reply = m.get_config(source = 'running', filter = ("subtree",netconf_filter))
 
    netconf_data = xmltodict.parse(netconf_reply.xml)["rpc-reply"]["data"]
    interfaces={}
    for interface in netconf_data["interfaces"]["interface"]:
        #print(interface)
        if(str(interface["name"]).find("L")==-1):
            interfaces[interface["name"]]={
                "address":interface["ipv4"]["address"]["ip"],
                "netmask":interface["ipv4"]["address"]["netmask"]
                }
    return(interfaces)



#Used to change the ip on an IOS-XE device
def changeInt(device,xmlInt):#Changes the ip on a IOS-XE device
    with manager.connect(host=device,port=info['port'],username=info['username'],password=info['password'],hostkey_verify=False) as m:


        netconf_reply = m.edit_config(target = 'running', config = xmlInt)
        #print(netconf_reply)


#MAIN
inventory = loadInventory()

#IP Address for the sw01 SVI interface first for VLAN 120 in the for loop.
ip_svi_addr = "172.16.120.2"


for device in inventory:
    if (inventory[device]["devType"]=="NXOS"):
        ip = inventory[device]["mgmt"]
        cookie = getCookie(ip)
        createVlan(ip, "vlan-120" ,"vlan120", cookie)#Creates the vlan
        createSVI(ip,"vlan120",ip_svi_addr + "/24",cookie)
        ip_svi_addr = updateSVIIP(ip_svi_addr) #Once the IP SVI address is added for sw01, it will go into sw02 and add it in sw02 for VLAN 120 interface
        interfaces = getInterfaces(ip,cookie) #Gets the interfaces from the device
        addresses = getAddress(ip,interfaces,cookie)
        newAddr = changeAddr(addresses,inventory[device]["devType"])
        for var in newAddr:
            setAddr(ip,newAddr[var],var,cookie)
            createHSRP(ip,var,"10",newAddr[var],cookie)
            createOSPF(ip,"1","0.0.0.0",var,cookie)
    elif(inventory[device]["devType"]=="IOS-XE"):
         ip = inventory[device]["mgmt"]
         addresses = getInt(ip)
         newAddr = changeAddr(addresses,inventory[device]["devType"])
         for interface in newAddr:
            if not (interface[-1]=="1"):
                xmlInt = """<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns = "urn:ietf:params:xml:ns:netconf:base:1.0">  
                        <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
                            <interface>
                                            <%intName%>
                                <name>%intNum%</name>
                               
                                <ip>                                    
                                                    <address>
                                                        <primary>
                                                            <address>%addr%</address>
                                                            <mask>%mask%</mask>
                                                        </primary>
                                                    </address>                                  
                                </ip>              
                                </GigabitEthernet>
                            </interface>
                           
                                </native>
                        </config>"""  
                xmlInt = xmlInt.replace("%addr%", newAddr[interface]["address"])
                xmlInt = xmlInt.replace("%intName%", "GigabitEthernet")
                xmlInt = xmlInt.replace("%intNum%", interface[-1])
                xmlInt = xmlInt.replace("%mask%", newAddr[interface]["netmask"])
                changeInt(ip,xmlInt)

#Manually typed these in the routers:

##Ospf commands for routers:
##dist-rtr01:
##Router ospf 1
##Network 172.31.252.0 0.0.0.3 area 0
##Network 172.31.252.8  0.0.0.3 area 0
##Network 172.31.252.16 0.0.0.3 area 0
##Network 172.31.252.20 0.0.0.3 area 0
##Network 172.31.252.24 0.0.0.3 area 0

##dist-rtr02:
##Router ospf 1
##Network 172.31.252.4 0.0.0.3 area 0
##Network 172.31.252.12 0.0.0.3 area 0
##Network 172.31.252.16 0.0.0.3 area 0
##Network 172.31.252.28 0.0.0.3 area 0
##Network 172.31.252.32 0.0.0.3 area 0
