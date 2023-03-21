'Adam Yang Midterm'
###################################################################################################
'Used to get (sh ip int br) cmd table from device' 

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

    deviceInfo = response['result']['body']['TABLE_intf']['ROW_intf']

    return deviceInfo 

###################################################################################################
'Used to print table'

def deviceTable(response,mgmtIP):
    print('Mangagement IP: ' + mgmtIP)
    print('\nInterface\tProto\tLink\t IP Address')
    print('-'*50)
    for row in response:
        interface = row['intf-name'] + '\t\t'
        ipaddress = row['prefix']
        proto = row['proto-state'] + '\t'
        link = row['link-state'] + '\t'
        print(interface, proto, link, ipaddress)

###################################################################################################
'Used to change IP'
        
def changeIP(mgmtIP,intName,IP):
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
          "cmd": "ip add " + IP + ' 255.255.255.0',
          "version": 1
        },
        "id": 3
      }
    ]
    
    response = requests.post(url,data=json.dumps(payload),verify=False, headers=myheaders,auth=(switchuser,switchpassword)).json()

##################################################################################################
'Puts all the Vlans into a list'
    
def vlanOnly(device):
    vlanList = []
    for vlan in device:
        if 'Vlan' in vlan['intf-name']:
            name = vlan['intf-name']
            vlanList.append(name)
    return (vlanList)

##################################################################################################
'Puts all the vlan IPs into a list'
        
def vlanIPOnly(device):
    IPList = []
    for vlan in device:
        if 'Vlan' in vlan['intf-name']:
            IP = vlan['prefix']
            IPList.append(IP)
    return (IPList)

###################################################################################################
'Adds 5 to existing IP'

def addFive(vlanIP):
    for item in range(len(vlanIP)):
        parts = vlanIP[item].split('.')
        parts[-1] = str(int(parts[-1]) + 5)
        vlanIP[item] = '.'.join(parts)
    return (vlanIP)

###################################################################################################
'Used to ask if user wans to go through with the change'

def changeYesOrNo():
    while True:
        userChoice = input('\nwould you like to (y or n) ')
        if userChoice == 'y':
            return True
        elif userChoice == 'n':
            return False
        else:
            print ('invalid input')

###################################################################################################
'Dictionary of devices'

devices ={
    'dist-sw01': '10.10.20.177',
    'dist-sw02': '10.10.20.178'
    }
###################################################################################################
 'Changes IP by 5'   

def changeIPByFive():
    for ip in devices.values():
        mgmtIP = ip
        device = deviceCmd(mgmtIP,'sh ip int br')
        deviceTable(device,mgmtIP)
        vlan = vlanOnly(device)
        vlanIP = vlanIPOnly(device)
        newVlanIP = addFive(vlanIP)
        answer = changeYesOrNo()
        if answer == True:
            for vlan, IP in zip(vlan,newVlanIP):
                changeIP(mgmtIP,vlan,IP)
            newdevice = deviceCmd(mgmtIP,'sh ip int br')
            deviceTable(newdevice, mgmtIP)
            print ('\n')
        else:
            print ('Have a good day!\n')

###################################################################################################

changeIPByFive()
