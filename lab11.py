import matplotlib.pyplot as plt
import os

# Reading files:
# Create list with all student names
with open('data/students.txt') as student_file:
    students = []
    for line in student_file:
        students.append(line.strip())

# Create list with all assignment names and data
with open('data/assignments.txt') as assignment_file:
    assignments = []
    for line in assignment_file:
        assignments.append(line.strip())

# Turn assignments list into a dictionary
assignments_dict = {}
for i in range(0, len(assignments), 3):
    assignments_dict[assignments[i]] = assignments[i + 1], assignments[i + 2]

# Create large list with all submission information
submissions = []
path = "/Users/charlie.willis/PycharmProjects/COP3502C/lab11/grade_calculator/data/submissions"
for root, dirs, files in os.walk(path):
    for file in files:
        filepath = os.path.join(root, file)
        with open(filepath) as submission_file:
            for line in submission_file:
                submissions.append(line.strip())
# Separate each submission into its own list of values
for i in range (0, len(submissions)):
    submissions[i] = submissions[i].split('|')

# Get student_id; if Student does not exist, returns None
def get_student_id(student_name):
    student_id = []
    for item in students:
        if student_name in item:
            student = str(item)
            for char in range(0,3):
                student_id.append(student[char])
            student_id = ''.join(student_id)
            return student_id
    return None

# Uses student_id to get student's overall grade
def get_student_grade(student_id):
  total_points = 0
  for submission in submissions:
      if submission[0] == student_id:
        assignment_weight = get_assignment_weight(submission[1])
        assignment_grade = int(submission[2])
        total_points += (assignment_grade * assignment_weight)

  course_grade = round(total_points)
  return course_grade

# Get assignment_id; if Student does not exist, returns None
def get_assignment_id(assignment_name):
    if assignment_name in assignments_dict:
        assignment_id = assignments_dict[assignment_name][0]
        return assignment_id
    return None

# Get assignment weight; used for calculating student's course grade
def get_assignment_weight(assignment_id):
    for key in assignments_dict.keys():
        if assignments_dict[key][0] == assignment_id:
            assignment_weight = (int(assignments_dict[key][1])) / 1000
            return assignment_weight

# Uses assignment_id to get a list of all the assignment's scores; displays in a histogram
def get_assignment_stats(assignment_id):
    scores = []
    for submission in submissions:
        if submission[1] == assignment_id:
            scores.append(int(submission[2]))

    # Calculate minimum, maximum, and average score
    min_score = 100
    max_score = 0
    average = 0
    for score in scores:
        average += score
        if score < min_score:
            min_score = score
        elif score > max_score:
            max_score = score

    average = round(average/30)
    stats = f'Min: {min_score}%\nAvg: {average}%\nMax: {max_score}%'
    return stats

# Plots and shows graph based on inputted assignment
def get_assignment_graph(assignment_id):
    scores = []
    for submission in submissions:
        if submission[1] == assignment_id:
            scores.append(int(submission[2]))
    plt.xlim(48, 102)
    plt.hist(scores, bins=6)
    plt.show()

def main():
    # Print menu:
    print("1. Student grade\n"
          "2. Assignment statistics\n"
          "3. Assignment graph\n")
    selection = int(input("Enter your selection: "))

    if selection == 1: # Get student course grade
        student_name = str(input("What is the student's name: "))
        student_id = get_student_id(student_name)
        if student_id is None:
            print('Student not found')
        else:
            course_grade = get_student_grade(student_id)
            print(f'{course_grade}%')
    elif selection == 2: # Get assignment stats
        assignment_name = str(input("What is the assignment name: "))
        assignment_id = get_assignment_id(assignment_name)
        if assignment_id is None:
            print('Assignment not found')
        else:
            assignment_stats = get_assignment_stats(assignment_id)
            print(assignment_stats)
    elif selection == 3: # Get assignment histogram
        assignment_name = str(input("What is the assignment name: "))
        assignment_id = get_assignment_id(assignment_name)
        if assignment_id is None:
            print('Assignment not found')
        else:
            get_assignment_graph(assignment_id)

if __name__ == "__main__":
    main()

