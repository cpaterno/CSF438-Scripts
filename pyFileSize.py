#!/usr/bin/python3

# Change the above line if python3 is located somewhere else on your computer

# Christopher Paterno
# Professor Fonseca
# CSF 438
# June 2nd, 2018
import sys
import os

# returns an integer representing validity of input
# takes in list of arguments and valid amount
def valid_input(argv, param_count):
	# true if wrong amount of arguments given
	if len(argv) != param_count:
		return 1
	# true if directory is invalid
	elif not os.path.isdir(argv[0]):
		return -1
	return 0

# returns an integer representing the size of a file
# takes in directory and file
def file_size(d, f):
	# try and except used to catch OSError instead of crashing script
	try:
		return os.path.getsize(os.path.join(d, f))
	except OSError:
		return 0

# walk through directory and subdirectory to add up file sizes
# write output to specified file, returns None
# takes in list of arguments
def walk_through(argv):
	total = subtotal = length = 0
	out_str = ""
	# open and close file using context manager
	with open(argv[1], "w") as output:
		# loop through directory and subdirectory
		# list of subdirectories returned from os.walk is not needed
		for cur_dir, _, files in os.walk(argv[0]):
			# loop through files w. counter in current directory
			for i, content in enumerate(files):
				subtotal += file_size(cur_dir, content)
				out_str = "File " + str(i + 1) + ": " \
					+ content + "\n"
				output.write(out_str)
				# length of longest line written thus far
				length = max((len(out_str) - 1), length)
			total += subtotal
			output.write("Running Total: " + str(total) + "\n")
			output.write("Directory Size: " + str(subtotal)  + "\n")
			out_str = "Path: " + cur_dir + "\n"
			output.write(out_str)
			length = max(length, (len(out_str) - 1))
			# divider line for easier to read output
			output.write("-" * length  + "\n")
			# reset subtotal and length
			subtotal = length = 0
		output.write("Total Size of All Directories: " + str(total) \
			+ "\n")
	return
# driver, returns None
# takes list of arguments
def main(argv):
	flag = valid_input(argv, 2)
	if flag == 1:
		print("Usage: ./pyFileSize.py [directory] [output]")
		print("Example: ./pyFileSize.py /home output.txt")
		sys.exit(1)
	elif flag == -1:
		print("Directory Not Found")
		sys.exit(1)
	walk_through(argv)
	return

# if statement that executes when script is run
# used to filter out program name from command line arguments
if __name__ == "__main__":
	main(sys.argv[1:])
