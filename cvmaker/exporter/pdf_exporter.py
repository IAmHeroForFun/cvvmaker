"""
Offline PDF Exporter using PySide6 QtWebEngineWidgets.
Renders HTML/CSS into a 300 DPI, print-accurate PDF file.
"""
import os
from PySide6.QtCore import QEventLoop, QMarginsF
from PySide6.QtGui import QPageLayout, QPageSize
from PySide6.QtWebEngineCore import QWebEnginePage


class PdfExporter:
    @staticmethod
    def export_html_to_pdf(html_content: str, output_path: str, page_size: QPageSize.PageSizeId = QPageSize.PageSizeId.A4) -> bool:
        """
        Renders HTML to PDF synchronously using a temporary offscreen QWebEnginePage.
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        page = QWebEnginePage()
        loop = QEventLoop()
        
        # Track HTML load completion
        page.loadFinished.connect(lambda ok: loop.quit())
        page.setHtml(html_content)
        loop.exec()

        # Setup standard layout: 12mm margins
        layout = QPageLayout(
            QPageSize(page_size),
            QPageLayout.Orientation.Portrait,
            QMarginsF(12, 12, 12, 12),
            QPageLayout.Unit.Millimeter
        )

        pdf_loop = QEventLoop()
        success_flag = [False]

        def on_pdf_finished(file_path: str, success: bool):
            success_flag[0] = success
            pdf_loop.quit()

        page.pdfPrintingFinished.connect(on_pdf_finished)
        page.printToPdf(output_path, layout)
        pdf_loop.exec()

        return success_flag[0] and os.path.exists(output_path) and os.path.getsize(output_path) > 0
