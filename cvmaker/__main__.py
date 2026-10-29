"""
Entry point for CV Maker desktop application.
"""
import os
import sys

# Ensure UTF-8 locale so xkbcommon compose table finds valid locale maps
if not os.environ.get("LC_ALL"):
    os.environ["LC_ALL"] = "en_US.UTF-8"
if not os.environ.get("LANG"):
    os.environ["LANG"] = "en_US.UTF-8"

# Silence low-level Chromium driver notices (like GBM/Vulkan fallback) printed to stderr
def _suppress_c_stderr():
    try:
        devnull = os.open(os.devnull, os.O_WRONLY)
        old_stderr = os.dup(2)
        os.dup2(devnull, 2)
        return old_stderr, devnull
    except Exception:
        return None, None

def _restore_c_stderr(old_stderr, devnull):
    if old_stderr is not None:
        try:
            os.dup2(old_stderr, 2)
            os.close(old_stderr)
            os.close(devnull)
        except Exception:
            pass

# Temporarily silence during QtWebEngine initialization
_old_err, _dnull = _suppress_c_stderr()

from PySide6.QtWidgets import QApplication
from PySide6.QtWebEngineWidgets import QWebEngineView

_restore_c_stderr(_old_err, _dnull)

from .ui.main_window import MainWindow
from .ui.styles import APP_STYLESHEET


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("CVMaker")
    app.setOrganizationName("CVMaker")
    app.setStyleSheet(APP_STYLESHEET)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

