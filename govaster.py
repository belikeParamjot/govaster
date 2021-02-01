#!/usr/bin/python3

### Run gobuster recursively. Same flags and usage, just... recursive to each directory found.

import os
import sys
import signal
import subprocess
import time
from threading import *
from optparse import OptionParser, Values
from termcolor import colored

def optionparser(mode):
	
	global flags

	parser = OptionParser()
	parser.add_option("-z","--noprogress", dest="noprogress", action="store_false")
	parser.add_option("-o","--output", dest='output', metavar='')
	parser.add_option("-q", "--quiet", dest='quiet', action='store_false')
	parser.add_option("-t", "--threads", dest='threads')
	parser.add_option("-v", "--verbose", dest='verbose', action='store_false')
	parser.add_option("-w", "--wordlist", dest='wordlist', metavar='FILE')
	parser.add_option("-R", "--recursive", dest='recursive', action='store_false')

	
	if mode == 'dir':
		parser.add_option("-u", "--url", dest="url")
		parser.add_option("-c", "--cookies", dest="cookies")
		parser.add_option("-e", "--expanded", dest="expanded", action="store_false")
		parser.add_option("-r", "--followredirect", dest="followredirect", action="store_false")
		parser.add_option("-x", "--extensions", dest="extensions")
		parser.add_option("-H", "--headers", dest="headers")
		parser.add_option("-l", "--includelength", dest="includelength", action="store_false") 
		parser.add_option("-k", "--insecuressl", dest="insecuressl", action="store_false") 
		parser.add_option("-n", "--nostatus", dest="nostatus", action="store_false") 
		parser.add_option("-P", "--password", dest="password")
		parser.add_option("-p", "--proxy", dest="proxy")
		parser.add_option("-s", "--statuscodes", dest="statuscodes")
		parser.add_option("-b", "--statuscodesblacklist", dest="statuscodesblacklist")
		parser.add_option("-a", "--useragent", dest="useragent")
		parser.add_option("-U", "--username", dest="username")
		parser.add_option("--timeout", dest="timeout")
		parser.add_option("--wildcard", dest="wildcard", action="store_false")
	
	if mode == 'dns':
		parser.add_option("-d", "--domain", dest="domain")
		parser.add_option("-r", "--resolver", dest="resolver")
		parser.add_option("-c", "--showcname", dest="showcname", action="store_false")
		parser.add_option("-i", "--showips", dest="showips", action="store_false")
		parser.add_option("--timeout", dest="timeout")
		parser.add_option("--wildcard", dest="wildcard", action="store_false")

	if mode == 'vhost':
		parser.add_option("-u", "--url", dest="url")
		parser.add_option("-c", "--cookies", dest="cookies")
		parser.add_option("-r", "--followredirect", dest="followredirect", action="store_false")
		parser.add_option("-H", "--headers", dest="headers")
		parser.add_option("-k", "--insecuressl", dest="insecuressl")
		parser.add_option("-P", "--password", dest="password")
		parser.add_option("-p", "--proxy", dest="proxy")
		parser.add_option("-a", "--useragent", dest="useragent")
		parser.add_option("-U", "--username", dest="username")
		parser.add_option("--timeout", dest="timeout")

	set_opts = Values()
	(options, args) = parser.parse_args(values=set_opts)
	options = Values(parser.get_default_values().__dict__)
	options._update_careful(set_opts.__dict__)
	flags = set_opts.__dict__

def formatter(mode):

	cmd = ''
	if mode == 'dir':
		cmd += "gobuster dir "
	elif mode == 'dns':
		cmd += "gobuster dns "
	elif mode == 'vhost':
		cmd += "gobuster vhost "

	for i,j in flags.items():
		if i == 'recursive':
			continue
		if j is False:
			cmd += "--" + i + " "
			continue

		cmd += "--" + i + " " + j + " "
	return cmd

# GOING RECURSIVE ON DIRECTORY

def recursedir(url, directory):
	 
	if 'extensions' in flags.keys():
		cmd = "gobuster dir " + "--url " + url + " --wordlist " + flags.get('wordlist') + " -x " + flags.get('extensions') + " --quiet -t 30 -e"
	else: # Default Arguments for better results
		cmd = "gobuster dir " + "--url " + url + " --wordlist " + flags.get('wordlist') + " -x php,txt,html,css,js,aspx,xml --quiet -t 30 -e"

	temp = ''

	process = subprocess.Popen("exec " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
	
	while process.poll() is None:
		output = process.stdout.readline()
		if output:
			print(colored('%s', 'green') %output.strip().decode('utf-8'))
		
		if 'expanded' in flags.keys():
			if 'http' in output.decode('utf-8'):
				directory = output.decode('utf-8').split(' ')[0].split('/')[-1]
		else:
			directory = output.decode('utf-8').split(' ')[0].split('/')[-1]
		
		if not directory == temp:
			temp = directory
			url += directory
			t = Thread(target=recursedir, args=(url, directory))
			t.start()
		else:
			continue

def recursedns(domain, subdomain):
	
	cmd = "gobuster dns -d " + domain + " -w " + flags.get('wordlist') + ' --quiet -t 30'
	temp = ''

	process = subprocess.Popen("exec " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
	
	while process.poll() is None:
		output = process.stdout.readline()
		if output:
			print(colored('%s', 'green') %output.strip().decode('utf-8'))
		
		if 'Found' in output.decode('utf-8'):
			subdomain = output.decode('utf-8').split(' ')[1].split('.')[0]
		
		if not subdomain == temp:
			temp = subdomain
			domain = subdomain + "." + domain
			t = Thread(target=recursedns, args=(domain, subdomain))
			t.start()
		else:
			continue

def recursevhost(url, directory):
	pass
	# Yet to be implemented

def dirbrute(cmd):

	print(colored('\nCommand: %s \n', 'blue') %cmd)
	url = flags.get('url')
	
	directory = ''
	temp = ''
	
	try:
		process = subprocess.Popen("exec " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
		
		while process.poll() is None:
			output = process.stdout.readline()
			if output:
				print(output.strip().decode('utf-8'))

			if 'recursive' in flags.keys():
				if 'expanded' in flags.keys():
					if 'http' in output.decode('utf-8'):
						directory = output.decode('utf-8').split(' ')[0].split('/')[-1]
				else:
					directory = output.decode('utf-8').split(' ')[0].split('/')[-1]
	
				if not directory == temp:
					temp = directory
					url = flags.get('url').rstrip('/') + "/" + directory
					tx = Thread(target=recursedir, args=(url, directory))
					tx.setDaemon(True)
					tx.start()
				else:
					continue

	except (KeyboardInterrupt, SystemExit):
		print("[!] Keyboard Interrupt Detected. Terminating...")
		time.sleep(0.5)
		exit("Terminated")


def dnsbrute(cmd):

	print(colored('\nCommand: %s \n', 'blue') %cmd)
	domain = flags.get('domain')
	
	subdomain = ''
	temp = ''
	
	try:
		process = subprocess.Popen("exec " + cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=os.setsid)
		
		while process.poll() is None:
			output = process.stdout.readline()
			if output:
				print(output.strip().decode('utf-8'))

			if 'recursive' in flags.keys():
				if 'Found' in output.decode('utf-8'):
					subdomain = output.decode('utf-8').split(' ')[1].split('.')[0]
			
				if not subdomain == temp:
					temp = subdomain
					domain = subdomain + '.' + flags.get('domain').rstrip('/')
					tx = Thread(target=recursedns, args=(domain, subdomain))
					tx.setDaemon(True)
					tx.start()
				else:
					continue

	except (KeyboardInterrupt, SystemExit):
		print("[!] Keyboard Interrupt Detected. Terminating...")
		time.sleep(0.5)
		exit("Terminated")

def vhostbrute(cmd):
	# Yet to be implemented
	print(colored('\nCommand: %s \n', 'blue') %cmd)
	os.system(cmd)

def main():
	global bust_mode
	bust_mode = sys.argv[1]
	if bust_mode == "dir":
		optionparser(bust_mode);
		cmd = formatter(bust_mode);
		dirbrute(cmd);
	elif bust_mode == "dns":
		optionparser(bust_mode);
		cmd = formatter(bust_mode);
		dnsbrute(cmd);
	elif bust_mode == "vhost":
		optionparser(bust_mode);
		cmd = formatter(bust_mode);
		vhostbrute(cmd);
	elif bust_mode == "help":
		try:
			os.system("gobuster help " + sys.argv[2])
		except:
			os.system("gobuster help")
	else:
		print("Invalid mode; Choose from dir, dns, vhost, or use help to get help")


if __name__ == "__main__":
	main()
