# Copyright (c) 2025, Patel Aasif Khan and contributors
# For license information, please see license.txt

# import frappe
from annotated_types import doc
from frappe.model.document import Document


class StoneDimension(Document):
	def before_save(self):
		tmp = f"{self.shape or ''}-{self.cut or ''}-{self.origin or ''}-{self.purity or ''}-{self.gradecolour or ''}-{self.stone_type or ''}-{str(self.length)}x{str(self.width)}x{str(self.height)}"
		self.name = tmp
