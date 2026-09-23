"""
academic.py - Academic Records: Manages marks entry, subjects, and attendance.
"""
from student import StudentManager

class AcademicManager:
    def __init__(self, student_manager: StudentManager):
        self.students = student_manager

    def record_mark(self, roll_no: str, subject: str, marks: float) -> bool:
        student = self.students.get_student(roll_no)
        if not student:
            return False
        if not (0.0 <= marks <= 100.0):
            raise ValueError("Marks must be between 0 and 100.")
        student.marks[subject.strip().title()] = round(float(marks), 1)
        self.students.save_cache()
        return True

    def update_attendance(self, roll_no: str, attendance: float) -> bool:
        student = self.students.get_student(roll_no)
        if not student:
            return False
        if not (0.0 <= attendance <= 100.0):
            raise ValueError("Attendance must be between 0 and 100%.")
        student.attendance = round(float(attendance), 1)
        self.students.save_cache()
        return True

    def get_student_marks(self, roll_no: str) -> dict:
        student = self.students.get_student(roll_no)
        return student.marks if student else {}