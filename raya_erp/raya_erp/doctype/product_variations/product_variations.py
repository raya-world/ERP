# Copyright (c) 2025, Patel Aasif Khan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from itertools import product

class ProductVariations(Document):

	def before_save(self):
		# Custom logic before saving the document
		self.validate_variation_fields()
		self.set_values_variation_fields()

	def validate_variation_fields(self):
		# Implement your validation logic here
		list_keys_metal = {}
		list_keys_stone = {}

		for i in self.table_lrpq:
			print(f"Key {i.key}, Value: {i.value}, will_impact_metal {i.will_impact_metal}, will_impact_stone {i.will_impact_gem}, will_impact_gem {i.will_impact_gem}")
			
			if i.will_impact_metal:
				if ',' in i.value:
					list_keys_metal[i.key] = [v.strip() for v in i.value.split(',')]
				else:
					list_keys_metal[i.key] = [i.value]

			if i.will_impact_gem:
				if ',' in i.value:
					list_keys_stone[i.key] = [v.strip() for v in i.value.split(',')]
				else:
					list_keys_stone[i.key] = [i.value]

		print(f"Metal Keys: {list_keys_metal}, Stone Keys: {list_keys_stone}")

		# Create a list of dictionaries for each combination of metal-impacting values
		self.pnc_of_metal = self._generate_combinations(list_keys_metal)
		self.pnc_of_stone = self._generate_combinations(list_keys_stone)

		print("Metal Combinations:")
		for item in self.pnc_of_metal:
			print(item)
		
		print("Stone Combinations:")
		for item in self.pnc_of_stone:
			print(item)

	def _generate_combinations(self, input_dict):
		if not input_dict:
			return []

		keys = list(input_dict.keys())
		values = list(input_dict.values())

		# Cartesian product of all value lists
		combinations = list(product(*values))

		# Convert each combination tuple to a dictionary
		result = [dict(zip(keys, combo)) for combo in combinations]

		return result

	def set_values_variation_fields(self):
		# Clear previous entries in the child table (optional but recommended)
		self.table_vvft = []

		# Handle metal combinations
		for i in self.pnc_of_metal:
			tmp = str(i)
			key = tmp.replace("{", "").replace("}", "").replace("'", "")
			self.append("table_vvft", {
				"combination": key			
			})

		# Handle stone combinations
		for i in self.pnc_of_stone:
			tmp = str(i)
			key = tmp.replace("{", "").replace("}", "").replace("'", "")
			self.append("table_vvft", {
				"combination": key
			})

			