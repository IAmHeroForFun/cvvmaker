"""
Main Window for the CV Maker Application.
Combines Section Editors, Real-Time Preview, Job Matcher, and Health Checks.
"""
import os
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QScrollArea, QToolBar, QPushButton, QLabel,
    QTextEdit, QTabWidget, QFileDialog, QMessageBox
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt

from ..models.resume import Resume
from ..models.storage import (
    save_resume_to_file, load_resume_from_file,
    get_sample_software_engineer_resume
)
from .preview_widget import PreviewWidget
from .widgets.contact_form import ContactForm
from .widgets.experience_editor import ExperienceEditor
from .widgets.section_editors import EducationEditor, SkillsEditor
from .advisor_dialog import AdvisorDialog
from .job_match_dialog import JobMatchDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CV Maker — Professional Offline Resume Studio")
        self.resize(1380, 880)

        # Start with pre-loaded high-standard resume
        self.current_resume: Resume = get_sample_software_engineer_resume()
        self.current_file_path: str = ""

        self._init_ui()
        self._load_resume_into_ui(self.current_resume)

    def _init_ui(self):
        # 1. Top Toolbar
        toolbar = QToolBar("Main Navigation")
        toolbar.setMovable(False)
        self.addToolBar(toolbar)

        act_new = QAction("📄 New Blank", self)
        act_new.triggered.connect(self._on_new)
        toolbar.addAction(act_new)

        act_sample = QAction("💡 Load Tech Template", self)
        act_sample.triggered.connect(self._on_load_sample)
        toolbar.addAction(act_sample)

        toolbar.addSeparator()

        act_open = QAction("📂 Open Draft...", self)
        act_open.triggered.connect(self._on_open)
        toolbar.addAction(act_open)

        act_save = QAction("💾 Save Draft", self)
        act_save.triggered.connect(self._on_save)
        toolbar.addAction(act_save)

        act_save_as = QAction("💾 Save As...", self)
        act_save_as.triggered.connect(self._on_save_as)
        toolbar.addAction(act_save_as)

        toolbar.addSeparator()

        act_job_match = QAction("🎯 Job Description Matcher", self)
        act_job_match.triggered.connect(self._open_job_matcher)
        toolbar.addAction(act_job_match)

        act_advisor = QAction("💡 Action Verbs & Audit", self)
        act_advisor.triggered.connect(self._open_advisor)
        toolbar.addAction(act_advisor)

        # 2. Main Central Split: Left is Form Editor, Right is Preview
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(12)

        # Left Column: Tabs for Sections
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(0, 0, 0, 0)

        self.tab_widget = QTabWidget()
        self.tab_widget.setStyleSheet("""
            QTabBar::tab {
                font-weight: bold;
                padding: 8px 12px;
            }
        """)

        # Tab: Contact & Summary
        contact_scroll = QScrollArea()
        contact_scroll.setWidgetResizable(True)
        contact_container = QWidget()
        v_contact = QVBoxLayout(contact_container)

        self.form_contact = ContactForm()
        self.form_contact.data_changed.connect(self._on_form_changed)
        v_contact.addWidget(self.form_contact)

        lbl_summary = QLabel("<b>Target Professional Summary:</b><br><span style='color: #6b7280; font-size: 8.5pt;'>3-4 sentences summarizing your core strengths, experience level, and proven value.</span>")
        v_contact.addWidget(lbl_summary)
        self.txt_summary = QTextEdit()
        self.txt_summary.setPlaceholderText("Results-driven engineer with 4+ years of experience architecting high-throughput applications...")
        self.txt_summary.setMinimumHeight(100)
        self.txt_summary.textChanged.connect(self._on_form_changed)
        v_contact.addWidget(self.txt_summary)
        v_contact.addStretch()

        contact_scroll.setWidget(contact_container)
        self.tab_widget.addTab(contact_scroll, "Contact & Summary")

        # Tab: Experience
        exp_scroll = QScrollArea()
        exp_scroll.setWidgetResizable(True)
        self.editor_experience = ExperienceEditor()
        self.editor_experience.data_changed.connect(self._on_form_changed)
        exp_scroll.setWidget(self.editor_experience)
        self.tab_widget.addTab(exp_scroll, "Work Experience")

        # Tab: Skills
        skills_scroll = QScrollArea()
        skills_scroll.setWidgetResizable(True)
        self.editor_skills = SkillsEditor()
        self.editor_skills.data_changed.connect(self._on_form_changed)
        skills_scroll.setWidget(self.editor_skills)
        self.tab_widget.addTab(skills_scroll, "Skills & Tech")

        # Tab: Education
        edu_scroll = QScrollArea()
        edu_scroll.setWidgetResizable(True)
        self.editor_education = EducationEditor()
        self.editor_education.data_changed.connect(self._on_form_changed)
        edu_scroll.setWidget(self.editor_education)
        self.tab_widget.addTab(edu_scroll, "Education")

        left_layout.addWidget(self.tab_widget)
        main_layout.addWidget(left_panel, 50)

        # Right Column: Live WebEngine Preview
        self.preview_widget = PreviewWidget()
        self.preview_widget.theme_changed.connect(self._on_theme_changed)
        main_layout.addWidget(self.preview_widget, 50)

    def _sync_model_from_ui(self):
        """Pulls current form values into self.current_resume."""
        self.current_resume.contact = self.form_contact.get_data()
        self.current_resume.summary = self.txt_summary.toPlainText().strip()
        self.current_resume.experience = self.editor_experience.get_data()
        self.current_resume.education = self.editor_education.get_data()
        self.current_resume.skill_categories = self.editor_skills.get_data()

    def _load_resume_into_ui(self, resume: Resume):
        """Loads a Resume model object into the UI inputs."""
        self.current_resume = resume
        self.form_contact.set_data(resume.contact)
        self.txt_summary.setPlainText(resume.summary)
        self.editor_experience.set_data(resume.experience)
        self.editor_education.set_data(resume.education)
        self.editor_skills.set_data(resume.skill_categories)
        self.preview_widget.update_preview(resume)

    def _on_form_changed(self):
        self._sync_model_from_ui()
        self.preview_widget.update_preview(self.current_resume)

    def _on_theme_changed(self, theme_key: str):
        self.current_resume.selected_theme = theme_key

    def _on_new(self):
        reply = QMessageBox.question(
            self, "New Resume",
            "Are you sure you want to create a new blank resume? Unsaved changes will be lost.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.current_file_path = ""
            self._load_resume_into_ui(Resume())

    def _on_load_sample(self):
        self.current_file_path = ""
        self._load_resume_into_ui(get_sample_software_engineer_resume())

    def _on_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open Resume Draft", "", "JSON Files (*.json)")
        if path:
            try:
                res = load_resume_from_file(path)
                self.current_file_path = path
                self._load_resume_into_ui(res)
            except Exception as e:
                QMessageBox.critical(self, "Error Loading File", f"Could not open draft:\n{e}")

    def _on_save(self):
        if not self.current_file_path:
            self._on_save_as()
        else:
            self._sync_model_from_ui()
            save_resume_to_file(self.current_resume, self.current_file_path)
            self.statusBar().showMessage(f"Saved to {self.current_file_path}", 3000)

    def _on_save_as(self):
        self._sync_model_from_ui()
        default_name = f"{self.current_resume.contact.full_name or 'Resume'}_Draft.json".replace(" ", "_")
        path, _ = QFileDialog.getSaveFileName(self, "Save Resume Draft", default_name, "JSON Files (*.json)")
        if path:
            self.current_file_path = path
            save_resume_to_file(self.current_resume, path)
            self.statusBar().showMessage(f"Saved to {path}", 3000)

    def _open_job_matcher(self):
        self._sync_model_from_ui()
        dialog = JobMatchDialog(self.current_resume, self)
        dialog.exec()

    def _open_advisor(self):
        self._sync_model_from_ui()
        dialog = AdvisorDialog(self.current_resume, self)
        dialog.exec()
