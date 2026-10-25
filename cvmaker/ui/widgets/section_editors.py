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
