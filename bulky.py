import paramiko
import getpass
import socket
import argparse
from argparse import RawTextHelpFormatter

def main():
	# get command line arguments
	args = getArgs()

	user = raw_input("Enter your username:")
	password = getpass.getpass("Enter your password:")
	args = getArgs()
	hosts = getHosts(args)

	for host in hosts:
		ssh(host, user, password, args.command)

def getHosts(args):

	if args.file:
		with open(args.file) as f:
			return f.read().splitlines()

	return args.list.split(',')

def getArgs():
	"""
	Gets command line arguments and switches.
	@return list Command Line arguments.

	"""
	global logger

	desc = "Do lots of stuff quickly.\n\n"
	parser = argparse.ArgumentParser(description=desc, formatter_class=RawTextHelpFormatter)
	parser.add_argument("-l", "--list", help="Comma separated list of ip addresses or switches to do stuff on.", required=False)
	parser.add_argument("-f", "--file", help="File of hosts", required=False)
	parser.add_argument("-c", "--command", help="Command to issue", required=True)

	result = parser.parse_args()

	return result

def ssh(host, user, password, command):
	ssh = paramiko.SSHClient()
	ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

	try:
		ssh.connect(host, username=user, password=password)
		stdin,stdout,stderr= ssh.exec_command(command)

		print ""
		print "#####################"
		print " From " + host
		print "#####################"
		print ""
		for line in stdout:
			print line.strip('\n')

		ssh.close()

	except socket.gaierror:
		print "Error: " + host + " doesn't resolve or doesn't exist"
	except paramiko.AuthenticationException:
		print "Error: " + host + " failed authentication"

main()