import json
import requests

def getCookie(url) :

    payload= {"aaaUser" :
              {"attributes" :
                   {"name" : "cisco",
                    "pwd" : "cisco"}
               }
          }

    response = requests.post(url, json=payload, verify = False)
    
    return response.json()["imdata"][0]["aaaLogin"]["attributes"]["token"]

cookie = getCookie("https://10.10.20.177/api/aaaLogin.json")

url = 'https://10.10.20.177/api/mo/sys.json'

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
      "id": "vlan101"
    },
"children": [
{
"ipv4Addr": {
  "attributes": {
    "addr": "10.0.0.21/24"
}}}]}}]}}]}}]}}]}}

headers = {
    'Content-Type' : 'text/plain',
    'Cookie' : 'APIC-cookie=' + cookie
}

response = requests.request('POST', url, verify = False, headers=headers, data=json.dumps(payload))

print (response.json())



