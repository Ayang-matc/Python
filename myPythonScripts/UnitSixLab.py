### Nested dictionary
devices = {
    'sw01': {
        'hostname' : 'dist-sw01',
        'deviceType' : 'switch',
        'mgmtIP' : '10.10.20.177',
        },
    'sw02': {
        'hostname' : 'dist-sw02',
        'deviceType' : 'switch',
        'mgmtIP' : '10.10.20.178',
        }}
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
### For table 
def deviceTable():
    print('Host \t\t Type \t\t MgmIP')
    print('-'*50)
    for switch in devices.values():
        hostname = switch['hostname'] + '\t'
        dType = switch['deviceType'] + '\t\t'
        mgmtIP = switch['mgmtIP']
        
        print (hostname, dType, mgmtIP)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## which Mgmt ip and cmd you want

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

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
## shows hostname and memory

def dVersion():
    sw01 = '10.10.20.177'
    sw02 = '10.10.20.178'
    cmd = 'show version'
    device1 = deviceCmd(sw01,cmd)
    device2 = deviceCmd(sw02,cmd)
    print(device1['host_name'] + '\t' + str(device1['memory']) + '\t' + str(device1['mem_type']) + '\t' + device1['chassis_id'] + '\t\t' + device1['kick_file_name']) 
    print(device2['host_name'] + '\t' + str(device2['memory']) + '\t' + str(device2['mem_type']) + '\t' + device2['chassis_id'] + '\t\t' + device2['kick_file_name'])  
    

dVersion()
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''



