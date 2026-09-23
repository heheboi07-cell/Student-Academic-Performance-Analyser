"""
student.py - Student Management: Domain entity and student registry operations.
"""
from typing import Dict, List, Optional
from storage import StorageManager

class Student:
    def __init__(self, roll_no: str, name: str, semester: int, section: str, attendance: float = 0.0):
        self.roll_no = roll_no.strip().upper()
        self.name = name.strip()
        self.semester = int(semester)
        self.section = section.strip().upper()
        self.attendance = float(attendance)
        self.marks: Dict[str, float] = {}

    def to_dict(self) -> dict:
        return {
            "roll_no": self.roll_no,
            "name": self.name,
            "semester": self.semester,
            "section": self.section,
            "attendance": self.attendance,
            "marks": self.marks
        }

    @classmethod
    def from_dict(cls, data: dict):
        student = cls(
            roll_no=data["roll_no"],
            name=data["name"],
            semester=data["semester"],
            section=data.get("section", "A"),
            attendance=data.get("attendance", 0.0)
        )
        student.marks = data.get("marks", {})
        return student


class StudentManager:
    def __init__(self, storage: StorageManager):
        self.storage = storage
        self._students: Dict[str, Student] = {}
        self.load_cache()

    def load_cache(self):
        raw = self.storage.load_all()
        self._students = {r_no: Student.from_dict(d) for r_no, d in raw.items()}

    def save_cache(self):
        raw = {r_no: s.to_dict() for r_no, s in self._students.items()}
        self.storage.save_all(raw)

    def add_student(self, student: Student) -> bool:
        if student.roll_no in self._students:
            return False
        self._students[student.roll_no] = student
        self.save_cache()
        return True

    def get_student(self, roll_no: str) -> Optional[Student]:
        return self._students.get(roll_no.strip().upper())

    def get_all_students(self) -> List[Student]:
        return list(self._students.values())

    def update_student(self, roll_no: str, name: str = None, sem: int = None, section: str = None) -> bool:
        student = self.get_student(roll_no)
        if not student:
            return False
        if name:
            student.name = name.strip()
        if sem is not None:
            student.semester = int(sem)
        if section:
            student.section = section.strip().upper()
        self.save_cache()
        return True

    def delete_student(self, roll_no: str) -> bool:
        r_no = roll_no.strip().upper()
        if r_no in self._students:
            del self._students[r_no]
            self.save_cache()
            return True
        return False

    def search_students(self, query: str) -> List[Student]:
        q = query.strip().lower()
        return [
            s for s in self._students.values()
            if q in s.roll_no.lower() or q in s.name.lower() or q in s.section.lower()
        ]