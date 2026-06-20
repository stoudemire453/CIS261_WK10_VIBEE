import os

FILE_NAME = "student_grades.txt"


class Student:
    def __init__(self, name: str, student_id: str, test1: float, test2: float, test3: float):
        self.name = name.strip()
        self.student_id = student_id.strip()
        self.test_scores = [test1, test2, test3]
        self.average = self.calculate_average()
        self.grade = self.calculate_grade()

    def calculate_average(self) -> float:
        return sum(self.test_scores) / len(self.test_scores)

    def calculate_grade(self) -> str:
        avg = self.average
        if avg >= 90:
            return "A"
        if avg >= 80:
            return "B"
        if avg >= 70:
            return "C"
        if avg >= 60:
            return "D"
        return "F"

    def to_record(self) -> str:
        return "|".join([
            self.name,
            self.student_id,
            f"{self.test_scores[0]:.2f}",
            f"{self.test_scores[1]:.2f}",
            f"{self.test_scores[2]:.2f}",
            f"{self.average:.2f}",
            self.grade,
        ])


def load_students(filename: str) -> list[Student]:
    students = []
    if not os.path.exists(filename):
        return students

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line in file:
                parts = line.strip().split("|")
                if len(parts) != 7:
                    continue

                name, student_id, test1, test2, test3, _, _ = parts
                try:
                    student = Student(
                        name,
                        student_id,
                        float(test1),
                        float(test2),
                        float(test3),
                    )
                    students.append(student)
                except ValueError:
                    continue
    except IOError as error:
        print(f"Error loading records from {filename}: {error}")
    return students


def save_students(filename: str, students: list[Student]) -> None:
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for student in students:
                file.write(student.to_record() + "\n")
    except IOError as error:
        print(f"Error saving records to {filename}: {error}")
    else:
        print(f"All student records were saved to {filename}.")


def format_student_row(student: Student) -> str:
    return (
        f"{student.name:20} | {student.student_id:10} | "
        f"{student.test_scores[0]:6.2f} | {student.test_scores[1]:6.2f} | {student.test_scores[2]:6.2f} | "
        f"{student.average:7.2f} | {student.grade}"
    )


def display_students(students: list[Student]) -> None:
    if not students:
        print("No student records available to display.")
        return

    print("\nStudent Records")
    print("=" * 90)
    print("Name                 | Student ID  | Test 1 | Test 2 | Test 3 | Average | Grade")
    print("-" * 90)
    for student in students:
        print(format_student_row(student))
    print("=" * 90)


def class_statistics(students: list[Student]) -> None:
    if not students:
        print("No student records available to calculate statistics.")
        return

    averages = [student.average for student in students]
    highest = max(averages)
    lowest = min(averages)
    class_avg = sum(averages) / len(averages)

    print("\nClass Statistics")
    print("-" * 30)
    print(f"Highest Average: {highest:.2f}")
    print(f"Lowest Average : {lowest:.2f}")
    print(f"Class Average  : {class_avg:.2f}")
    print("-" * 30)


def search_student(students: list[Student], search_name: str) -> None:
    found = [
        student for student in students
        if search_name.lower() in student.name.lower()
    ]

    if not found:
        print(f"No student found matching '{search_name}'.")
        return

    print(f"\nSearch results for '{search_name}':")
    print("-" * 90)
    print("Name                 | Student ID  | Test 1 | Test 2 | Test 3 | Average | Grade")
    print("-" * 90)
    for student in found:
        print(format_student_row(student))
    print("-" * 90)


def get_float_input(prompt: str) -> float:
    while True:
        value = input(prompt).strip()
        try:
            score = float(value)
            if 0 <= score <= 100:
                return score
            print("Please enter a score between 0 and 100.")
        except ValueError:
            print("Invalid number. Please enter a decimal or whole number.")


def add_student(students: list[Student]) -> None:
    print("\nAdd New Student Record")
    print("-" * 25)
    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be blank.")
        return

    student_id = input("Enter student ID: ").strip()
    if not student_id:
        print("Student ID cannot be blank.")
        return

    test1 = get_float_input("Enter Test 1 score: ")
    test2 = get_float_input("Enter Test 2 score: ")
    test3 = get_float_input("Enter Test 3 score: ")

    new_student = Student(name, student_id, test1, test2, test3)
    students.append(new_student)
    print(f"Student '{new_student.name}' added with average {new_student.average:.2f} and grade {new_student.grade}.")


def main_menu() -> None:
    students = load_students(FILE_NAME)
    if students:
        print(f"Loaded {len(students)} student record(s) from {FILE_NAME}.")
    else:
        print(f"No existing records found. Starting with an empty student list.")

    while True:
        print("\nStudent Grade Calculator")
        print("1. Add new student record")
        print("2. Display all students")
        print("3. Show class statistics")
        print("4. Search for student by name")
        print("5. Save student records")
        print("ESC. Exit program")
        choice = input("Choose an option: ").strip()

        if choice.lower() == "esc":
            save_students(FILE_NAME, students)
            print("Exiting program. Goodbye!")
            break

        if choice == "1":
            add_student(students)
            continue
        if choice == "2":
            display_students(students)
            continue
        if choice == "3":
            class_statistics(students)
            continue
        if choice == "4":
            name_search = input("Enter student name to search: ").strip()
            if name_search:
                search_student(students, name_search)
            else:
                print("Search term cannot be blank.")
            continue
        if choice == "5":
            save_students(FILE_NAME, students)
            continue

        print("Invalid option. Please select 1-5 or type ESC to quit.")


if __name__ == "__main__":
    main_menu()

