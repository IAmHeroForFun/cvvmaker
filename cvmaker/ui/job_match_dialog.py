"""
Dialog for matching resume against a target job description.
Extracts top technical and domain keywords and shows missing skills.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit,
    QPushButton, QProgressBar, QGroupBox, QListWidget, QListWidgetItem
)
from PySide6.QtGui import QColor
from ..models.resume import Resume
from ..advisors.keyword_matcher import match_resume_to_job


class JobMatchDialog(QDialog):
    def __init__(self, resume: Resume, parent=None):
        super().__init__(parent)
        self.resume = resume
        self.setWindowTitle("Offline Job Matcher & Keyword Optimizer")
        self.resize(720, 600)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        desc_label = QLabel(
            "<b>Paste a Job Description below:</b><br>"
            "<span style='color: #4b5563;'>The tool analyzes the posting 100% offline and compares keywords against your resume.</span>"
        )
        layout.addWidget(desc_label)

        self.txt_job = QTextEdit()
        self.txt_job.setPlaceholderText("Paste target job requirements and duties here...")
        self.txt_job.setMaximumHeight(150)
        layout.addWidget(self.txt_job)

        btn_analyze = QPushButton("🔍 Analyze & Match Keywords")
        btn_analyze.setStyleSheet("""
            QPushButton {
                background-color: #4f46e5;
                color: white;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #4338ca;
            }
        """)
        btn_analyze.clicked.connect(self._do_analysis)
        layout.addWidget(btn_analyze)

        # Match Score Bar
        score_box = QHBoxLayout()
        score_label = QLabel("<b>Target Match Rate:</b>")
        self.score_bar = QProgressBar()
        self.score_bar.setRange(0, 100)
        self.score_bar.setValue(0)
        self.score_bar.setTextVisible(True)
        self.score_bar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #d1d5db;
                border-radius: 4px;
                text-align: center;
                height: 24px;
                font-weight: bold;
            }
            QProgressBar::chunk {
                background-color: #10b981;
            }
        """)
        score_box.addWidget(score_label)
        score_box.addWidget(self.score_bar)
        layout.addLayout(score_box)

        # Keyword Split: Found vs Missing
        lists_layout = QHBoxLayout()
        
        box_matched = QGroupBox("Matched Keywords in Resume")
        v_matched = QVBoxLayout(box_matched)
        self.list_matched = QListWidget()
        v_matched.addWidget(self.list_matched)

        box_missing = QGroupBox("⚠️ Missing Keywords (Add to Experience/Skills)")
        v_missing = QVBoxLayout(box_missing)
        self.list_missing = QListWidget()
        v_missing.addWidget(self.list_missing)

        lists_layout.addWidget(box_matched)
        lists_layout.addWidget(box_missing)
        layout.addLayout(lists_layout)

        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

    def _do_analysis(self):
        text = self.txt_job.toPlainText().strip()
        if not text:
            return

        result = match_resume_to_job(self.resume, text)
        pct = result["match_percentage"]
        self.score_bar.setValue(pct)

        self.list_matched.clear()
        for w in result["matched_keywords"]:
            item = QListWidgetItem(f"✓ {w}")
            item.setForeground(QColor("#059669"))
            self.list_matched.addItem(item)

        self.list_missing.clear()
        for w in result["missing_keywords"]:
            item = QListWidgetItem(f"✗ {w}")
            item.setForeground(QColor("#dc2626"))
            self.list_missing.addItem(item)
