"""
Editor widgets for Education, Projects, and Skills.
"""
from typing import List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QPushButton, QGroupBox, QLabel
)
from PySide6.QtCore import Signal
from ...models.resume import EducationItem, ProjectItem, SkillCategory
from ...advisors.ats_rules import analyze_bullet_point


# ===================== PROJECTS =====================

class SingleProjectCard(QGroupBox):
    changed = Signal()
    delete_requested = Signal(object)

    def __init__(self, item: ProjectItem = None, parent=None):
        super().__init__(parent)
        self.setTitle("Project Entry")
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding-top: 14px;
                background-color: #fafafa;
                color: #111827;
                font-weight: bold;
            }
            QLabel {
                color: #374151;
            }
            QLineEdit, QTextEdit {
                background-color: #ffffff;
                color: #111827;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 4px 8px;
            }
        """)
        self._init_ui()
        if item:
            self.set_data(item)

    def _init_ui(self):
        layout = QVBoxLayout(self)

        top_row = QHBoxLayout()
        btn_del = QPushButton("✕ Remove Project")
        btn_del.setStyleSheet("color: #dc2626; border: none; font-weight: bold;")
        btn_del.clicked.connect(lambda: self.delete_requested.emit(self))
        top_row.addStretch()
        top_row.addWidget(btn_del)
        layout.addLayout(top_row)

        form = QFormLayout()
        self.in_name = QLineEdit()
        self.in_name.setPlaceholderText("e.g. Self-Hosted DNS & VPN Infrastructure")
        self.in_name.textChanged.connect(lambda: self.changed.emit())

        self.in_role = QLineEdit()
        self.in_role.setPlaceholderText("e.g. Creator & Lead Developer")
        self.in_role.textChanged.connect(lambda: self.changed.emit())

        self.in_tech = QLineEdit()
        self.in_tech.setPlaceholderText("e.g. Docker, WireGuard, Unbound, Linux, Bash")
        self.in_tech.textChanged.connect(lambda: self.changed.emit())

        self.in_link = QLineEdit()
        self.in_link.setPlaceholderText("e.g. https://github.com/yourusername/dns-vpn")
        self.in_link.textChanged.connect(lambda: self.changed.emit())

        form.addRow("Project Name:", self.in_name)
        form.addRow("Your Role:", self.in_role)
        form.addRow("Technologies:", self.in_tech)
        form.addRow("Link / URL:", self.in_link)

        layout.addLayout(form)

        lbl_bullets = QLabel(
            "<b>Key Accomplishments (One bullet per line):</b><br>"
            "<span style='color: #6b7280; font-weight: normal; font-size: 8.5pt;'>Action Verb + Problem/Architecture + Outcome</span>"
        )
        layout.addWidget(lbl_bullets)

        self.txt_highlights = QTextEdit()
        self.txt_highlights.setPlaceholderText(
            "• Architected a secure containerized DNS filter using Docker and WireGuard VPN\n"
            "• Decreased local telemetry and improved recursive DNS query latency by 35%"
        )
        self.txt_highlights.setMinimumHeight(80)
        self.txt_highlights.textChanged.connect(self._on_bullets_changed)
        layout.addWidget(self.txt_highlights)

        self.lbl_feedback = QLabel()
        self.lbl_feedback.setWordWrap(True)
        self.lbl_feedback.setStyleSheet("font-size: 8.5pt; color: #4b5563;")
        layout.addWidget(self.lbl_feedback)

    def _on_bullets_changed(self):
        text = self.txt_highlights.toPlainText().strip()
        lines = [line.strip().lstrip("•-* ") for line in text.split("\n") if line.strip()]
        if lines:
            res = analyze_bullet_point(lines[-1])
            if res["score"] >= 80:
                self.lbl_feedback.setText(f"<span style='color: #059669;'>✓ Strong bullet (Score: {res['score']}/100)</span>")
            else:
                sugg = " ".join(res["suggestions"][:1])
                self.lbl_feedback.setText(f"<span style='color: #d97706;'>⚡ Tip ({res['score']}/100): {sugg}</span>")
        else:
            self.lbl_feedback.setText("")
        self.changed.emit()

    def set_data(self, item: ProjectItem):
        self.in_name.setText(item.name)
        self.in_role.setText(item.role)
        self.in_tech.setText(item.technologies)
        self.in_link.setText(item.link)
        bullets_text = "\n".join(f"• {h}" for h in item.highlights)
        self.txt_highlights.setPlainText(bullets_text)

    def get_data(self) -> ProjectItem:
        lines = [
            line.strip().lstrip("•-* ")
            for line in self.txt_highlights.toPlainText().split("\n")
            if line.strip()
        ]
        return ProjectItem(
            name=self.in_name.text().strip(),
            role=self.in_role.text().strip(),
            technologies=self.in_tech.text().strip(),
            link=self.in_link.text().strip(),
            highlights=lines
        )


class ProjectsEditor(QWidget):
    data_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cards: List[SingleProjectCard] = []
        self._init_ui()

    def _init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout = QVBoxLayout()
        self.layout.addLayout(self.cards_layout)

        btn_add = QPushButton("＋ Add Project Entry")
        btn_add.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                border: 1px dashed #9ca3af;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
                color: #374151;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
            }
        """)
        btn_add.clicked.connect(self.add_entry)
        self.layout.addWidget(btn_add)

    def add_entry(self, item: ProjectItem = None):
        card = SingleProjectCard(item, self)
        card.changed.connect(lambda: self.data_changed.emit())
        card.delete_requested.connect(self._remove_entry)
        self.cards.append(card)
        self.cards_layout.addWidget(card)
        self.data_changed.emit()

    def _remove_entry(self, card: SingleProjectCard):
        if card in self.cards:
            self.cards.remove(card)
            self.cards_layout.removeWidget(card)
            card.deleteLater()
            self.data_changed.emit()

    def set_data(self, items: List[ProjectItem]):
        for c in list(self.cards):
            self.cards_layout.removeWidget(c)
            c.deleteLater()
        self.cards.clear()
        for i in items:
            self.add_entry(i)

    def get_data(self) -> List[ProjectItem]:
        return [c.get_data() for c in self.cards]


# ===================== EDUCATION =====================

class SingleEducationCard(QGroupBox):
    changed = Signal()
    delete_requested = Signal(object)

    def __init__(self, item: EducationItem = None, parent=None):
        super().__init__(parent)
        self.setTitle("Education Entry")
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding-top: 14px;
                background-color: #fafafa;
                color: #111827;
                font-weight: bold;
            }
            QLabel {
                color: #374151;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #111827;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 4px 8px;
            }
        """)
        self._init_ui()
        if item:
            self.set_data(item)

    def _init_ui(self):
        layout = QVBoxLayout(self)

        top_row = QHBoxLayout()
        btn_del = QPushButton("✕ Remove")
        btn_del.setStyleSheet("color: #dc2626; border: none; font-weight: bold;")
        btn_del.clicked.connect(lambda: self.delete_requested.emit(self))
        top_row.addStretch()
        top_row.addWidget(btn_del)
        layout.addLayout(top_row)

        form = QFormLayout()
        self.in_inst = QLineEdit()
        self.in_inst.setPlaceholderText("e.g. UC Berkeley")
        self.in_inst.textChanged.connect(lambda: self.changed.emit())

        self.in_deg = QLineEdit()
        self.in_deg.setPlaceholderText("e.g. Bachelor of Science")
        self.in_deg.textChanged.connect(lambda: self.changed.emit())

        self.in_major = QLineEdit()
        self.in_major.setPlaceholderText("e.g. Computer Science")
        self.in_major.textChanged.connect(lambda: self.changed.emit())

        dates_row = QHBoxLayout()
        self.in_start = QLineEdit()
        self.in_start.setPlaceholderText("2018")
        self.in_start.textChanged.connect(lambda: self.changed.emit())
        self.in_end = QLineEdit()
        self.in_end.setPlaceholderText("2022")
        self.in_end.textChanged.connect(lambda: self.changed.emit())
        self.in_gpa = QLineEdit()
        self.in_gpa.setPlaceholderText("3.8 / 4.0")
        self.in_gpa.textChanged.connect(lambda: self.changed.emit())

        dates_row.addWidget(self.in_start)
        dates_row.addWidget(QLabel("to"))
        dates_row.addWidget(self.in_end)
        dates_row.addWidget(QLabel("GPA:"))
        dates_row.addWidget(self.in_gpa)

        form.addRow("Institution:", self.in_inst)
        form.addRow("Degree:", self.in_deg)
        form.addRow("Field of Study:", self.in_major)
        form.addRow("Timeline & GPA:", dates_row)

        layout.addLayout(form)

    def set_data(self, item: EducationItem):
        self.in_inst.setText(item.institution)
        self.in_deg.setText(item.degree)
        self.in_major.setText(item.field_of_study)
        self.in_start.setText(item.start_date)
        self.in_end.setText(item.end_date)
        self.in_gpa.setText(item.grade_or_gpa)

    def get_data(self) -> EducationItem:
        return EducationItem(
            institution=self.in_inst.text().strip(),
            degree=self.in_deg.text().strip(),
            field_of_study=self.in_major.text().strip(),
            start_date=self.in_start.text().strip(),
            end_date=self.in_end.text().strip(),
            grade_or_gpa=self.in_gpa.text().strip()
        )


class EducationEditor(QWidget):
    data_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cards: List[SingleEducationCard] = []
        self._init_ui()

    def _init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout = QVBoxLayout()
        self.layout.addLayout(self.cards_layout)

        btn_add = QPushButton("＋ Add Education")
        btn_add.setStyleSheet("background-color: #f3f4f6; border: 1px dashed #9ca3af; padding: 6px; font-weight: bold;")
        btn_add.clicked.connect(self.add_entry)
        self.layout.addWidget(btn_add)

    def add_entry(self, item: EducationItem = None):
        card = SingleEducationCard(item, self)
        card.changed.connect(lambda: self.data_changed.emit())
        card.delete_requested.connect(self._remove_entry)
        self.cards.append(card)
        self.cards_layout.addWidget(card)
        self.data_changed.emit()

    def _remove_entry(self, card):
        if card in self.cards:
            self.cards.remove(card)
            self.cards_layout.removeWidget(card)
            card.deleteLater()
            self.data_changed.emit()

    def set_data(self, items: List[EducationItem]):
        for c in list(self.cards):
            self.cards_layout.removeWidget(c)
            c.deleteLater()
        self.cards.clear()
        for i in items:
            self.add_entry(i)

    def get_data(self) -> List[EducationItem]:
        return [c.get_data() for c in self.cards]


# ===================== SKILLS =====================

class SingleSkillCategoryCard(QGroupBox):
    changed = Signal()
    delete_requested = Signal(object)

    def __init__(self, item: SkillCategory = None, parent=None):
        super().__init__(parent)
        self.setTitle("Skill Category")
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding-top: 14px;
                background-color: #fafafa;
                color: #111827;
                font-weight: bold;
            }
            QLabel {
                color: #374151;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #111827;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 4px 8px;
            }
        """)
        self._init_ui()
        if item:
            self.set_data(item)

    def _init_ui(self):
        layout = QVBoxLayout(self)

        top_row = QHBoxLayout()
        btn_del = QPushButton("✕ Remove")
        btn_del.setStyleSheet("color: #dc2626; border: none; font-weight: bold;")
        btn_del.clicked.connect(lambda: self.delete_requested.emit(self))
        top_row.addStretch()
        top_row.addWidget(btn_del)
        layout.addLayout(top_row)

        form = QFormLayout()
        self.in_cat = QLineEdit()
        self.in_cat.setPlaceholderText("e.g. Languages or Tools & Platforms")
        self.in_cat.textChanged.connect(lambda: self.changed.emit())

        self.in_skills = QLineEdit()
        self.in_skills.setPlaceholderText("e.g. Python, Docker, PostgreSQL, React (comma separated)")
        self.in_skills.textChanged.connect(lambda: self.changed.emit())

        form.addRow("Category Name:", self.in_cat)
        form.addRow("Skills (comma-separated):", self.in_skills)
        layout.addLayout(form)

    def set_data(self, item: SkillCategory):
        self.in_cat.setText(item.category)
        self.in_skills.setText(", ".join(item.skills))

    def get_data(self) -> SkillCategory:
        skills = [s.strip() for s in self.in_skills.text().split(",") if s.strip()]
        return SkillCategory(category=self.in_cat.text().strip(), skills=skills)


class SkillsEditor(QWidget):
    data_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cards: List[SingleSkillCategoryCard] = []
        self._init_ui()

    def _init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout = QVBoxLayout()
        self.layout.addLayout(self.cards_layout)

        btn_add = QPushButton("＋ Add Skill Category")
        btn_add.setStyleSheet("background-color: #f3f4f6; border: 1px dashed #9ca3af; padding: 6px; font-weight: bold;")
        btn_add.clicked.connect(self.add_entry)
        self.layout.addWidget(btn_add)

    def add_entry(self, item: SkillCategory = None):
        card = SingleSkillCategoryCard(item, self)
        card.changed.connect(lambda: self.data_changed.emit())
        card.delete_requested.connect(self._remove_entry)
        self.cards.append(card)
        self.cards_layout.addWidget(card)
        self.data_changed.emit()

    def _remove_entry(self, card):
        if card in self.cards:
            self.cards.remove(card)
            self.cards_layout.removeWidget(card)
            card.deleteLater()
            self.data_changed.emit()

    def set_data(self, items: List[SkillCategory]):
        for c in list(self.cards):
            self.cards_layout.removeWidget(c)
            c.deleteLater()
        self.cards.clear()
        for i in items:
            self.add_entry(i)

    def get_data(self) -> List[SkillCategory]:
        return [c.get_data() for c in self.cards]


# ===================== CERTIFICATIONS =====================

from ...models.resume import CertificationItem

class SingleCertificationCard(QGroupBox):
    changed = Signal()
    delete_requested = Signal(object)

    def __init__(self, item: CertificationItem = None, parent=None):
        super().__init__(parent)
        self.setTitle("Certification Entry")
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding-top: 14px;
                background-color: #fafafa;
                color: #111827;
                font-weight: bold;
            }
            QLabel {
                color: #374151;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #111827;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 4px 8px;
            }
        """)
        self._init_ui()
        if item:
            self.set_data(item)

    def _init_ui(self):
        layout = QVBoxLayout(self)

        top_row = QHBoxLayout()
        btn_del = QPushButton("✕ Remove")
        btn_del.setStyleSheet("color: #dc2626; border: none; font-weight: bold;")
        btn_del.clicked.connect(lambda: self.delete_requested.emit(self))
        top_row.addStretch()
        top_row.addWidget(btn_del)
        layout.addLayout(top_row)

        form = QFormLayout()
        self.in_name = QLineEdit()
        self.in_name.setPlaceholderText("e.g. AWS Certified Solutions Architect – Associate")
        self.in_name.textChanged.connect(lambda: self.changed.emit())

        self.in_issuer = QLineEdit()
        self.in_issuer.setPlaceholderText("e.g. Amazon Web Services (AWS)")
        self.in_issuer.textChanged.connect(lambda: self.changed.emit())

        self.in_date = QLineEdit()
        self.in_date.setPlaceholderText("e.g. 2023 or Nov 2023")
        self.in_date.textChanged.connect(lambda: self.changed.emit())

        self.in_url = QLineEdit()
        self.in_url.setPlaceholderText("e.g. Verification URL or Credential ID")
        self.in_url.textChanged.connect(lambda: self.changed.emit())

        form.addRow("Certification Name:", self.in_name)
        form.addRow("Issuing Organization:", self.in_issuer)
        form.addRow("Issue Date / Year:", self.in_date)
        form.addRow("Credential URL / ID:", self.in_url)

        layout.addLayout(form)

    def set_data(self, item: CertificationItem):
        self.in_name.setText(item.name)
        self.in_issuer.setText(item.issuer)
        self.in_date.setText(item.issue_date)
        self.in_url.setText(item.credential_url)

    def get_data(self) -> CertificationItem:
        return CertificationItem(
            name=self.in_name.text().strip(),
            issuer=self.in_issuer.text().strip(),
            issue_date=self.in_date.text().strip(),
            credential_url=self.in_url.text().strip()
        )


class CertificationsEditor(QWidget):
    data_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cards: List[SingleCertificationCard] = []
        self._init_ui()

    def _init_ui(self):
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.cards_layout = QVBoxLayout()
        self.layout.addLayout(self.cards_layout)

        btn_add = QPushButton("＋ Add Certification")
        btn_add.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                border: 1px dashed #9ca3af;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
                color: #374151;
            }
            QPushButton:hover {
                background-color: #e5e7eb;
            }
        """)
        btn_add.clicked.connect(self.add_entry)
        self.layout.addWidget(btn_add)

    def add_entry(self, item: CertificationItem = None):
        card = SingleCertificationCard(item, self)
        card.changed.connect(lambda: self.data_changed.emit())
        card.delete_requested.connect(self._remove_entry)
        self.cards.append(card)
        self.cards_layout.addWidget(card)
        self.data_changed.emit()

    def _remove_entry(self, card: SingleCertificationCard):
        if card in self.cards:
            self.cards.remove(card)
            self.cards_layout.removeWidget(card)
            card.deleteLater()
            self.data_changed.emit()

    def set_data(self, items: List[CertificationItem]):
        for c in list(self.cards):
            self.cards_layout.removeWidget(c)
            c.deleteLater()
        self.cards.clear()
        for i in items:
            self.add_entry(i)

    def get_data(self) -> List[CertificationItem]:
        return [c.get_data() for c in self.cards]

