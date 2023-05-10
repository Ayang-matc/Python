#Adam Yang

#Switching host name

import requests
import json
import urllib3
urllib3.disable_warnings()

#Gets cookie from device
def getCookie(url) :
    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False)
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]
    print(x)

#This function allows you to switch host name 
def changeHostName(newHostName, mgmtIP, cookie):
    url = f"https://{mgmtIP}/api/mo/sys.json"

    payload = {
        "topSystem": {
            "attributes": {
                "name": newHostName
            }
        }
    }

    headers = {
        "Content-Type": "application/json",
        "Cookie": f"APIC-cookie={cookie}"
    }

    response = requests.post(url, headers=headers, json=payload, verify=False)


#Checks to see if the management IP is valid
def checkMgmtIP(ip):
    if ip == "10.10.20.177" or ip == "10.10.20.178":
        return True

    else:
        return False

#Checks to see if the host name is valid    
def validMgmtIPInput():
    validInput = False
    while validInput == False:
        userMgmtIP = input("Enter the management IP address of the switch you would like the hostname to change (dist-sw01: 10.10.20.177 or dist-sw02: 10.10.20.178). \n")
        validMgmtIP = checkMgmtIP(userMgmtIP)
        if validMgmtIP == True:
            return  userMgmtIP
        else:
            print("Invalid! Please try again. \n")
            validInput = False

#Check host name to see if it is valid
def checkHostName(newHostName):
    allowedChars = set('-_')
    validHostName = True
    if newHostName[0].isalpha() == False:
        validHostName = False
    else:
        if " " in newHostName:
            validHostName = False
        else:
            for char in newHostName:
                if newHostName.isalnum() or allowedChars == False:
                    validHostName = False
            else:
                return validHostName

#Checks to see if the host name is valid       
def validHostNameInput():
    validInput = False
    while validInput == False:
        userHostName = input("Enter the new hostname for the switch. \n")
        validHostName = checkHostName(userHostName)
        if validHostName == True:
            return userHostName
        else:
            print("Invalid! Please try again. \n")
            validInput = False
    
##MAIN
#
def deviceNameChange():
    mgmtIPInput = validMgmtIPInput()
    cookie = getCookie(f'https://{mgmtIPInput}/api/aaaLogin.json')
    hostNameInput = validHostNameInput()
    changeHostName(hostNameInput, mgmtIPInput,cookie)
    print(f"\nHostname has been changed to {hostNameInput}!")


deviceNameChange()  