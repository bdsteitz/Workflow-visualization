import sqlite3
import json

#first run boolean
first_run = True

#create the database
db = sqlite3.connect(':memory:')

#create/open sqlite file
try:
	db = sqlite3.connect('datasort')#TODO:change this to whatever you want the file to be named
except Exception as e:
	print "Error connecting to db. MSG: "+str(e)
	print "\nExiting..."
	exit(0)
	
#get a db cursor
cursor = db.cursor()

cursor.execute('''DROP TABLE IF EXISTS WBOHO''')
cursor.execute('''DROP TABLE IF EXISTS WBOHO_CLEANED''')

#define input filename
in_file = "jul28_data.txt" #TODO:change this to whatever you named the input file

#open the file stream
f = open(in_file, 'r')

#instantiate line as something not blank
line = "start"

#print start confirmation message
print "***\nWorking...\n***"

#iterate over each line of the file ensuring that the line isn't blank 
#(indicates EOF)
while line != "":
	#actually get the line from the file and set it to a variable
	line = f.readline()
	
	#handle case where line is blank. (breaks the while loop and goes to end)
	if line == "":
		break

	#splits the line of text that was read in delimited by a pipe
	#returns an array with each index being a value that was contained within
	#the pipes (ex. line_array[0] is appt_date in the example you gave me.
	#...line_array[2] is MRN). To access this data, you will just query it
	#like any other array
	line_elements = line.split("|")
	
	#remove the new line character from the end of the last index
	if line_elements[-1][-1] == "\n":
		line_elements[-1] = line_elements[-1][:-1]
		
	#remove the return character from the end of the last index
	if line_elements[-1][-1] == "\r":
		line_elements[-1] = line_elements[-1][:-1]

	#set element information from data retrieved in line_elements
	appt_date = line_elements[0]
	column_id = line_elements[1]
	mrn = line_elements[2]
	time_stamp_of_action = line_elements[3]
	action_code = line_elements[4]
	display_text = line_elements[5]
	addl_text = line_elements[6]
	appt_idno = line_elements[7]
	racfid = line_elements[8]
	full_name = line_elements[9]
	
	if first_run == True:
		#create the table
		cursor.execute('''CREATE TABLE WBOHO(entry_id INTEGER PRIMARY KEY, appt_date TEXT,column_id TEXT,mrn TEXT,time_stamp_of_action TEXT,action_code TEXT,display_text TEXT,addl_text TEXT,appt_idno TEXT,racfid TEXT,full_name TEXT)''')
		cursor.execute('''CREATE TABLE WBOHO_CLEANED(entry_id INTEGER PRIMARY KEY, enter_time TEXT, exit_time TEXT, mrn TEXT, room TEXT)''')

		#commit changes
		db.commit()
			
		first_run = False
	else:
		#insert the current line into the table
		cursor.execute('''
			INSERT INTO WBOHO(appt_date,column_id, mrn, time_stamp_of_action, action_code, display_text, addl_text, appt_idno, racfid, full_name)
			VALUES(?,?,?,?,?,?,?,?,?,?)
		''', (appt_date,column_id, mrn, time_stamp_of_action, action_code, display_text, addl_text, appt_idno, racfid, full_name))
		
		#commit changes
		db.commit()
		

#get information
cursor.execute('''
	SELECT a.time_stamp_of_action AS enter_time, b.time_stamp_of_action AS exit_time, a.mrn AS id, b.mrn, a.action_code, b.action_code, SUBSTR(a.display_text, 9) AS rooms, SUBSTR(b.display_text, 9), a.addl_text, a.appt_idno, b.appt_idno, a.appt_date
	FROM WBOHO AS a, WBOHO AS b
	WHERE a.action_code = "I"
	AND b.action_code = "O"
	AND a.mrn = b.mrn
	AND SUBSTR(a.display_text, 9) = SUBSTR(b.display_text, 9)
	AND datetime(a.time_stamp_of_action) < datetime(b.time_stamp_of_action)
	AND a.addl_text = "Williamson Walk-In"
	ORDER BY a.mrn, a.time_stamp_of_action, a.display_text, a.action_code ASC
''')

insert_rows = cursor.fetchall()
for row in insert_rows:
	enter_time = row[0]
	exit_time = row[1]
	mrn = row[2]
	room = row[6]
	
	#insert the current line into the table
	cursor.execute('''
		INSERT INTO WBOHO_CLEANED(enter_time, exit_time, mrn, room)
		VALUES(?,?,?,?)
	''', (enter_time, exit_time, mrn, room))
	
	#commit changes
	db.commit()
	
output_rows = cursor.execute("SELECT enter_time, exit_time, mrn, room FROM WBOHO_CLEANED")
for row in output_rows:
	print row
	

	
#close the filestream
f.close()

#close the db connection
db.close()

#print ending confirmation message
print "***\nFinished\n***"




