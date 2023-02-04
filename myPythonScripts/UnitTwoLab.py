router1 = {
    'hostname': 'R1',
    'brand': 'Cisco',
    'model': '1941',
    'mgmtIP': '10.0.0.1',
    'g0/0': '10.0.1.1 /24',
    'g0/1': '10.0.2.1 /24',
    'g0/2': '10.0.3.1 /24'
    }

router1_list = list(router1.keys())
interface_list = router1_list[3:]
management_list = router1_list[:3]

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
    
def selectInt():
    whichInt = False
    while whichInt == False:
        selectedInt = input('Choose interface ' + (', '.join(map(str, interface_list))) + ': \n')
        if selectedInt in interface_list:
            return selectedInt
        else:
            print ('Invalid interface!')
            
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
        
def changeMgmtIP():
    isValidIP = False

    while isValidIP == False:
        changeIP = input('Do you want to change the Management IP Address (y or n) ?: ')
        if changeIP == 'y':
            quest = False
            while quest == False:
                newIP = input('Please enter new IP address for the Management Interface: ')
                newIPList = newIP.split('.')
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
                   print ('Address Updated!')
                   router1['mgmtIP'] = newIP
                   router1Table()
                   break
                if ifnumber == False:
                   print ('Ip address must be x.x.x.x where x>= 0 and x <=255.')
            break
        if changeIP == 'n':
            print ('Nothing changed')
            break
        else:
            print ('please only enter (y or n).')
            
''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def router1Table():
    header=''
    value=''

    for key in router1.keys():
        header = header + key + ' '
        if len(key) >= 8:
            header = header + '\t'
        else:
            header = header + '\t\t'
        value = value + router1[key] 
        if len(router1[key]) >= 8:
            value = value + '\t'
        else:
            value = value + '\t\t'
            
    value = value.replace (' /24', '')
    print (header)
    print ('-'*145)
    print (value)

''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

def changeIP():
    selectedInt = str(selectInt())
    quest = False
    while quest == False:
        newIP = input('Please enter new IP address for the ' + selectedInt + ' Interface: ')
        newIPList = newIP.split('.')
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
           print (selectedInt + ' address updated!')
           router1[selectedInt] = newIP
           router1Table()
           break
        if ifnumber == False:
           print ('Ip address must be x.x.x.x where x>= 0 and x <=255.')

           
router1Table()
