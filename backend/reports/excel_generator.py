class ExcelGenerator:
	"""Stub Excel generator. Real implementation should use openpyxl.

	This class intentionally does not implement generation logic —
	it provides the expected interface for `ReportService` wiring.
	"""

	def generate(self, report_data, output_path):
		"""Generate an Excel report.

		Args:
			report_data: The report payload/data structure.
			output_path: Destination file path for the generated Excel file.

		Raises:
			NotImplementedError: Indicates generation is not implemented here.
		"""
		raise NotImplementedError(
			"Excel generation not implemented. Provide implementation using openpyxl."
		)

