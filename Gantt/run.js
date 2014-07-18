
function make_x_axis() {        
    return d3.svg.axis()
        .scale(x)
         .orient("bottom")
         .ticks(5)
}

function make_y_axis() {        
    return d3.svg.axis()
        .scale(y)
        .orient("left")
        .ticks(5)
}
//Add Task Start Time and Date, End Time and Date, Name, and Status
//Sample Below
var tasks = [

//Task 1
{"startDate":new Date("Thurs Jun 12 13:54:00 EST 2014"),"endDate":new Date("Thurs Jun 12 13:58:00 EST 2014"),"taskName":"Task 1","status":"Wait"},

//Add Room Movement tasks for CSS
];
var taskStatus = {
	"O" : "O-Flag",
	"A" : "A-Flag",
	"P" : "P-Flag",
	"D" : "D-Flag",
	"R" : "R-Flag",
	"C" : "C-Flag",
	"S"	: "S-Flag",
	"X" : "X-Flag",
    "Exam" : "exam",
    "Con" : "Consult",
    "MM" : "Mammography",
    "Wait" : "Waiting",
    "Inf" : "Infusion",
    "DR" : "DR",
    "US" : "US",
    "UBX" : "UBX",
    "Stereo" : "Stereo",
    "Intake" : "Intake",
    "I" : "I-Extra"
    
};

//Add Tasks for Y-Axis of Gantt
var taskNames = [ "Task 1
];

tasks.sort(function(a, b) {
    return a.endDate - b.endDate;
});
var maxDate = tasks[tasks.length - 1].endDate;
tasks.sort(function(a, b) {
    return a.startDate - b.startDate;
});
var minDate = tasks[0].startDate;

var format = "%H:%M";


var gantt = d3.gantt().taskTypes(taskNames).taskStatus(taskStatus).tickFormat(format);
gantt(tasks);