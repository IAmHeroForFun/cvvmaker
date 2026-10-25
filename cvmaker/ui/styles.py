"""
Universal application-wide stylesheet.
Forces crisp, readable contrast regardless of whether the user OS runs in Dark or Light mode.
"""

APP_STYLESHEET = """
/* Base Window & Dialogs */
QMainWindow, QDialog, QWidget#centralWidget {
    background-color: #f8fafc;
    color: #0f172a;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 13px;
}

/* ToolBar */
QToolBar {
    background-color: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    padding: 6px;
    spacing: 8px;
}

QToolButton {
    background-color: #ffffff;
    color: #1e293b;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 6px 12px;
    font-weight: 600;
}

QToolButton:hover {
    background-color: #f1f5f9;
    border-color: #94a3b8;
}

/* Tabs */
QTabWidget::pane {
    border: 1px solid #cbd5e1;
    background-color: #ffffff;
    border-radius: 4px;
}

QTabBar::tab {
    background-color: #e2e8f0;
    color: #334155;
    font-weight: 600;
    padding: 8px 16px;
    margin-right: 2px;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
}

QTabBar::tab:selected {
    background-color: #ffffff;
    color: #1e40af;
    border: 1px solid #cbd5e1;
    border-bottom: none;
}

/* Scroll Areas & Containers */
QScrollArea {
    background-color: #ffffff;
    border: none;
}

QScrollArea > QWidget > QWidget {
    background-color: #ffffff;
}

/* Text & Form Inputs */
QLabel {
    color: #1e293b;
    font-size: 13px;
}

QLineEdit, QTextEdit, QPlainTextEdit {
    background-color: #ffffff !important;
    color: #0f172a !important;
    border: 1px solid #94a3b8;
    border-radius: 5px;
    padding: 6px 8px;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
    font-size: 13px;
}

QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
    border: 1.5px solid #2563eb;
    background-color: #ffffff !important;
    color: #0f172a !important;
}

/* Group Boxes (Cards) */
QGroupBox {
    background-color: #f8fafc;
    border: 1.5px solid #cbd5e1;
    border-radius: 6px;
    margin-top: 18px;
    padding: 14px 10px 10px 10px;
    font-weight: 700;
    color: #0f172a;
}

QGroupBox::title {
    subcontrol-origin: margin;
    subcontrol-position: top left;
    left: 12px;
    padding: 0 4px;
    color: #1e40af;
    background-color: #f8fafc;
}

/* Buttons */
QPushButton {
    background-color: #f1f5f9;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 5px;
    padding: 6px 14px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #e2e8f0;
    border-color: #94a3b8;
}

/* Combo Box */
QComboBox {
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 5px 10px;
    font-weight: 500;
}

QComboBox QAbstractItemView {
    background-color: #ffffff;
    color: #0f172a;
    selection-background-color: #2563eb;
    selection-color: #ffffff;
    border: 1px solid #cbd5e1;
}

/* Lists & Trees */
QListWidget {
    background-color: #ffffff;
    color: #0f172a;
    border: 1px solid #cbd5e1;
    border-radius: 4px;
    padding: 4px;
}

QListWidget::item:selected {
    background-color: #e0e7ff;
    color: #1e3a8a;
}
"""
