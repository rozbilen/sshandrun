#! /usr/bin/python3
# Author: Yasin Cengiz
# Purpose: SSH into list of devices and run list of commands

import getopt,sys,paramiko,getpass
from datetime import datetime

# Ensuring variables exist
commandfile, username, devicefile = "default", "default", "default"

def usage():
	print("\nOptions: \n-h: help \n-l: device list \n-u: username \n-c: command list \n\nUsage: ssh.py -u bob -l device-list.txt -c command-list.txt\n")
	return

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

# This will throw an error if unsupported parameters are received.
try:
	# This grabs input parameters. If the paramater requires an argument, it should have a colon ':' after. IE, -h does not require argument, -l, -u, -c do, so they get colons
	opts, args = getopt.getopt(sys.argv[1:], "hl:u:c:d:")
except getopt.GetoptError as err:
	# print help information and exit:
	print(str(err)) # will print something like "option -a not recognized"
	usage()
	sys.exit(2)

# This loops through the given parameters and sets the variables. The letters o and a are arbitrary, anything can be used.
# The logic is 'if paramater = x, set variable'.
for o, a in opts:
	if o == "-l":
		devicefile = a
	elif o in ("-h"):
		usage()
		sys.exit()
	elif o in ("-u"):
		username = a
	elif o in ("-c"):
		commandfile = a
	else:
		assert False, "unhandled option"

# This prints the given arugments
print("Username: ", username)
print("Device List: ", devicefile)
print("Command List: ", commandfile)

password = getpass.getpass("What is your password? ")

# Opens files in read mode
f1 = open(devicefile,"r")
f2 = open(commandfile,"r")

# Creates list based on f1 and f2
devices = f1.readlines()
commands = f2.readlines()

# This function loops through devices. No real need for a function here, just doing it.
def connect_to(x):
	for device in x:
		# This strips \n from end of each device (line) in the devices list
		device = device.rstrip()
		# This opens an SSH session and loops for every command in the file
		for command in commands:
			# This strips \n from end of each command (line) in the commands list
			command = command.rstrip()
			ssh = paramiko.SSHClient()
			ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			ssh.connect(device, username=username, password=password)
			stdin, stdout, stderr = ssh.exec_command(command)
			output = open(device + ".out", "a")
			output.write("\n\nDateTime: "+dt_string+"\nCommand Issued: "+command+"\n")
			output.writelines(stdout)
			output.write("\n")
			print("Your file has been updated, it is ", device+".out")
			ssh.close()
connect_to(devices)
f1.close()
f2.close()
# END 


# ./ssh.py -h

'''Options:
-h: help
-l: device list
-u: username
-c: command list

Usage: ssh.py -u yasin -l device-list.txt -c command-list.txt'''
