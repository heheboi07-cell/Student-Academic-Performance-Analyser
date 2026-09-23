"""
test_project.py - Unit test suite covering Student, Academic, Analysis, and Reporting.
"""
import sys
import unittest
from pathlib import Path

# Add project root to sys.path so modules import seamlessly
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from student import Student
from analysis import PerformanceAnalyzer
from reports import ReportGenerator

class TestAcademicPerformanceAnalyzer(unittest.TestCase):
    def setUp(self):
        self.student = Student("26BCE12345", "Mohit Dongare", 1, "C", attendance=87.0)
        self.student.marks = {
            "Mathematics": 82.0,
            "Python": 91.0,
            "Physics": 74.0,
            "Electronics": 78.0,
            "English": 86.0
        }

    def test_analysis_metrics(self):
        analysis = PerformanceAnalyzer.analyze_student(self.student)
        self.assertIsNotNone(analysis)
        self.assertEqual(analysis["average"], 82.2)
        self.assertEqual(analysis["overall_grade"], "A")
        self.assertEqual(analysis["highest_sub"], "Python")
        self.assertEqual(analysis["lowest_sub"], "Physics")
        self.assertEqual(analysis["status"], "GOOD")

    def test_grade_boundaries(self):
        self.assertEqual(PerformanceAnalyzer.get_grade(95), "A+")
        self.assertEqual(PerformanceAnalyzer.get_grade(85), "A")
        self.assertEqual(PerformanceAnalyzer.get_grade(75), "B+")
        self.assertEqual(PerformanceAnalyzer.get_grade(65), "B")
        self.assertEqual(PerformanceAnalyzer.get_grade(35), "F")

    def test_strong_and_attention_categories(self):
        analysis = PerformanceAnalyzer.analyze_student(self.student)
        self.assertIn("Python", analysis["strong"])
        self.assertIn("English", analysis["strong"])
        self.assertIn("Physics", analysis["attention"])
        self.assertIn("Electronics", analysis["attention"])

    def test_report_generation(self):
        reporter = ReportGenerator()
        text = reporter.generate_detailed_report(self.student)
        self.assertIn("STUDENT ACADEMIC REPORT", text)
        self.assertIn("Mohit Dongare", text)
        self.assertIn("82.2%", text)

if __name__ == "__main__":
    unittest.main()