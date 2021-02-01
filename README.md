# Govaster
Tool to recursively bruteforce directories with gobuster.

## About the Tool
This tool uses the same flags, same modes, as offered by gobuster itself(dir,dns,vhost). No harsh changes you want to look at, so if you want to go recursive, just use ```-R``` and it will launch multiple threads at each directory it finds, without any further ados. Also, if any directory found(using recursive approach), it will be displayed in a colored output. Make sure, you have the base tool installed(gobuster). It's more of a plugin to the tool, which allows it to search recursively.

Note: Currently, it doesn't support s3 and fuzzing mode.

### Warning
This tool might take a little more time than a usual gobuster scan, as it has to manage multiple threads running in conjuction with various subprocesses. So just make sure you increase your threads about to 20 or more. If you have not much problem with delayed outputs, then default number of threads (default: 10) should not be a problem.

This tool/plugin, is currently in development, please be kind enough to open a new issue (if found) in the issues tab.

## Requirements and Installation

Follow the below steps to install the tool, and run it through ```govaster --help```
- ```git clone https://github.com/belikeParamjot/govaster```
- ```cd govaster```
- ```pip3 install -r requirements.txt```
- ```sudo cp govaster.py /usr/bin/govaster```
- ```sudo chmod +x /usr/bin/govaster```
- ```cd ..```
- ```sudo rm -r govaster/```

OR

You could just simply clone the repo install the packages from requirements.txt and then run the tool via ```./govaster.py --help```.

## Usage and Features

It's nothing new, the only added feature for you to look at is... Recursive bruteforcing. So, go on, try using this tool on your own, it's exact same as gobuster... Just use ```-R``` flag, to see the tool go in recursion.
