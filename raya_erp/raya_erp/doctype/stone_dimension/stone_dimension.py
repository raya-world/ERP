# Copyright (c) 2025, Patel Aasif Khan and contributors
# For license information, please see license.txt

# import frappe
from annotated_types import doc
from frappe.model.document import Document


class StoneDimension(Document):
	def before_save(self):
		# {Stone_name}-{Shape}-{Stone_type}-{Cut_Style}-{Clarity_grade}-{Colour_grade}-{length}x{width}x{height}
		tmp = f"{self.family or ''}-{self.shape or ''}-{self.stone_type or ''}-{self.cut or ''}-{self.cut_grade or ''}-{self.gradecolour or ''}-{str(self.length)}x{str(self.width)}x{str(self.height)}"
		self.name = tmp
