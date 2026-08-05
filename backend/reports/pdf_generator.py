class PDFGenerator:
	"""Stub PDF generator. Real implementation should use ReportLab.

	This class intentionally does not implement generation logic —
	it provides the expected interface for `ReportService` wiring.
	"""

	def generate(self, report_data, output_path):
		"""Generate a PDF report.

		Args:
			report_data: The report payload/data structure.
			output_path: Destination file path for the generated PDF.

		Raises:
			NotImplementedError: Indicates generation is not implemented here.
		"""
		raise NotImplementedError(
			"PDF generation not implemented. Provide implementation using ReportLab."
		)

