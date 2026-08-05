from typing import Any

from .pdf_generator import PDFGenerator
from .excel_generator import ExcelGenerator
from .word_generator import WordGenerator


class ReportFactory:
	"""Factory that returns a concrete report generator instance based on type.

	Supported types: PDF, EXCEL, WORD (case-insensitive).
	"""

	def get_generator(self, report_type: str) -> Any:
		if not report_type:
			raise ValueError("report_type must be provided")

		t = report_type.strip().lower()

		if t == "pdf":
			return PDFGenerator()

		if t in ("excel", "xlsx", "xls"):
			return ExcelGenerator()

		if t in ("word", "docx"):
			return WordGenerator()

		raise ValueError(f"Unsupported report type: {report_type}")

