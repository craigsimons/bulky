## Overview

Bulky is an SSH tool intended to push bulk changes to a number of hosts. While there are other ways to accomplish this like [Ansible](https://www.ansible.com/), I don't know how to use those, so this is what you get...

## Installation

Assuming a Python 2.x environment, only the [Paramiko](http://www.paramiko.org/) module needs to be installed. This is best done by using the [pip](https://pypi.python.org/pypi/pip) package installer.

### MacOS, Linux

```bash
sudo easy_install pip
sudo pip install paramiko
```

Then, download the bulky.py file and that's pretty much it.

## Instructions

### Simple Use

This example shows how to run a single command to a small number of hosts. 

```bash
python bulky.py -l host1.sfu.ca,host2.sfu.ca -c "ls -l"
```

### Simple Use (with hosts file)

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

### Simple Use (with command file)

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

### Advanced Use (Variable Replacement)

Bulky allows for simple variable substitution.

## License

This project is licensed under the terms of the MIT license.