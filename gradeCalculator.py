#---Globals-------------------------------------------------------------
studentGrades = {}

#---Functions-----------------------------------------------------------
##
# Sort Exam Grades and remove lowest.  Calculate final average with a weight of 33% for each exam.
##
def calculateFinalAverage(studentName):
    examGrades = sorted([float(examGrade) for examGrade in studentGrades[studentName][:-1]])[1:]
    finalAverage = (examGrades[0] * .33) + (examGrades[1] * .33) + (float(studentGrades[studentName][3]) * .33) + 1
    return str(finalAverage)
    
##
# Display Student information and final grade on screen
##
def viewGrades():
    print "\n\n         Student         |  Exam 1  |  Exam 2  |  Exam 3  |  Final Exam  |  Final Average"
    print "------------------------------------------------------------------------------------------"
    for studentName in sorted(studentGrades.keys()):
        print studentName + (' ' * (25 - len(studentName))) + "|",
        examCount = 1
        for studentGrade in studentGrades[studentName]:
            numberSpaces = (10 - len(studentGrade)) / 2 if examCount != 4 else (14 - len(studentGrade)) / 2
            print (' ' * (numberSpaces if len(studentGrade) == 3 else numberSpaces - 1)) + studentGrade + (' ' * (numberSpaces if len(studentGrade) != 1 else numberSpaces + 1)) + "|",
            examCount += 1
        finalAverage = calculateFinalAverage(studentName)
        print (' ' * ((15 - len(finalAverage)) / 2)) + '\033[1;' + ('32m' if float(finalAverage) >= 65.0 else '31m') + finalAverage + '\033[0m'
    print "------------------------------------------------------------------------------------------\n\n"

print "Grade Calculator\n"
while 1:
    studentName = raw_input("Enter Student Name: ")
    if studentName == "":
        viewGrades()
        break
    while 1:
        studentGrade = raw_input("Enter Grades (1,2,3,F): ")
        if len(studentGrade.split(',')) == 4:
            validGrades = 1
            for singleGrade in studentGrade.split(','):
                if int(singleGrade) not in range(101):
                    validGrades = 0
            if validGrades:
                break
    studentGrades[studentName] = [singleGrade for singleGrade in studentGrade.split(',')]