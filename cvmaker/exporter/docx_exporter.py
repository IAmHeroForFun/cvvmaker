"""
Offline DOCX Exporter.
Converts rendered HTML resume to genuine Microsoft Word (.docx) format
using headless LibreOffice with the Open XML export filter.
"""
import os
import shutil
import tempfile
import subprocess
from typing import Tuple


class DocxExporter:
    @staticmethod
    def is_available() -> bool:
        """Check if libreoffice executable is installed in path."""
        return shutil.which("libreoffice") is not None

    @classmethod
    def export_html_to_docx(cls, html_content: str, output_path: str) -> Tuple[bool, str]:
        """
        Converts HTML to DOCX using headless LibreOffice.
        Returns (success: bool, message: str).
        """
        if not cls.is_available():
            return False, "LibreOffice is not installed. Please install libreoffice to enable DOCX export."

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)

        with tempfile.TemporaryDirectory() as tmpdir:
            temp_html = os.path.join(tmpdir, "resume.html")
            with open(temp_html, "w", encoding="utf-8") as f:
                f.write(html_content)

            cmd = [
                "libreoffice",
                "--headless",
                "--convert-to",
                "docx:Office Open XML Text",
                temp_html,
                "--outdir",
                tmpdir
            ]

            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
                generated_docx = os.path.join(tmpdir, "resume.docx")

                if result.returncode == 0 and os.path.exists(generated_docx):
                    shutil.copy2(generated_docx, output_path)
                    return True, "Exported successfully."
                else:
                    return False, f"Conversion failed: {result.stderr or result.stdout}"
            except Exception as e:
                return False, f"Error during export: {str(e)}"
