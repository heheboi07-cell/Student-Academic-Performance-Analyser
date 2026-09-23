# Student Academic Performance Analyzer

A command-line Python application designed to track student details, record subject marks and attendance, compute performance metrics, and generate formatted academic reports.

---

## 5-Module Architecture
- `student.py`: Profile encapsulation, CRUD, and search functions.
- `academic.py`: Subject marks entry, validation, and attendance tracking.
- `analysis.py`: Computes averages, letter grades, extremes, and recommendations.
- `reports.py`: Formats terminal reports and exports to disk.
- `storage.py`: JSON datastore persistence, automated seeding, backup, and restore.

---

## How to Run

### Interactive Mode
```bash
python main.py