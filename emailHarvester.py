#!/usr/bin/python3

# Change the above line if python 3 is located somewhere else on your computer

# Christopher Paterno
# Professor Fonseca
# CSF 438
# 10 June 2018


# Script which runs both theharvester and metagoofil and returns 3 text documents containing:
# the emails found by both tools
# the emails found by theharvester only
# the emails found by metagoofil only

import sys
import subprocess
import bs4
import re

# returns 0 if input is valid and 1 if input is not
# takes in a list of arguments, and the number of valid parameters
def valid_input(argv, param_count):
	if len(argv) != param_count:
		return 1
	return 0

# function that calls the harvester tool
# takes in a domain name (passed as an argument) 
def harvest(domain):
	command = ['theharvester', '-d', domain, '-b', 'all',\
		'-f', 'h.html']
	# module method which allows python to execute bash commands
	subprocess.call(command)
	return

# function that calls the metagoofil tool
# takes in a domain name (passed as an argument)
def meta(domain):
	command = ['metagoofil', '-d', domain, '-t',\
		'pdf,doc,xls,ppt,odp,ods,docx,xlsx,pptx',\
		'-l', '100', '-n', '5', '-o', 'temp', '-f',\
		'm.html']
	# module method which allows python to execute bash commands
	subprocess.call(command)
	return

# function to write out results to a text file
# takes in a list of emails, a string representing the name of a file
# and a string representing the opening message
def write_to_file(emails, f_name, message):
	# using context manager to open file
	# since the file doesn't exist yet it will automatically be created 
	with open(f_name, "w") as output:
		output.write(message + "\n")
		for e in emails:
			output.write(e + "\n")
	return

# function that finds the emails produced by the tools and outputs the results to a text file
# then filters the emails into 3 categories: 
# emails found by both tools
# emails found by theharvester only
# emails found by metafoogil only
# takes in two strings representing html files
def results(theharvester, metagoofil):
	both = []
	harv = []
	metag = []
	# uses beautiful soup and perl like regex operations to find all emails in html file
	html_file = open(theharvester)
	# beautiful soup constructor parses and creates an html object
	# beautiful soup find all method returns a list of strings containing '@' (emails)
	hlist = bs4.BeautifulSoup(html_file, "lxml").findAll(text = re.compile('@'))
	html_file.close()
	
	# uses beautiful soup and perl like regex operations to find all emails in html file
	html_file = open(metagoofil)
	# beautiful soup constructor parses and creates an html object
	# beautiful soup find all method returns a list of strings containing '@' (emails)
	mlist = bs4.BeautifulSoup(html_file, "lxml").findAll(text = re.compile('@'))
	html_file.close()

	# below loops create lists of emails representing the three categories described above
	for email in hlist:
		if email in mlist and email not in both:
			both.append(email)
		else:
			harv.append(email)

	for email in mlist:
		if email in hlist and email not in both:
			both.append(email)
		else:
			metag.append(email)

	write_to_file(both, "both.txt", "Emails Found By Both Tools")
	write_to_file(harv, "theharvester_only.txt",\
		"Emails Found In The Harvester Only")
	write_to_file(metag, "metagoofil_only.txt",\
		"Emails Found In Metagoofil Only")
	return

# deletes other output files created by calling the two tools
# since this script only cares about the email output
# comment out below in main to keep the tool's output files
def clean_up():
	files = ['h.html', 'h.xml', 'stash.sqlite', 'm.html', 'temp']
	command = ['rm', '-f', '']
	for f in files:
		if f == 'temp':
			command[1] = '-rf'
		command[2] = f
		# module method which allows python to execute bash commands
		subprocess.call(command)
	return

# driver function
# takes in a list of arguments 
def main(argv):
	flag = valid_input(argv, 1)
	if flag:
		print("Usage: ./emailHarvester.py [domain]")
		print("Example: ./emailHarvester.py hackthissite.org")
		sys.exit(1)
	harvest(argv[0])
	meta(argv[0])
	results('h.html', 'm.html')
	clean_up()
	return

# alias the command line arguments to remove the script's name
# statement executes when program begins
if __name__ == "__main__":
	main(sys.argv[1:])
