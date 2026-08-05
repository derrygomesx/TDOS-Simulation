class WordGenerator:
	"""Stub Word generator. Real implementation should use python-docx.

	This class intentionally does not implement generation logic —
	it provides the expected interface for `ReportService` wiring.
	"""

	def generate(self, report_data, output_path):
		"""Generate a Word report.

		Args:
			report_data: The report payload/data structure.
			output_path: Destination file path for the generated Word document.

		Raises:
			NotImplementedError: Indicates generation is not implemented here.
		"""
		raise NotImplementedError(
			"Word generation not implemented. Provide implementation using python-docx."
		)

