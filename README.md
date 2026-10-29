# CV Maker — Professional Offline Resume Studio

A 100% offline desktop application designed to build world-class, ATS-compliant resumes with real-time preview and one-click dual export to **PDF** and **DOCX**.

Built based on proven principles from top career literature (*Modernize Your Resume*, *The Damn Good Resume Guide*, and *Resume Writing 2023*).

---

## ⚡ Quick Start (How to Run)

### Option 1: One-Click Shell Script (Linux / macOS)
Simply open your terminal in this directory and execute:
```bash
./run.sh
```
*(The script automatically uses `.venv`, sets display environment variables, and launches the application.)*

### Option 2: Python Script (Cross-Platform)
```bash
python3 run.py
```
or with the virtual environment:
```bash
.venv/bin/python run.py
```

### Option 3: Module Execution
```bash
python3 -m cvmaker
```

---

## 🚀 Key Features

### 1. 🔒 100% Offline & Private
- No cloud accounts, no API keys, and no telemetry.
- Your personal contact details and employment history never leave your computer.

### 2. 📄 Dual Export: PDF & DOCX
- **High-Resolution PDF**: 300 DPI print-ready rendering via Qt WebEngine with proper A4 and Letter pagination. Ideal for direct applications on modern company portals (Workday, Greenhouse, Lever).
- **Microsoft Word (.docx)**: Clean Open XML Word conversion via headless LibreOffice. Essential for recruitment agencies and legacy corporate portals requiring editable files.

### 3. 🎯 PAR / CAR Bullet Point Quality Analyzer
- Evaluates your experience bullets in real time as you type.
- Enforces the **CAR / PAR principle** (*Problem/Challenge + Action Verb + Quantifiable Result*).
- Flags weak passive phrases (e.g., *"Responsible for..."*, *"Worked on..."*) and prompts you to add measurable metrics (%, numbers, $, time saved).

### 4. 💼 Offline Job Keyword Matcher
- Click **"🎯 Job Description Matcher"** in the top toolbar.
- Paste any job posting description.
- Automatically analyzes high-frequency domain & technical skills and displays:
  - Match percentage score.
  - Matched keywords found in your resume.
  - Missing keywords you should consider incorporating.

### 5. 🛡️ Modernization & Anti-Discrimination Audit
- Click **"💡 Action Verbs & Audit"** in the toolbar.
- Scans your resume for outdated regional resume habits (marital status, date of birth/age, salary/CTC history, religious/caste info, or obsolete declaration statements).
- Includes a built-in searchable library of **curated action verbs** organized by Leadership, Engineering, Optimization, Research, and Communication.

### 6. 🎨 High-Contrast Modern Themes
- **Modern Clean**: Contemporary sans-serif layout with accent titles, perfect for Tech, Product, and Corporate roles.
- **Classic Executive**: Elegant serif layout tailored for management, legal, and traditional business sectors.
- Real-time instant preview as you edit form fields.

---

## 🛠️ Project Structure

```text
cvmaker/
├── cvmaker/
│   ├── advisors/            # Offline intelligence engines
│   │   ├── ats_rules.py     # PAR/CAR bullet scorer & red-flag auditor
│   │   ├── keyword_matcher.py # Offline job posting keyword matcher
│   │   └── verbs.py         # Curated action verbs database
│   ├── exporter/            # Dual export pipelines
│   │   ├── docx_exporter.py # Headless LibreOffice Word converter
│   │   └── pdf_exporter.py  # QtWebEngine print-to-PDF generator
│   ├── models/              # Data schemas & local JSON persistence
│   │   ├── resume.py        # Resume dataclasses & JSON serialization
│   │   └── storage.py       # File loader/saver & sample templates
│   ├── templates/           # Jinja2 HTML/CSS themes
│   │   ├── engine.py        # Template rendering engine
│   │   └── themes/          # Modern Clean & Classic Executive themes
│   ├── ui/                  # PySide6 desktop interface
│   │   ├── advisor_dialog.py # Verbs library & audit modal
│   │   ├── job_match_dialog.py # Job description matching dialog
│   │   ├── main_window.py   # Main split-view workspace
│   │   ├── preview_widget.py# Embedded live WebEngine preview
│   │   ├── styles.py        # High-contrast universal styling
│   │   └── widgets/         # Section form editors
│   └── __main__.py          # Module entry point
├── tests/                   # Automated unit & integration tests
├── .gitignore               # Ignores study materials, virtualenv, and temp files
├── README.md                # Documentation & user manual
├── requirements.txt         # Package dependencies
├── run.py                   # Python entry point launcher
└── run.sh                   # Linux one-click executable runner
```

---

## 🧪 Running Automated Tests

Run the full test suite with:
```bash
.venv/bin/python -m unittest discover -s tests -v
```

---

## 💡 Tips for Crafting a Winning CV

1. **Keep it focused**: Aim for 1 page for early career/students, and 2 pages maximum for experienced professionals.
2. **Quantify achievements**: Instead of *"Fixed bugs"*, write *"Resolved 40+ high-severity bugs in production, boosting platform uptime to 99.95%"*.
3. **Use the Job Matcher**: Before applying to a specific role, paste the job description into the built-in matcher to ensure critical skills and keywords are addressed in your summary and experience sections.
