"""
analysis.py - Performance Analysis: Calculates averages, letter grades, insights & suggestions.
"""
from typing import Optional, Dict
from student import Student

class PerformanceAnalyzer:
    @staticmethod
    def get_grade(marks: float) -> str:
        if marks >= 90.0:
            return "A+"
        elif marks >= 80.0:
            return "A"
        elif marks >= 70.0:
            return "B+"
        elif marks >= 60.0:
            return "B"
        elif marks >= 50.0:
            return "C"
        elif marks >= 40.0:
            return "D"
        else:
            return "F"

    @classmethod
    def get_performance_status(cls, average: float) -> str:
        if average >= 85.0:
            return "OUTSTANDING"
        elif average >= 75.0:
            return "GOOD"
        elif average >= 60.0:
            return "SATISFACTORY"
        elif average >= 50.0:
            return "AVERAGE"
        else:
            return "NEEDS IMPROVEMENT"

    @classmethod
    def analyze_student(cls, student: Student) -> Optional[Dict]:
        if not student.marks:
            return None

        marks_dict = student.marks
        total = sum(marks_dict.values())
        avg = round(total / len(marks_dict), 1)
        overall_grade = cls.get_grade(avg)
        status = cls.get_performance_status(avg)

        # Build subject grade mapping
        breakdown = {sub: (mark, cls.get_grade(mark)) for sub, mark in marks_dict.items()}

        highest_sub = max(marks_dict, key=marks_dict.get)
        lowest_sub = min(marks_dict, key=marks_dict.get)

        strong = [sub for sub, mark in marks_dict.items() if mark >= 80.0]
        attention = [sub for sub, mark in marks_dict.items() if mark < 80.0]

        if attention:
            focus_subs = " and ".join(attention[:2])
            suggestion = f"Focus more on {focus_subs}\nto improve overall performance."
        else:
            suggestion = "Excellent balance across all subjects! Keep up the good work."

        return {
            "breakdown": breakdown,
            "average": avg,
            "overall_grade": overall_grade,
            "highest_sub": highest_sub,
            "highest_mark": marks_dict[highest_sub],
            "lowest_sub": lowest_sub,
            "lowest_mark": marks_dict[lowest_sub],
            "strong": strong,
            "attention": attention,
            "attendance": student.attendance,
            "status": status,
            "suggestion": suggestion
        }