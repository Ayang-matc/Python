name = input('what is your name: ')
age = input('what is your age: ')
x = 5
NewAge = (x+int(age))
numstring = NewAge.__str__()
print ('Hello ' + name + '. In five years, you will be ' + numstring + ' years old!')
