import requests
import json

"""
Be sure to run feature nxapi first on Nexus Switch

"""
switchuser='cisco'
switchpassword='cisco'

url='https://10.10.20.177/ins'
myheaders={'content-type':'application/json-rpc'}
payload=[
  {
    "jsonrpc": "2.0",
    "method": "cli",
    "params": {
      "cmd": "show ip interface brief",
      "version": 1
    },
    "id": 1
  }
]

'''

verify=False below is to accept untrusted certificate

'''

response = requests.post(url,data=json.dumps(payload), verify=False,headers=myheaders,auth=(switchuser,switchpassword)).json()

print(response)

def IPTable(ipDict):
    print ('\nName \tproto \tlink \t Ip Address')
    print ('-'*50)
    for key in ipDict['result']['body']['TABLE_intf']['ROW_intf']:
        interfaces = (key['intf-name'])
        if len(interfaces) <= 7:
            interfaces = interfaces + '\t'
        proto = (key['proto-state']) + '\t'
        link = (key['link-state']) + '\t'
        ipAdd = (key['prefix']) + '\t'
        print (interfaces, proto, link, ipAdd)

        

