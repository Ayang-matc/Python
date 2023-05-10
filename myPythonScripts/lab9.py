#Adam Yang
#4/2/23

#Unit 9 Lab

import requests
import json
import urllib3
urllib3.disable_warnings()

#The following function is getting a token/cookie from the request. It requires the url of the API aaaLogin from the switch that wants to be authenticated. It returns the token number. 
def getCookie(url) :

 
    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False)
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

def createVlan(deviceIP, vlan_num, vlan_name, cookie):
    url = "https://" + deviceIP + "/api/node/mo/sys.json"
    
    payload = {
        
  "topSystem": {
    "children": [
      {
        "bdEntity": {
          "children": [
            {
              "l2BD": {
                "attributes": {
                  "fabEncap": "vlan-" + vlan_num,
                  "name": vlan_name
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

def createSVIInt(deviceIP, svi_name, ip, subnet_mask, cookie):
    url = "https://" + deviceIP + "/api/node/mo/sys.json"
    
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
                                  "id": svi_name
                                },
                                "children": [
                                  {
                                    "ipv4Addr": {
                                      "attributes": {
                                        "addr": ip + subnet_mask
                                        
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
          },
          {
            "interfaceEntity": {
              "children": [
                {
                  "sviIf": {
                    "attributes": {
                      "adminSt": "up",
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

def createHSRP(deviceIP, sviVlan, hsrp_grp, hsrp_ipv4, cookie):

    url = "https://" + deviceIP + "/api/node/mo/sys.json"
    
    payload = {
      "topSystem": {
        "children": [
          {
            "interfaceEntity": {
              "children": [
                {
                  "sviIf": {
                    "attributes": {
                      "id": sviVlan
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
                            "id": sviVlan,
                            "version": "v2"
                          },
                          "children": [
                            {
                              "hsrpGroup": {
                                "attributes": {
                                  "af": "ipv4",
                                  "ctrl": "preempt",
                                  "id": hsrp_grp,
                                  "ip": hsrp_ipv4,
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
###########################################################################################################################
    
def createOSPF(deviceIP, sviVlan, ospfNumber, area, cookie):
    url = "https://" + deviceIP + "/api/node/mo/sys.json"
    
    payload = {
      "topSystem": {
        "children": [
          {
            "ospfEntity": {
              "children": [
                {
                  "ospfInst": {
                    "attributes": {
                      "name": ospfNumber
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
                                  "area": area,
                                  "id": sviVlan
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
                      "id": sviVlan
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

###Main

#Get Session Cookie from dist-sw01.
cookie = getCookie('https://10.10.20.177/api/aaaLogin.json')

createVlan("10.10.20.177", "9", "cisco", cookie)
createSVIInt("10.10.20.177", "vlan9", "192.168.1.109", "/24", cookie)
createHSRP('10.10.20.177', 'vlan9', '10', '192.168.1.1', cookie)
createOSPF('10.10.20.177', 'vlan9', '1', '0', cookie)
