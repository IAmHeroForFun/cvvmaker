"""
Dynamic list widget for editing work experience items with live bullet-point CAR/PAR analysis.
"""
from typing import List
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QPushButton, QGroupBox, QCheckBox, QLabel
)
from PySide6.QtCore import Signal
from ...models.resume import ExperienceItem
from ...advisors.ats_rules import analyze_bullet_point


class SingleExperienceCard(QGroupBox):
    changed = Signal()
    delete_requested = Signal(object)

    def __init__(self, item: ExperienceItem = None, parent=None):
        super().__init__(parent)
        self.setTitle("Work Experience Entry")
        self.setStyleSheet("""
            QGroupBox {
                border: 1px solid #d1d5db;
                border-radius: 6px;
                margin-top: 8px;
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
            QCheckBox {
                color: #374151;
            }
        """)
        self._init_ui()
        if item:
            self.set_data(item)

    def _init_ui(self):
        main_layout = QVBoxLayout(self)

        top_row = QHBoxLayout()
        btn_del = QPushButton("✕ Remove Position")
        btn_del.setStyleSheet("color: #dc2626; border: none; font-weight: bold;")
        btn_del.clicked.connect(lambda: self.delete_requested.emit(self))
        top_row.addStretch()
        top_row.addWidget(btn_del)
        main_layout.addLayout(top_row)

        form = QFormLayout()
        self.in_company = QLineEdit()
        self.in_company.setPlaceholderText("e.g. Acme Corp")
        self.in_company.textChanged.connect(self._on_change)

        self.in_position = QLineEdit()
        self.in_position.setPlaceholderText("e.g. Senior Software Engineer")
        self.in_position.textChanged.connect(self._on_change)

        self.in_location = QLineEdit()
        self.in_location.setPlaceholderText("e.g. New York, NY (or Remote)")
        self.in_location.textChanged.connect(self._on_change)

        dates_layout = QHBoxLayout()
        self.in_start = QLineEdit()
        self.in_start.setPlaceholderText("Start (e.g. 2021-06)")
        self.in_start.textChanged.connect(self._on_change)

        self.in_end = QLineEdit()
        self.in_end.setPlaceholderText("End (e.g. 2023-12)")
        self.in_end.textChanged.connect(self._on_change)

        self.chk_current = QCheckBox("Current Job")
        self.chk_current.toggled.connect(self._on_current_toggled)

        dates_layout.addWidget(self.in_start)
        dates_layout.addWidget(QLabel("to"))
        dates_layout.addWidget(self.in_end)
        dates_layout.addWidget(self.chk_current)

        form.addRow("Company Name:", self.in_company)
        form.addRow("Position / Title:", self.in_position)
        form.addRow("Location:", self.in_location)
        form.addRow("Dates:", dates_layout)

        main_layout.addLayout(form)

        # Bullets / Accomplishments
        lbl_bullets = QLabel("<b>Key Accomplishments (One bullet per line):</b><br><span style='color: #6b7280; font-weight: normal; font-size: 8.5pt;'>Use Action Verb + Problem/Task + Quantifiable Result</span>")
        main_layout.addWidget(lbl_bullets)

        self.txt_highlights = QTextEdit()
        self.txt_highlights.setPlaceholderText(
            "• Spearheaded migration to PostgreSQL, cutting query latency by 45%\n"
            "• Directed a cross-functional team of 6 engineers to deliver mobile app 2 weeks ahead of deadline"
        )
        self.txt_highlights.setMinimumHeight(90)
        self.txt_highlights.textChanged.connect(self._on_bullets_changed)
        main_layout.addWidget(self.txt_highlights)

        # Feedback banner
        self.lbl_feedback = QLabel()
        self.lbl_feedback.setWordWrap(True)
        self.lbl_feedback.setStyleSheet("font-size: 8.5pt; color: #4b5563;")
        main_layout.addWidget(self.lbl_feedback)

    def _on_current_toggled(self, checked: bool):
        self.in_end.setEnabled(not checked)
        if checked:
            self.in_end.setText("Present")
        self._on_change()

    def _on_bullets_changed(self):
        text = self.txt_highlights.toPlainText().strip()
        lines = [line.strip().lstrip("•-* ") for line in text.split("\n") if line.strip()]
        if lines:
            # Check the last edited bullet
            res = analyze_bullet_point(lines[-1])
            if res["score"] >= 80:
                self.lbl_feedback.setText(f"<span style='color: #059669;'>✓ High-impact bullet (Score: {res['score']}/100)</span>")
            else:
                sugg = " ".join(res["suggestions"][:1])
                self.lbl_feedback.setText(f"<span style='color: #d97706;'>⚡ Tip ({res['score']}/100): {sugg}</span>")
        else:
            self.lbl_feedback.setText("")

        self._on_change()

    def _on_change(self):
        self.changed.emit()

    def set_data(self, item: ExperienceItem):
        self.in_company.setText(item.company)
        self.in_position.setText(item.position)
        self.in_location.setText(item.location)
        self.in_start.setText(item.start_date)
        self.in_end.setText(item.end_date)
        self.chk_current.setChecked(item.is_current)
        bullets_text = "\n".join(f"• {h}" for h in item.highlights)
        self.txt_highlights.setPlainText(bullets_text)

    def get_data(self) -> ExperienceItem:
        lines = [
            line.strip().lstrip("•-* ")
            for line in self.txt_highlights.toPlainText().split("\n")
            if line.strip()
        ]
        return ExperienceItem(
            company=self.in_company.text().strip(),
            position=self.in_position.text().strip(),
            location=self.in_location.text().strip(),
            start_date=self.in_start.text().strip(),
            end_date="Present" if self.chk_current.isChecked() else self.in_end.text().strip(),
            is_current=self.chk_current.isChecked(),
            highlights=lines
        )


class ExperienceEditor(QWidget):
    data_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.cards: List[SingleExperienceCard] = []
        self._init_ui()

    def _init_ui(self):
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.cards_layout = QVBoxLayout()
        self.main_layout.addLayout(self.cards_layout)

        btn_add = QPushButton("＋ Add Experience Entry")
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
        self.main_layout.addWidget(btn_add)

    def add_entry(self, item: ExperienceItem = None):
        card = SingleExperienceCard(item, self)
        card.changed.connect(self._emit_change)
        card.delete_requested.connect(self._remove_entry)
        self.cards.append(card)
        self.cards_layout.addWidget(card)
        self._emit_change()

    def _remove_entry(self, card: SingleExperienceCard):
        if card in self.cards:
            self.cards.remove(card)
            self.cards_layout.removeWidget(card)
            card.deleteLater()
            self._emit_change()

    def _emit_change(self):
        self.data_changed.emit()

    def set_data(self, items: List[ExperienceItem]):
        for card in list(self.cards):
            self.cards_layout.removeWidget(card)
            card.deleteLater()
        self.cards.clear()

        for item in items:
            self.add_entry(item)

    def get_data(self) -> List[ExperienceItem]:
        return [card.get_data() for card in self.cards]
