import sys
import argparse
from pathlib import Path

from storage import StorageManager
from student import Student, StudentManager
from academic import AcademicManager
from analysis import PerformanceAnalyzer
from reports import ReportGenerator

def pause():
    input("\nPress Enter to continue...")

class CLIApplication:
    def __init__(self):
        self.storage = StorageManager()
        self.students = StudentManager(self.storage)
        self.academics = AcademicManager(self.students)
        self.analyzer = PerformanceAnalyzer()
        self.reports = ReportGenerator()

    def run(self):
        while True:
            print("=" * 60)
            print("        STUDENT ACADEMIC PERFORMANCE ANALYZER")
            print("=" * 60)

            all_s = self.students.get_all_students()
            first_name = all_s[0].name.split()[0] if all_s else "Student"
            print(f"\nWelcome, {first_name}!\n")
            print("1. Student Management")
            print("2. Academic Records")
            print("3. Performance Analysis")
            print("4. Generate Report")
            print("5. Settings")
            print("6. Exit")

            choice = input("\nEnter your choice: ").strip()
            if choice == "1":
                self.menu_student_management()
            elif choice == "2":
                self.menu_academic_records()
            elif choice == "3":
                self.menu_performance_analysis()
            elif choice == "4":
                self.menu_generate_report()
            elif choice == "5":
                self.menu_settings()
            elif choice == "6":
                print("\nSaving data...")
                self.students.save_cache()
                print("✓ Data saved successfully.\n")
                print("Thank you for using\nStudent Academic Performance Analyzer!\n")
                print(f"Goodbye, {first_name}! 👋\n")
                break
            else:
                print("Invalid option. Please choose between 1 and 6.")

    # 1. Student Management
    def menu_student_management(self):
        while True:
            print("\n---------------- STUDENT MANAGEMENT ----------------\n")
            print("1. Add Student")
            print("2. View Students")
            print("3. Search Student")
            print("4. Update Student")
            print("5. Delete Student")
            print("6. Back")

            c = input("\nEnter your choice: ").strip()
            if c == "1":
                print("\n--------------- ADD NEW STUDENT ----------------\n")
                r_no = input("Enter Roll Number : ").strip()
                name = input("Enter Name        : ").strip()
                sem = input("Enter Semester    : ").strip()
                sec = input("Enter Section     : ").strip()

                try:
                    s = Student(r_no, name, int(sem), sec)
                    if self.students.add_student(s):
                        print("\n✓ Student added successfully!")
                    else:
                        print("\nError: Roll number already exists.")
                except ValueError:
                    print("\nError: Semester must be a valid number.")
                pause()

            elif c == "2":
                print("\n--------------- REGISTERED STUDENTS ----------------")
                print(f"{'Roll No':<16}{'Name':<24}{'Sem':<6}{'Section':<6}")
                print("-" * 52)
                for s in self.students.get_all_students():
                    print(f"{s.roll_no:<16}{s.name:<24}{s.semester:<6}{s.section:<6}")
                pause()

            elif c == "3":
                q = input("\nEnter search query: ").strip()
                res = self.students.search_students(q)
                print(f"\nFound {len(res)} student(s):")
                for s in res:
                    print(f"• {s.roll_no} - {s.name} (Sem {s.semester}, Sec {s.section})")
                pause()

            elif c == "4":
                r_no = input("\nEnter Roll Number to update: ").strip()
                s = self.students.get_student(r_no)
                if s:
                    name = input(f"New Name [{s.name}]: ").strip() or s.name
                    sec = input(f"New Section [{s.section}]: ").strip() or s.section
                    self.students.update_student(r_no, name=name, section=sec)
                    print("✓ Student updated successfully.")
                else:
                    print("Student not found.")
                pause()

            elif c == "5":
                r_no = input("\nEnter Roll Number to delete: ").strip()
                if self.students.delete_student(r_no):
                    print("✓ Student deleted.")
                else:
                    print("Student not found.")
                pause()

            elif c == "6":
                break

    # 2. Academic Records
    def menu_academic_records(self):
        while True:
            print("\n---------------- ACADEMIC RECORDS ----------------\n")
            print("1. Add Subject")
            print("2. Enter Marks")
            print("3. Update Marks")
            print("4. View Marks")
            print("5. Enter Attendance")
            print("6. Back")

            c = input("\nEnter your choice: ").strip()
            if c in ("1", "2", "3"):
                print("\n--------------- SELECT STUDENT ----------------\n")
                print(f"{'Roll No':<16}{'Name'}")
                print("-" * 32)
                for s in self.students.get_all_students():
                    print(f"{s.roll_no:<16}{s.name}")

                r_no = input("\nEnter Roll Number: ").strip()
                student = self.students.get_student(r_no)
                if not student:
                    print("Student not found.")
                    pause()
                    continue

                if c == "2":
                    print("\n--------------- ENTER MARKS ----------------\n")
                    default_subjects = ["Mathematics", "Python", "Physics", "Electronics", "English"]
                    for sub in default_subjects:
                        while True:
                            try:
                                m = float(input(f"Subject: {sub}\nMarks (0-100): "))
                                self.academics.record_mark(r_no, sub, m)
                                print()
                                break
                            except ValueError as e:
                                print(f"Error: {e}")
                    print("✓ Academic record updated!")
                    pause()

                elif c in ("1", "3"):
                    sub = input("Subject Name: ").strip()
                    try:
                        m = float(input("Marks (0-100): "))
                        self.academics.record_mark(r_no, sub, m)
                        print(f"✓ Recorded {sub}: {m}")
                    except ValueError as e:
                        print(f"Error: {e}")
                    pause()

            elif c == "4":
                r_no = input("\nEnter Roll Number: ").strip()
                m_dict = self.academics.get_student_marks(r_no)
                if m_dict:
                    print(f"\nMarks for {r_no}:")
                    for sub, m in m_dict.items():
                        print(f"• {sub:<15}: {m}")
                else:
                    print("No marks found.")
                pause()

            elif c == "5":
                r_no = input("\nEnter Roll Number: ").strip()
                try:
                    att = float(input("Enter Attendance Percentage (0-100): "))
                    if self.academics.update_attendance(r_no, att):
                        print("✓ Attendance updated successfully!")
                except ValueError as e:
                    print(f"Error: {e}")
                pause()

            elif c == "6":
                break

    # 3. Performance Analysis
    def menu_performance_analysis(self):
        r_no = input("\nEnter Roll Number: ").strip()
        student = self.students.get_student(r_no)
        if not student:
            print("Student not found.")
            pause()
            return

        analysis = self.analyzer.analyze_student(student)
        if not analysis:
            print("No marks recorded yet.")
            pause()
            return

        print("\n---------------- PERFORMANCE ANALYSIS ----------------\n")
        print(f"Student: {student.name}")
        print(f"Roll No : {student.roll_no}\n")
        print(f"{'Subject':<17}{'Marks':<12}{'Grade'}")
        print("-" * 38)
        for sub, (m, g) in analysis["breakdown"].items():
            m_str = str(int(m)) if m.is_integer() else str(m)
            print(f"{sub:<17}{m_str:<12}{g}")
        print("-" * 38)
        print(f"Average           : {analysis['average']}%")
        print(f"Overall Grade     : {analysis['overall_grade']}")

        print("\n--------------- PERFORMANCE INSIGHTS ----------------\n")
        print(f"Highest Subject       : {analysis['highest_sub']}")
        print(f"Lowest Subject        : {analysis['lowest_sub']}\n")
        print("Strong Subjects:")
        for sub in analysis["strong"]:
            print(f"✓ {sub}")
        print("\nSubjects Needing Attention:")
        for sub in analysis["attention"]:
            print(f"! {sub}")
        print(f"\nAttendance: {int(analysis['attendance'])}%\n")
        print(f"Overall Status: {analysis['status']}\n")
        print("Suggestion:")
        print(analysis["suggestion"])
        pause()

    # 4. Generate Report
    def menu_generate_report(self):
        while True:
            print("\n---------------- REPORT GENERATOR ----------------\n")
            print("1. Student Summary")
            print("2. Detailed Academic Report")
            print("3. Performance Analysis Report")
            print("4. Export Report")
            print("5. Back")

            c = input("\nEnter your choice: ").strip()
            if c in ("1", "2", "3", "4"):
                r_no = input("\nEnter Roll Number: ").strip()
                student = self.students.get_student(r_no)
                if not student:
                    print("Student not found.")
                    pause()
                    continue

                if c in ("1", "2", "3"):
                    report_text = self.reports.generate_detailed_report(student)
                    print("\n" + report_text)
                    export_choice = input("\nExport report? (Y/N): ").strip().upper()
                    if export_choice == "Y":
                        filepath = self.reports.export_to_file(student)
                        print("\n✓ Report saved successfully.")
                        print(f"File: {filepath}")
                    pause()

                elif c == "4":
                    filepath = self.reports.export_to_file(student)
                    print("\n✓ Report saved successfully.")
                    print(f"File: {filepath}")
                    pause()

            elif c == "5":
                break

    # 5. Settings
    def menu_settings(self):
        while True:
            print("\n---------------- SETTINGS ----------------\n")
            print("1. Change grading system")
            print("2. Backup student data")
            print("3. Restore student data")
            print("4. View application information")
            print("5. Back")

            c = input("\nEnter your choice: ").strip()
            if c == "1":
                print("\nActive Grading Scale: 10-Point Scale (A+ >=90, A >=80, B+ >=70, B >=60)")
                print("✓ Grading configuration active.")
                pause()
            elif c == "2":
                path = self.storage.backup_data()
                print(f"\n✓ Backup created successfully: {path}")
                pause()
            elif c == "3":
                backups = list(self.storage.backup_dir.glob("*.json"))
                if not backups:
                    print("\nNo backups available.")
                else:
                    print("\nAvailable Backups:")
                    for idx, b in enumerate(backups, 1):
                        print(f"{idx}. {b.name}")
                    try:
                        idx_choice = int(input("\nSelect backup number: ")) - 1
                        if 0 <= idx_choice < len(backups):
                            self.storage.restore_data(str(backups[idx_choice]))
                            self.students.load_cache()
                            print("✓ Data successfully restored.")
                    except ValueError:
                        print("Invalid selection.")
                pause()
            elif c == "4":
                print("\nStudent Academic Performance Analyzer")
                print("Architecture : 5-Module Modular Python Application")
                print("Runtime      : Python 3.9+ Standard Library")
                pause()
            elif c == "5":
                break

def main():
    parser = argparse.ArgumentParser(description="Student Academic Performance Analyzer")
    parser.add_argument("--report", type=str, metavar="ROLL_NO", help="Headless runner: print report for a student")
    parser.add_argument("--summary", action="store_true", help="Headless runner: display summary of all students")
    args = parser.parse_args()

    app = CLIApplication()

    # Headless / Non-interactive automated evaluation support
    if args.report:
        student = app.students.get_student(args.report)
        if student:
            print(app.reports.generate_detailed_report(student))
            sys.exit(0)
        else:
            print(f"Student with roll number {args.report} not found.")
            sys.exit(1)

    if args.summary:
        print("=== BATCH SUMMARY ===")
        for s in app.students.get_all_students():
            analysis = app.analyzer.analyze_student(s)
            avg = analysis['average'] if analysis else 'N/A'
            print(f"{s.roll_no} | {s.name:<18} | Average: {avg}%")
        sys.exit(0)

    # Launch interactive experience
    app.run()

if __name__ == "__main__":
    main()

