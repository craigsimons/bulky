import paramiko
import getpass
import socket
import argparse
import csv
import re
import sys
from argparse import RawTextHelpFormatter

def main():
	# get command line arguments
	args = getArgs()
	hosts = getHosts(args)
	# get command
	command = getCommand(args)
	varCount = getCommandVarCount(command)

	if not args.test:
		user = raw_input("Enter your username:")
		password = getpass.getpass("Enter your password:")	

	for line in hosts:
		# Read each CSV line and arrange into host and variable array
		thisLine = csv.reader([line])
		columns = list(thisLine)[0]
		host = columns[0]
		columns.pop(0)
		columnCount = len(columns)

		# test if variables in each coc
		if varCount != len(columns):
			print "There is a problem with: " + str(line)
			print "Number of variables in supplied command was " + str(varCount) + " but the host entry had " + str(columnCount) + " variable columns!"
			sys.exit(1)

		if not args.test:
			ssh(host, user, password, replaceVariables(columns, command))
		else:
			printBanner(host, replaceVariables(columns, command))

def replaceVariables(variables, command):
	"""
	Replaces all variables in the format {{integer}}
	"""
	for i, value in enumerate(variables):
		command = command.replace("{{" + str(i) + "}}",variables[i])

	return command

def getHosts(args):
	""" 
	Reads CSV file in 
	"""
	if args.file:
		with open(args.file) as f:
			return f.read().splitlines()

	return args.list.split(',')

def getCommand(args):
	if args.commandfile:
		command = open(args.commandfile, 'r').read()
		return parseCommand(command)
	elif args.command:
		return args.command
	else:
		print "No command or command file specified"
		sys.exit(1)

def parseCommand(command):
	result = []
	commands = command.split('\n')
	for line in commands:
		if line:
			result.append(line)
	return "; ".join(result)

def getCommandVarCount(command):
	""" 
	Get the number of variables in the command. This number will be used to test each host entry
	"""
	if command:
		return len(re.findall('\{\{.*?\}\}', command))
	else:
		return 0

def getArgs():
	"""
	Gets command line arguments and switches.
	@return list Command Line arguments.

	"""
	global logger

	desc = "Do lots of stuff quickly.\n\n"
	parser = argparse.ArgumentParser(description=desc, formatter_class=RawTextHelpFormatter)
	parser.add_argument("-l", "--list", help="Comma separated list of ip addresses or switches to do stuff on.", required=False)
	parser.add_argument("-f", "--file", help="CSV file hosts and variables. Should be delimited with quotes. \nIf variable substitution is being used, the number of columns must exactly match \nthe number of variables for each host.", required=False)
	parser.add_argument("-c", "--command", help="Command to issue. Use {{integer}} for variable substition.", required=False)
	parser.add_argument("-cf", "--commandfile", help="Command file to load. Use {{integer}} for variable substition.", required=False)
	parser.add_argument("-t", "--test", help="Run in test mode without actually connecting to the host.", action="store_true")

	result = parser.parse_args()

	return result

def printBanner(host, command):
		print ""
		print "#####################"
		print " From " + host
		print "#####################"
		print ""
		print "Command: " + command
		print ""

def ssh(host, user, password, command):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		ssh.connect(host, username=user, password=password)
		stdin,stdout,stderr= ssh.exec_command(command)

		printBanner(host, command)
		for line in stdout:
			print line.strip('\n')

		ssh.close()

	except socket.gaierror:
		print "Error: " + host + " doesn't resolve or doesn't exist"
	except paramiko.AuthenticationException:
		print "Error: " + host + " failed authentication"

main()