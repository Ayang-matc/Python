'Adam yang Lab 7'
#####################################################################################################################################
'Which Mgmt ip and cmd you want'

def deviceCmd(ipadd,cmd):
    import requests
    import json
    ## disables warnings
    import urllib3
    urllib3.disable_warnings()

    """
    Modify these please
    """
    switchuser='cisco'
    switchpassword='cisco'

    url='https://'+ipadd+'/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": cmd,
          "version": 1
        },
        "id": 1
      }
    ]
    response = requests.post(url,data=json.dumps(payload),verify=False, headers=myheaders,auth=(switchuser,switchpassword)).json()
    
    return response

#####################################################################################################################################
'Gets interface list'

def getIntList(response):
    interfaces = response['result']['body']['TABLE_intf']['ROW_intf']
    intf_list = [intf['intf-name'] for intf in interfaces]
    return intf_list

#####################################################################################################################################
'Makes device table'

def deviceTable(response):
    print('\nInterface\tProto\tLink\t IP Address')
    print('-'*50)
    for row in response['result']['body']['TABLE_intf']['ROW_intf']:
        interface = row['intf-name'] + '\t\t'
        ipaddress = row['prefix']
        proto = row['proto-state'] + '\t'
        link = row['link-state'] + '\t'
        print(interface, proto, link, ipaddress)
        
#####################################################################################################################################
'Gets user input'
        
def getUserInput(intList):
    
    validAnswer = False
    while validAnswer == False:
        Int_list = intList
        # Prompt the user for interface details
        interface = input("Enter interface name: ")
        ip = input("Enter IP address: ")
        subnet = input("Enter subnet : ")

        # Validate the IP and subnet mask
        ip_valid = checkIP(ip)
        subnet_valid = checkMask(subnet)
        interface_valid = checkInterface(interface, Int_list)

        if interface_valid == True:
            if ip_valid == True:
                if subnet_valid == True:
                    ValidAnswer = True
                    return {"interface": interface, "ip": ip, "subnet": subnet}
                else:
                    validAnswer = False
                    print("Invalid subnet mask!")
            else:
                validAnswer = False
                print("Invalid IP address!")
        else:
            validAnswer = False
            print ('invalid Interface!')
        

#####################################################################################################################################
'Changes IP'

def changeAddress(mgmtIP,intName,IP,subnetMask):
    import requests
    import json
    ## disables warnings
    import urllib3
    urllib3.disable_warnings()

    """
    Modify these please
    """
    switchuser='cisco'
    switchpassword='cisco'

    url='https://'+mgmtIP+'/ins'
    myheaders={'content-type':'application/json-rpc'}
    payload=[
       {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "conf t",
          "version": 1
        },
        "id": 1
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "int " + intName,
          "version": 1
        },
        "id": 2
      },
      {
        "jsonrpc": "2.0",
        "method": "cli",
        "params": {
          "cmd": "ip add " + IP + ' ' + subnetMask,
          "version": 1
        },
        "id": 3
      }
    ]
    
    response = requests.post(url,data=json.dumps(payload),verify=False, headers=myheaders,auth=(switchuser,switchpassword)).json()
    

#####################################################################################################################################
'Checks Interface from interface list'

def checkInterface(interface, intList):
    if interface not in intList:
        return False
    else:
        return True        

#####################################################################################################################################
'Checks IP'

def checkIP(ip):
    isValidIP = True
    newIPList = ip.split('.')
    if len(newIPList) != 4:
        isValidIP = False
    else:
        for y in newIPList:
            if y.isnumeric() == False:
                isValidIP = False            
            else:
                number = int(y)
                if number > 255 or number < 0:
                    isValidIP = False
                else:
                    isValidIP = True
    return (isValidIP) 

#####################################################################################################################################
'checks subnet'

def checkMask(subnet):
    string = subnet.replace('/','')
    if string.isnumeric() == False:
        return False
    else:
        number = int(string)
        if number < 8 or number > 30:
            return False
        else:
            return True

    
    
#####################################################################################################################################
'subnet mask dictionary'
    
subnet_masks = {
    "/30": "255.255.255.252",
    "/29": "255.255.255.248",
    "/28": "255.255.255.240",
    "/27": "255.255.255.224",
    "/26": "255.255.255.192",
    "/25": "255.255.255.128",
    "/24": "255.255.255.0",
    "/22": "255.255.252.0",
    "/21": "255.255.248.0",
    "/20": "255.255.240.0",
    "/19": "255.255.224.0",
    "/18": "255.255.192.0",
    "/17": "255.255.128.0",
    "/16": "255.255.0.0",
    "/15": "255.254.0.0",
    "/14": "255.252.0.0",
    "/13": "255.248.0.0",
    "/12": "255.240.0.0",
    "/11": "255.224.0.0",
    "/10": "255.192.0.0",
    "/9": "255.128.0.0",
    "/8": "255.0.0.0"

}
    
#####################################################################################################################################
'ask Yes or no'

def changeYesOrNo():
    while True:
        userChoice = input('\nwould you like to change (y or n) ')
        if userChoice == 'y':
            return True
        elif userChoice == 'n':
            return False
        else:
            print ('invalid input')
            
#####################################################################################################################################
'Runs Sh ip int br command and asks if you want to change the ip of an interface'
    
def showIP():
    mgmtIP = input ('What is the management IP of the switch or router you would like to see? ')
    validMgmtIP = checkIP(mgmtIP)
    if validMgmtIP ==  True:
        ipChart = deviceCmd(mgmtIP, 'sh ip int br')
        deviceTable(ipChart)
        intList = getIntList(ipChart)
        userChoice = changeYesOrNo()
        if userChoice == True:
            userInput = getUserInput(intList)
            intf = userInput['interface']
            ip = userInput ['ip']
            subnetmask = subnet_masks[(userInput['subnet'])]
            changeAddress(mgmtIP, intf, ip, subnetmask)
            newIPChart = deviceCmd(mgmtIP, 'sh ip int br')
            deviceTable(newIPChart)
        else:
            print ('Have a good day')
    else:
        print ('IP invalid')
        showIP()

showIP()
