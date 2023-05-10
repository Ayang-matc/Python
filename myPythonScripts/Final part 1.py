import json

# Define the name of your inventory file
INVENTORY_FILE = 'inventory.json'

def load_inventory():
    """
    Loads the inventory from the file in JSON format and returns it as a dictionary.
    """
    with open(INVENTORY_FILE, 'r') as f:
        inventory = json.load(f)
    return inventory

def save_inventory(inventory):
    """
    Saves the inventory dictionary to the file in JSON format.
    """
    with open(INVENTORY_FILE, 'w') as f:
        json.dump(inventory, f)

def display_devices(inventory):
    """
    Displays all devices in the inventory dictionary.
    """
    print('Current inventory:')
    for hostname, device in inventory.items():
        print(f'Hostname: {hostname}, Device type: {device["type"]}, Management IP: {device["ip"]}')

def add_device(inventory):
    """
    Prompts the user for information about a new device and adds it to the inventory dictionary.
    """
    hostname = input('Enter the hostname of the new device: ')
    dev_type = input('Enter the device type (NXOS or IOS-XE): ')
    ip = input('Enter the management IP address of the new device: ')
    inventory[hostname] = {'type': dev_type, 'ip': ip}
    print(f'Device {hostname} added to inventory.')

def modify_device(inventory):
    """
    Prompts the user for the hostname of a device to modify and then prompts for new information about the device.
    """
    hostname = input('Enter the hostname of the device to modify: ')
    if hostname in inventory:
        dev_type = input('Enter the new device type (NXOS or IOS-XE): ')
        ip = input('Enter the new management IP address: ')
        inventory[hostname]['type'] = dev_type
        inventory[hostname]['ip'] = ip
        print(f'Device {hostname} modified in inventory.')
    else:
        print(f'Device {hostname} not found in inventory.')

def delete_device(inventory):
    """
    Prompts the user for the hostname of a device to delete and removes it from the inventory dictionary.
    """
    hostname = input('Enter the hostname of the device to delete: ')
    if hostname in inventory:
        del inventory[hostname]
        print(f'Device {hostname} deleted from inventory.')
    else:
        print(f'Device {hostname} not found in inventory.')

def main():
    # Load the inventory from the file
    inventory = load_inventory()

    # Display all devices in the inventory
    display_devices(inventory)

    # Offer options to add, modify, or delete a device
    while True:
        print('\nOptions:')
        print('1. Add a device')
        print('2. Modify a device')
        print('3. Delete a device')
        print('4. Save changes to inventory')
        print('5. Exit')
        choice = input('Enter your choice: ')
        if choice == '1':
            add_device(inventory)
        elif choice == '2':
            modify_device(inventory)
        elif choice == '3':
            delete_device(inventory)
        elif choice == '4':
            save_inventory(inventory)
            print('Changes saved to inventory file.')
        elif choice == '5':
            break
        else:
            print('Invalid choice.')

if __name__ == '__main__':
    main()
