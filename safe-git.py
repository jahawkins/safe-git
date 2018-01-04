#!/usr/bin/python

import sys
from subprocess import call

keyListFile = "sensitive_keys.list"

originalGitCommand = "/usr/bin/git"

# Finds any instances of the words in the sensitive_keys.list file
def FindKeys(inputFile):
	keyFound = False

	keyList = [line.rstrip() for line in open(keyListFile)]


	with open(inputFile, 'r') as file:
		for line in file:
			for key in keyList:
				if (((key + "=") in line) or ((key + " =") in line)):
					print("WARNING: Line containing sensitive key word found: " + key)
					print(inputFile + ": " + line)
					keyFound = True 

	return keyFound



# Check the number of arguments. If 0, run the git --help command, otherwise check the first argument.

if (len(sys.argv) == 1):
	print("This is safe-git. It is a slightly modified version of git that intercepts the add command.")
	print("It will grep through the files provided add command for any key words found in sensitive_keys.list file.")
	print("If any are found it will display the lines it found and in which file and prompt you if you want to still continue.")
	print("Be safe and use git :)\n\n\n")
	call([originalGitCommand, "--help"])

else:

	if (sys.argv[1] == "add"):
		anyKeysFound = False
		for file in sys.argv[2:len(sys.argv)]:
			newKeyFound = FindKeys(file)
			anyKeysFound = anyKeysFound or newKeyFound

		if(anyKeysFound):

			stillAdd = raw_input("Do you want to continue and add the files as is (Y/n): ")

			# I try really hard to let the user type anything that would mean yes. They can still screw it up, but at this point, that is on them
			if (stillAdd == "Y" or stillAdd == "y" or stillAdd == "yes" or stillAdd == "YES" or stillAdd == "Yes"):
				systemCall = [originalGitCommand] + sys.argv[1:len(sys.argv)]
				call(systemCall)
			else:
				quit()

	else:
 
		systemCall = [originalGitCommand] + sys.argv[1:len(sys.argv)]
		call(systemCall)


