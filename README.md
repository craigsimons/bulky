## Overview

Bulky is an SSH tool intended to push bulk changes to a number of hosts. While there are other ways to accomplish this like [Ansible](https://www.ansible.com/), I don't know how to use those, so this is what you get...

## Installation

Assuming a Python 2.x environment, only the [Paramiko](http://www.paramiko.org/) module needs to be installed. This is best done by using the [pip](https://pypi.python.org/pypi/pip) package installer.

#### MacOS, Linux

```bash
sudo easy_install pip
sudo pip install paramiko
```

Then, download the bulky.py file and that's pretty much it.

### Command Line Arguments 

```
usage: bulky.py [-h] [-l LIST] [-f FILE] [-c COMMAND] [-cf COMMANDFILE] [-t]

Do lots of stuff quickly.

optional arguments:
  -h, --help            show this help message and exit
  -l LIST, --list LIST  Comma separated list of ip addresses or switches to do stuff on.
  -f FILE, --file FILE  CSV file hosts and variables. Should be delimited with quotes. 
                        If variable substitution is being used, the number of columns must exactly match 
                        the number of variables for each host.
  -c COMMAND, --command COMMAND
                        Command to issue. Use {{integer}} for variable substition.
  -cf COMMANDFILE, --commandfile COMMANDFILE
                        Command file to load. Use {{integer}} for variable substition.
  -t, --test            Run in test mode without actually connecting to the host.
```

## Instructions

**Note:** Under most circumstances, it is recommented the **--test** parameter be used to ensure the commands being sent are correct.

#### Example 1: Basic Use

This example shows how to run a single command to a small number of hosts. 

```bash
python bulky.py -l host1.sfu.ca,host2.sfu.ca -c "ls -l"
```

#### Example 2: Simple Use with Hosts File

For scenarios with large numbers of hosts, a separate file can be used.

Example file: **hosts.txt**
```
host1.sfu.ca
host2.sfu.ca
host3.sfu.ca
```

Command:
```bash
python bulky.py -f hosts.txt -c "ls -l"
```

#### Example 3: Simple Use with Command File)

For scenarios with a larger set of commands, a separate input file can be used.

**Note:** Bulky will attempt to strip bank lines and condense the supplied commands into a single line (spearated by the ; character). This is a restriction of the underlying SSH channel used by the Paramiko library. It is recommended to run Bulky with the **-test** parameter to ensure the commands being sent are compatible.

Example file: **commands.txt**
```
ls -l
pwd
date
```

Command:
```bash
python bulky.py -l host1.sfu.ca,host2.sfu.ca -cf commands.txt
```

#### Example 4: Advanced Use with Variable Replacement

Bulky allows for simple variable substitution. Variables are defined in the command string using the {{integer}} format starting at 0. Variables are defined in the input host file (-f) in CSV format. 

Example file: **commands.txt**
```
ls -l {{0}}
id {{1}}
```

Example file: **hosts.txt**
```
host1.sfu.ca,"w*","root"
host2.sfu.ca,"a*","root"
```

Command:
```bash
python bulky.py -f hosts.txt -cf commands.txt
```

## License

This project is licensed under the terms of the MIT license.