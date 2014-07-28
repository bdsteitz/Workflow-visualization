#
#
#	script to convert a csv file containing multiple lines of the following
#	start_date , end_date , mrn , status
#	into javascript appropriate for Gantt visualizations
#
#

import sys

if len(sys.argv) > 1:
	print "*"*50
	print "        Invalid options. Common usage below: "
	print ""
	print " python csvTOjs.py"
	print ""
	print "*"*50
	exit(0)



#
# global vars
#

first_run = True

#TODO:replace filepath with correct one for your csv file
#input file in format input_time, output_time, MRN, room \n
in_filename = "movement.csv"
f = open(in_filename, 'r')

out_filename = "output.js"
g = open(out_filename, 'w')

#mrn check variables
old_mrn = ""
current_patient_number = 0


#
#function to get and return the next line in an array
#
def getNextLine():
	global first_run
	dirty_line = ""
	clean_line = []
	
	#read in each line
	if first_run == True:
		first_run = False
		f.readline()
		return "firstrun"
	else:
		dirty_line = f.readline()

		#check for end of file
		if dirty_line == '':
			return "eof"
		
		#split the string into an array named clean_line delimited by comma 
		clean_line = dirty_line.split(",")
		return clean_line

#
#	functions to format the raw csv data into their respective formats
#
def formatStartDate(raw_start_date):
	return '"startDate":new Date("Thurs Jun 12 '+raw_start_date+' EST 2014")'

def formatEndDate(raw_end_date):
	return '"endDate":new Date("Thurs Jun 12 '+raw_end_date+' EST 2014")'

def formatPatientNumber(patient_number):
	return '"taskName":"'+patient_number+'"'

def formatStatus(raw_status):
	return '"status":"'+raw_status+'"'

#
# function to convert mrn into Patient #
#
def checkMRN(current_mrn):
	global old_mrn
	global current_patient_number
	patient_number = ""
	
	#if its the first run, set old_mrn to current_mrn
	if old_mrn == "":
		old_mrn=current_mrn
	
	#case where mrn has not changed
	if current_mrn == old_mrn:
		patient_number = "Patient "+str(current_patient_number)
		
	#case where mrn has changed
	else:
		#update global current patient number and mrn
		current_patient_number+=1 
		old_mrn = current_mrn
		
		patient_number = "Patient "+str(current_patient_number)
		
	return patient_number

#
# function to convert room into status
#
def changeRoomToStatus(room):
	if room[0] == ' ':
		room = room[1:]
	if room[-1] == "\n":
		room = room[:-1]

	status_dict = {
	'BR-WR':'Wait', 
	'LabWR':'Wait', 
	'TVWR':'Wait', 
	'InfWR':'Wait', 
	'Lunch':'Wait', 
	'IR':'Intake', 
	'DR':'DR',
	'A515':'Exam',
	'A516':'Exam',
	'A517':'Exam',
	'B518':'Exam',
	'B519':'Exam',
	'B520':'Exam',
	'B521':'Exam',
	'B522':'Exam',
	'B523':'Exam',
	'BD09':'Exam',
	'BXDR':'Exam',
	'C524':'Exam',
	'C525':'Exam',
	'C526':'Exam',
	'C527':'Exam',
	'C528':'Exam',
	'C529':'Exam',
	'C530':'Exam',
	'Con1':'Con',
	'Con2':'Con',
	'Con3':'Con',
	'Con4':'Con',
	'MM05':'MM',
	'MM42':'MM',
	'MM44':'MM',
	'MM46':'MM',
	'MM07':'MM',
	'MM43':'MM',
	'I-1':'Inf',
	'I-2':'Inf',
	'I-3':'Inf',
	'I-4':'Inf',
	'I-5':'Inf',
	'I-6':'Inf',
	'I-7':'Inf',
	'I-8':'Inf',
	'I-9':'Inf',
	'I-10':'Inf',
	'I-11':'Inf',
	'I-12':'Inf',
	'I-13':'Inf',
	'I-14':'Inf',
	'I-15':'Inf',
	'I-16':'Inf',
	'US-45':'US',
	'US45':'US',
	'US43':'US',
	'UBX-2':'UBX',
	'USBX':'UBX',
	'Stereo':'Stereo',
	'IR':'Intake',
	'IR47':'Intake',
	'I-Lab':'I',
	'RadCon':'Other',
	'MRI':'Other'
	}

	return_value = ""
	try:
		return_value = status_dict[room]
	except KeyError:
		return_value = ['INVALID ROOM', room]

	return return_value



def main():

	try:
		#print starting confirmation
		print "Working..."
		print_message = "Contents outputted to "+out_filename

		while True:
			#gets the next line of the file as an array with 4 entries
			#[0]=start_date [1]=end_date [2]=mrn [3]=status
			result = getNextLine()
			
			#check for end of file to break loop
			if result == "eof":
				break

			#check for first run
			if result != "firstrun":
				#calls to get correctly formatted results
				js_startdate = formatStartDate(result[0])
				js_enddate = formatEndDate(result[1])
				patient_number = checkMRN(result[2])
				js_patientnumber = formatPatientNumber(patient_number)
				status = changeRoomToStatus(result[3])

				if status[0] == 'INVALID ROOM':
					print "ERROR: Room "+status[1]+" is not defined. Update dictionary in 'changeRoomToStatus' to include it.\n"
					print_message = "All successful contents outputted to "+out_filename+". Not all entries may have been copied. See errors above"
				else:
					js_status = formatStatus(status)

					#writes out the final value to output file
					g.write("{"+js_startdate+","+js_enddate+","+js_patientnumber+","+js_status+"},")
					g.write("\n")
				
		#print confirmation
		print print_message
		
	except KeyboardInterrupt:
		print "Recieved quit signal. Exiting..."
		exit(0)

	#close file streams
	f.close()
	g.close()


if __name__ == "__main__":
    main()