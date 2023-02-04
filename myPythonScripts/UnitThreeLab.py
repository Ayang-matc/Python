def yourname():
    validName = False

    while validName == False:
        name = input('what is your name? ')
        nameList = name.split(' ')
        nameIsAlpha = checkName(nameList)
        if nameIsAlpha == True:
            validName = True
            print ('Hello,' , name)
        else:
            print ('name is not valid, please use letters only.')

def checkName(names):
    #['a', 'd']
    valid = True
    for name in names:
        if name.isalpha() == False:
            valid = False      
    return valid


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

ntpServer = {
    'Server1' : '221.100.250.75',
    'Server2' : '201.0.113.22',
    'Server3' : '58.23.191.6',
    }

def Table(server):
    print ('Server Name \t Address')
    print ('-'*50)
    for key in server.keys():
        print (key, '\t' ,  server[key])
    ipList = (server.values())
    PingPrep(ipList)


   
def PingPrep(ipList):
    print ('\n')
    for ip in ipList:
        print ('ping', ip )


''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

devices = {
    'R1': {'type' : 'router', 'hostname' : 'R1', 'mgmtIP' : '10.0.0.1'},
    'R2': {'type' : 'router', 'hostname' : 'R2', 'mgmtIP' : '10.0.0.2'},
    'S1': {'type' : 'router', 'hostname' : 'S1', 'mgmtIP' : '10.0.0.3'},
    'S2': {'type' : 'router', 'hostname' : 'S2', 'mgmtIP' : '10.0.0.4'}
    }

def ping():
    for key in devices:
        print ('ping ' + devices[key]['mgmtIP'])


def newDevice():
    isValidDevice = False

    while isValidDevice == False:
        addDevice = input('would you like to add a Device (y or n)? ')

        if addDevice == 'y':
            isValidDevice = True
            whatName = input('What is the name of the device? ')
            whatType = input('What is the device type? ')
            whatBrand = input ('What is the brand of the device? ')
            whatMgmtIP = input('What IP address do you want to assign to management IP? ')
            validIP = checkIP(whatMgmtIP)
            devices[whatName] = {
                'hostname': whatName,
                'type': whatType,
                'brand': whatBrand,
                'mgmtIP': validIP,
                }
            print ('\n')
            ping()

            
        elif addDevice == 'n':
            return
        
        else:
            print('Invalid input')


#checking IP
            
def checkIP(ip):
    isValidIP = False
    while isValidIP == False:
        newIPList = ip.split('.')
        ifnumber = True
        if len(newIPList) == 4: 
            for y in newIPList:
                if y.isnumeric() == True:
                    number = int(y)
                    if number > 255 or number < 0:
                        ifnumber = False
                else:
                    ifnumber = False
        else:
            ifnumber = False
            
        if ifnumber == True:
           return ip
        if ifnumber == False:
           ip = input('Please enter valid IP ')







        

