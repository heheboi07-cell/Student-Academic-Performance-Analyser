# Problem Statement: Student Academic Performance Analyzer

## 1. Problem Statement
Maintaining an accurate overview of semester progress, grade averages, and attendance thresholds is critical for university students. Manual tracking often results in overlooked attendance deficits and missed opportunities to prioritize weaker courses. 

The **Student Academic Performance Analyzer** is an offline, terminal-based application written in modular Python that allows students to register academic details, log marks, compute grade averages, identify strong and weak subjects, receive actionable suggestions, and export detailed academic reports.

## 2. Scope & Target Users
- **Target Users:** Engineering and college students who want a lightweight, distraction-free command-line tool.
- **In-Scope:**
  - Student Profile Management (CRUD operations, search).
  - Academic Records (marks entry with 0–100 limits, attendance logging).
  - Performance Analysis (averages, letter grades, highest/lowest subjects, automated advice).
  - Report Generation (ASCII summary cards, file export).
  - Data Persistence (JSON storage with backup and restore).
- **Out-of-Scope:**
  - Direct live database sync with university ERPs.
  - Graphical (GUI) frameworks.

## 3. High-Level Features
- 5-module decoupled architecture.
- Real-time performance insights and targeted study recommendations.
- Interactive menu and direct command-line arguments for automated testing.
- Comprehensive unit tests covering calculations and report rendering.