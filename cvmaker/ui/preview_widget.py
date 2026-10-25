"""
Live HTML Preview and Export Widget for CV Maker.
Uses QtWebEngineView for instant updates as data changes.
"""
import os
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QComboBox, QLabel, QFileDialog, QMessageBox
)
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import Signal, QUrl
from ..models.resume import Resume
from ..templates.engine import TemplateEngine, THEMES
from ..exporter.pdf_exporter import PdfExporter
from ..exporter.docx_exporter import DocxExporter


class PreviewWidget(QWidget):
    theme_changed = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.template_engine = TemplateEngine()
        self.current_resume: Resume = None
        self.current_html: str = ""

        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Top Control Bar (Theme Selector & Export Buttons)
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        theme_label = QLabel("Theme:")
        theme_label.setStyleSheet("font-weight: bold;")
        self.theme_combo = QComboBox()
        for key, name in THEMES.items():
            self.theme_combo.addItem(name, key)
        self.theme_combo.currentIndexChanged.connect(self._on_theme_selection)

        self.btn_export_pdf = QPushButton("📄 Export to PDF")
        self.btn_export_pdf.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: white;
                font-weight: bold;
                padding: 6px 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        self.btn_export_pdf.clicked.connect(self.export_pdf)

        self.btn_export_docx = QPushButton("📝 Export to DOCX")
        self.btn_export_docx.setStyleSheet("""
            QPushButton {
                background-color: #059669;
                color: white;
                font-weight: bold;
                padding: 6px 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #047857;
            }
        """)
        self.btn_export_docx.clicked.connect(self.export_docx)

        top_bar.addWidget(theme_label)
        top_bar.addWidget(self.theme_combo)
        top_bar.addStretch()
        top_bar.addWidget(self.btn_export_pdf)
        top_bar.addWidget(self.btn_export_docx)

        layout.addLayout(top_bar)

        # Embedded Web View for Real-time rendering
        self.web_view = QWebEngineView()
        self.web_view.setStyleSheet("border: 1px solid #d1d5db; background-color: #f3f4f6;")
        layout.addWidget(self.web_view)

    def _on_theme_selection(self, index: int):
        theme_key = self.theme_combo.currentData()
        if self.current_resume:
            self.current_resume.selected_theme = theme_key
            self.update_preview(self.current_resume)
        self.theme_changed.emit(theme_key)

    def update_preview(self, resume: Resume):
        self.current_resume = resume
        
        # Sync combo if theme is set on resume
        for i in range(self.theme_combo.count()):
            if self.theme_combo.itemData(i) == resume.selected_theme:
                if self.theme_combo.currentIndex() != i:
                    self.theme_combo.blockSignals(True)
                    self.theme_combo.setCurrentIndex(i)
                    self.theme_combo.blockSignals(False)
                break

        self.current_html = self.template_engine.render_resume(resume)
        self.web_view.setHtml(self.current_html)

    def export_pdf(self):
        if not self.current_resume:
            return
        
        default_filename = f"{self.current_resume.contact.full_name or 'Resume'}.pdf".replace(" ", "_")
        path, _ = QFileDialog.getSaveFileName(self, "Save Resume as PDF", default_filename, "PDF Files (*.pdf)")
        
        if path:
            success = PdfExporter.export_html_to_pdf(self.current_html, path)
            if success:
                QMessageBox.information(self, "Export Complete", f"Resume successfully saved to:\n{path}")
            else:
                QMessageBox.critical(self, "Export Error", "Failed to generate PDF. Please try again.")

    def export_docx(self):
        if not self.current_resume:
            return

        default_filename = f"{self.current_resume.contact.full_name or 'Resume'}.docx".replace(" ", "_")
        path, _ = QFileDialog.getSaveFileName(self, "Save Resume as Word Document", default_filename, "Word Documents (*.docx)")

        if path:
            success, msg = DocxExporter.export_html_to_docx(self.current_html, path)
            if success:
                QMessageBox.information(self, "Export Complete", f"Resume successfully exported to DOCX:\n{path}")
            else:
                QMessageBox.critical(self, "Export Error", f"Failed to export DOCX:\n{msg}")
