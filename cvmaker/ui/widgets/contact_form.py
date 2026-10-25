"""
Form widget for editing contact info and the professional summary.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QTextEdit, QLabel
)
from PySide6.QtCore import Signal
from ...models.resume import ContactInfo


class ContactForm(QWidget):
    data_changed = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)

        form = QFormLayout()
        form.setSpacing(8)

        self.in_name = QLineEdit()
        self.in_name.setPlaceholderText("e.g. Alex Rivera")
        self.in_name.textChanged.connect(self._emit_change)

        self.in_headline = QLineEdit()
        self.in_headline.setPlaceholderText("e.g. Senior Full Stack Engineer")
        self.in_headline.textChanged.connect(self._emit_change)

        self.in_email = QLineEdit()
        self.in_email.setPlaceholderText("e.g. alex.rivera@example.com")
        self.in_email.textChanged.connect(self._emit_change)

        self.in_phone = QLineEdit()
        self.in_phone.setPlaceholderText("e.g. +1 (555) 019-2834")
        self.in_phone.textChanged.connect(self._emit_change)

        self.in_location = QLineEdit()
        self.in_location.setPlaceholderText("e.g. San Francisco, CA or London, UK")
        self.in_location.textChanged.connect(self._emit_change)

        self.in_linkedin = QLineEdit()
        self.in_linkedin.setPlaceholderText("e.g. linkedin.com/in/alexrivera")
        self.in_linkedin.textChanged.connect(self._emit_change)

        self.in_github = QLineEdit()
        self.in_github.setPlaceholderText("e.g. github.com/alexrivera")
        self.in_github.textChanged.connect(self._emit_change)

        self.in_website = QLineEdit()
        self.in_website.setPlaceholderText("e.g. alexrivera.dev")
        self.in_website.textChanged.connect(self._emit_change)

        form.addRow("Full Name*:", self.in_name)
        form.addRow("Professional Title:", self.in_headline)
        form.addRow("Email*:", self.in_email)
        form.addRow("Phone:", self.in_phone)
        form.addRow("Location (City, Country):", self.in_location)
        form.addRow("LinkedIn:", self.in_linkedin)
        form.addRow("GitHub / Portfolio:", self.in_github)
        form.addRow("Personal Website:", self.in_website)

        self.setStyleSheet("""
            QLabel {
                color: #374151;
                font-weight: 500;
            }
            QLineEdit {
                background-color: #ffffff;
                color: #111827;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                padding: 5px 8px;
            }
            QLineEdit:focus {
                border: 1px solid #2563eb;
            }
        """)
        layout.addLayout(form)

    def _emit_change(self):
        self.data_changed.emit()

    def set_data(self, contact: ContactInfo):
        self.in_name.setText(contact.full_name)
        self.in_headline.setText(contact.headline)
        self.in_email.setText(contact.email)
        self.in_phone.setText(contact.phone)
        self.in_location.setText(contact.location)
        self.in_linkedin.setText(contact.linkedin)
        self.in_github.setText(contact.github)
        self.in_website.setText(contact.website)

    def get_data(self) -> ContactInfo:
        return ContactInfo(
            full_name=self.in_name.text().strip(),
            headline=self.in_headline.text().strip(),
            email=self.in_email.text().strip(),
            phone=self.in_phone.text().strip(),
            location=self.in_location.text().strip(),
            linkedin=self.in_linkedin.text().strip(),
            github=self.in_github.text().strip(),
            website=self.in_website.text().strip()
        )
