#! /usr/bin/env python



import sys



#

#you will want to change these back to your files

#I had to change them for local testing

#

f=open('whiteboard.txt', 'r')

g=open('output_new.txt','w')



def main():

	print "SET sql_mode='NO_BACKSLASH_ESCAPES';"

	

	#set a boolean to represent the end of file (eof)

	eof = False

	

	#iterate while eof has not been reached

	while (eof == False):

		#read the f filestream in one line per iteration

		#the readline() function takes care of moving to the next line so there is no worries there

		line = f.readline()

		

		#check to see if you have reached the end of the file before continuing

		#if you have, break out of the while loop

		if line == "":

			eof = True

			

		#move on to the algorithm you created

		processLine(line)



def processLine(line):

	if (line.startswith("PRAGMA") or line.startswith("BEGIN TRANSACTION;") or line.startswith("COMMIT;") or line.startswith("DELETE FROM sqlite_sequence;") or line.startswith("INSERT INTO \"sqlite_sequence\"")):

		return

	line = line.replace("AUTOINCREMENT", "AUTO_INCREMENT")

	line = line.replace("DEFAULT 't'", "DEFAULT '1'")

	line = line.replace("DEFAULT 'f'", "DEFAULT '0'")

	line = line.replace(",'t'", ",'1'")

	line = line.replace(",'f'", ",'0'")

	in_string = False

	newLine = ''

	for c in line:

		if not in_string:

			if c == "'":

				in_string = True

			elif c == '"':

				newLine = newLine + '`'

				continue

		elif c == "'":

			in_string = False

		newLine = newLine + c

		

	print newLine

	

	#write newLine variable out to the g filestream line by line

	g.write(newLine)



if __name__ == "__main__":

    main()