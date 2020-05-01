#! usr/bin/env python

import subprocess
import argparse
import re

#Argument function - takes user input and sets varibales
def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i ", "--interface ", dest="interface", help="Interface you would like to modify " )
    parser.add_argument("-m ", "--mac", dest="new_mac", help="New MAC address ")
    args = parser.parse_args()
    if not args.interface:
        parser.error("[-]) Please specify a network interface, use --help for more information")
    elif not args.new_mac:
        parser.error("[-] Please specify a new MAC address, use --help for more information")
    return args

  #change_mac fnction changes the mac adress by using subprocess to run terminal commands and passes the interface & new_mac functions
def change_mac(interface, new_mac):
    print("[+] Changing MAC address for " + interface + " to " + new_mac)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["ifconfig", interface, "up"])


#prints current MAC and uses regex to print the new mac address
def get_current_mac(interface):
    ifconfig_return = subprocess.check_output(["ifconfig", interface])
    mac_address_search_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_return)
    if mac_address_search_result:
        return mac_address_search_result.group(0)
    else:
        print("[-] Could not read MAC address ")



#calls Arguments
args = get_arguments()
current_mac = get_current_mac(args.interface)  #gets current MAC using get_current_mac function
print("Current MAC = " + str(current_mac)) #casts as string 

change_mac(args.interface, args.new_mac) #changes MAC

current_mac = get_current_mac(args.interface)
if current_mac == args.new_mac:
    print("[+] MAC address for " + args.interface + " was successfully changed to " + current_mac)
else:
    print("[-] MAC address was not changed")
