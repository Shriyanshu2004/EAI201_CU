class StudentRecord:
    def __init__(self, student_name, math_score, science_score, english_score):
        self.student_name = student_name
        self.scores = {
            'Mathematics': math_score,
            'Science': science_score,
            'English': english_score
        }

    def calculate_total(self):
        return sum(self.scores.values())

    def __repr__(self):
        return f"Name: {self.student_name}, Scores: {self.scores}, Total: {self.calculate_total()}"

# Collect student names
students_list = [input(f"Enter student {i+1} name: ") for i in range(3)]

student_records = []

for student in students_list:
    print(f"\nProvide marks for {student}:")
    
    while True:
        try:
            math = int(input(f"Math marks (0-100): "))
            if 0 <= math <= 100:
                break
            print("Please enter marks between 0 and 100.")
        except ValueError:
            print("Invalid input, try again.")

    while True:
        try:
            science = int(input(f"Science marks (0-100): "))
            if 0 <= science <= 100:
                break
            print("Please enter marks between 0 and 100.")
        except ValueError:
            print("Invalid input, try again.")

    while True:
        try:
            english = int(input(f"English marks (0-100): "))
            if 0 <= english <= 100:
                break
            print("Please enter marks between 0 and 100.")
        except ValueError:
            print("Invalid input, try again.")

    student_records.append(StudentRecord(student, math, science, english))

# Display all student records
for record in student_records:
    print(record)

# Find the top student
top_student = max(student_records, key=lambda r: r.calculate_total())
print(f"\nTop scorer is {top_student.student_name} with total marks: {top_student.calculate_total()}")
