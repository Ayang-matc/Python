router1 = {
    'hostname': 'R1',
    'brand': 'Cisco',
    'mgmIP': '10.0.0.1',
    'interfaces': {
        'G0/0': '10.1.1.1',
        'G0/1': '10.1.2.1'
        }}

sortDict = False

##while sortDict == False:
##    selectDict = input('Which Dictionary do you want to sort?')
##    if 


print ('router1 keys\n',router1.keys())
print ('router1[interfaces] keys\n',router1['interfaces'].keys())
print ('router1 values\n',router1.values())
print ('router1[interfaces] values\n',router1['interfaces'].values())
print ('router1 items\n',router1.items())
print ('router1[interfaces] items\n',router1['interfaces'].items())
