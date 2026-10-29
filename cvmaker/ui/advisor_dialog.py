"""
Advisor Modal Dialog: Action Verbs Browser & Outdated Resume Pitfall Checker.
"""
from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QTabWidget, QWidget, QListWidget, QListWidgetItem,
    QTextBrowser, QPushButton
)
from PySide6.QtGui import QColor, QFont
from ..advisors.verbs import ACTION_VERBS_BY_CATEGORY
from ..advisors.ats_rules import scan_for_red_flags
from ..models.resume import Resume


class AdvisorDialog(QDialog):
    def __init__(self, resume: Resume, parent=None):
        super().__init__(parent)
        self.resume = resume
        self.setWindowTitle("Resume Writing Advisor & Best Practices")
        self.resize(750, 580)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        tabs = QTabWidget()

        # Tab 1: High-Impact Action Verbs
        tab_verbs = QWidget()
        v_verbs = QVBoxLayout(tab_verbs)
        lbl_verbs = QLabel(
            "<b>Power Action Verbs by Category:</b><br>"
            "<span style='color: #4b5563;'>Start every bullet point with an active, high-impact verb.</span>"
        )
        v_verbs.addWidget(lbl_verbs)

        verb_tabs = QTabWidget()
        for category, verbs in ACTION_VERBS_BY_CATEGORY.items():
            list_widget = QListWidget()
            for v in sorted(verbs):
                item = QListWidgetItem(v)
                item.setFont(QFont("sans-serif", 10, QFont.Bold))
                list_widget.addItem(item)
            verb_tabs.addTab(list_widget, category)

        v_verbs.addWidget(verb_tabs)
        tabs.addTab(tab_verbs, "Action Verbs Library")

        # Tab 2: Resume Health Check (Pitfalls & Red Flags)
        tab_health = QWidget()
        v_health = QVBoxLayout(tab_health)
        lbl_health = QLabel(
            "<b>Resume Modernization Audit:</b><br>"
            "<span style='color: #4b5563;'>Scans for obsolete habits (marital status, DOB, declarations, salary disclosures).</span>"
        )
        v_health.addWidget(lbl_health)

        self.health_browser = QTextBrowser()
        v_health.addWidget(self.health_browser)
        self._run_health_check()
        tabs.addTab(tab_health, "Modernization Audit")

        # Tab 3: The 3 Golden Rules (from Study materials)
        tab_rules = QWidget()
        v_rules = QVBoxLayout(tab_rules)
        rules_text = QTextBrowser()
        rules_text.setHtml("""
        <h3>The 3 Rules of World-Class Resumes</h3>
        <hr>
        <p><b>1. The CAR / PAR Framework (Challenge - Action - Result)</b><br>
        Never list routine responsibilities. Instead, frame each bullet as:
        <br><i>[Strong Action Verb] + [Context/Problem] + [Measurable Outcome]</i>
        <br><b>Weak:</b> Handled client database queries.
        <br><b>World-Class:</b> Streamlined client SQL query workflows, slashing report turnaround time by 45%.
        </p>

        <p><b>2. The 6-Second First Scan Rule</b><br>
        Recruiters and automated ATS scan the top 1/3 of the page first. Ensure your <b>Name, Target Title, Contact Links</b>, and <b>Professional Summary</b> immediately convey your value proposition.
        </p>

        <p><b>3. Privacy & Anti-Discrimination Standards</b><br>
        Global hiring standards strictly mandate omitting personal demographics (marital status, religion, caste, DOB, photo on US/UK tech resumes). Let your skills and quantifiable track record speak for themselves.
        </p>
        """)
        v_rules.addWidget(rules_text)
        tabs.addTab(tab_rules, "Golden Rules")

        layout.addWidget(tabs)

        btn_close = QPushButton("Close")
        btn_close.clicked.connect(self.accept)
        layout.addWidget(btn_close)

    def _run_health_check(self):
        full_text = self.resume.to_json()
        red_flags = scan_for_red_flags(full_text)

        if not red_flags:
            self.health_browser.setHtml(
                "<div style='color: #059669; font-size: 14pt; font-weight: bold;'>✓ Excellent! No outdated red-flags detected.</div>"
                "<p style='color: #374151;'>Your resume avoids obsolete regional information like marital status, age/DOB, or salary disclosures.</p>"
            )
        else:
            html = "<div style='color: #dc2626; font-size: 13pt; font-weight: bold;'>⚠️ Items that need attention:</div><ul>"
            for pattern, expl in red_flags:
                html += f"<li style='margin-bottom: 8px;'><b>Flag:</b> {expl}</li>"
            html += "</ul>"
            self.health_browser.setHtml(html)
