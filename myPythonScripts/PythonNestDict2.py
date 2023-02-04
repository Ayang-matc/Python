devices = {
    'R1': {'type' : 'router', 'hostname' : 'R1', 'mgmtIP' : '10.0.0.1'},
    'R2': {'type' : 'router', 'hostname' : 'R2', 'mgmtIP' : '10.0.0.2'},
    'S1': {'type' : 'router', 'hostname' : 'S1', 'mgmtIP' : '10.0.0.3'},
    'S2': {'type' : 'router', 'hostname' : 'S2', 'mgmtIP' : '10.0.0.4'}
    }

for key in devices:
    print ('ping ' + devices[key]['mgmtIP'])
