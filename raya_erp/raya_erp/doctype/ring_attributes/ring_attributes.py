# Copyright (c) 2025, Patel Aasif Khan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class RingAttributes(Document):
	def before_save(self):
		weight = 0
		if self.dimension[-2:] == "ct":
			weight = weight + float(self.dimension[:-2])
		else:
			length = self.dimension.split("x")[0]
			width = self.dimension.split("x")[1] if "x" in self.dimension else None
			height = self.dimension.split("x")[2] if self.dimension.count("x") == 2 else None
			if height:
				sd = frappe.get_doc("Stone Dimension", {
					"Shape": self.shape,
					"stone_type": self.family,
					"length": round(float(length),3),
					"width": round(float(width),3),
					"height": round(float(height),3)
				})
				weight = weight + float(sd.estimated_weight_ct)
			else:
				sd = frappe.get_doc("Stone Dimension", {
					"Shape": self.shape,
					"stone_type": self.family,
					"length": round(float(length),3),
					"width": round(float(width),3)
				})
				weight = weight + float(sd.estimated_weight_ct)

		self.total_weight_in_ct = self.no_of_stones * weight
