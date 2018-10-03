#!/bin/bash

# Christopher Paterno
# Professor Fonseca
# CSF 438
# June 2nd, 2018

# if invalid usage, teach users how to use script
if [ "$1" == "" ] || [ "$2" == "" ]
then
	echo "Usage: ./bashDirContent.sh [directory] [outputFile]"
	echo "Example: ./bashDirContent.sh /home output.txt"
else
	# store current working directory
	oldDir=$(pwd)
	# move subshell into the specified directory
	cd $1
	# sed removes first line
	# awk takes permissions, file size, and file name columns
	# and prints it with spaces and newline
	# column converts awk's output into neat table,
	# deliminated by spaces
	# finally output the result to specified file in the user's
	# current directory
	ls -l | sed "1d" | awk '{printf "%s %d %s\n", $1, $5, $9}' \
	| column -t > $oldDir/$2
fi
