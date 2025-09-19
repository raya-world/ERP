# Copyright (c) 2025, Patel Aasif Khan and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from itertools import product


class ProductMaster(Document):

	def before_save(self):
		# Custom logic before saving the selfument
		self.validate_variation_fields()
		self.set_values_variation_fields()
		self.stone_combinations()


	def stone_combinations(self):
		print("======================================================\n")
		"""
		Build Stone Product Master child table from Stone and Stone Shape Combinations
		"""
		self.set("stone_product_master", [])

		# Expand Stone table (split families & shapes)
		stone_expanded = []
		for row in self.stone:
			families = [f.strip() for f in (row.stone_family or "").split(",") if f.strip()]
			shapes = [s.strip() for s in (row.stone_shape or "").split(",") if s.strip()]
			for fam in families:
				for shape in shapes:
					stone_expanded.append({
						"stone_setting_type": row.stone_setting_type,
						"stone_family": fam,
						"stone_shapes": shape,
						"no_of_stone": row.no_of_stone
					})
		# Only for single type i.e. Primary
		for i in stone_expanded:
			for j in self.stone_shape_combinations:
				if i["stone_shapes"] == j.shape and i["stone_setting_type"] == "Primary" and j.stone_category == "Primary":
					pid = f'{j.stone_category[0]}{i["stone_family"][0]}{i["stone_shapes"][0]}'
					self.append("stone_product_master", {
						"product_id": pid.upper(),
						"family": i["stone_family"],
						"stone_category": j.stone_category,
						"shape": j.shape,
						"dimension": j.dimension,
						"no_of_stone": j.no_of_stone,
						# Replace with your actual weight logic
						"weight": j.no_of_stone * 10
					})
		
		# Both for type i.e. Primary & Secondary
		for i in self.stone_product_master:
			print(i)

		
		# Loop through families & match with shape combinations
		# for stone_row in stone_expanded:
		# 	family = stone_row["stone_family"]
		# 	shapes = stone_row["stone_shapes"]

		# 	for shape_row in self.stone_shape_combinations:
		# 		if shape_row.shape not in shapes:
		# 			continue

		# 		# Product ID (base)
		# 		pid = f"{shape_row.stone_category[0]}{family[0]}{shape_row.shape[0]}"

		# 		# Add row
		# 		self.append("stone_product_master", {
		# 			"product_id": pid.upper(),
		# 			"family": family,
		# 			"stone_category": shape_row.stone_category,
		# 			"shape": shape_row.shape,
		# 			"dimension": shape_row.dimension,
		# 			"no_of_stone": shape_row.no_of_stone,
		# 			# Replace with your actual weight logic
		# 			"weight": shape_row.no_of_stone * 10
		# 		})

		# 		# If secondary, create extended product_id variant
		# 		if shape_row.stone_category.startswith("Secondary"):
		# 			pid_sec = f"{pid}-S{shape_row.shape[0]}R"
		# 			self.append("stone_product_master", {
		# 				"product_id": pid_sec.upper(),
		# 				"family": family,
		# 				"stone_category": shape_row.stone_category,
		# 				"shape": shape_row.shape,
		# 				"dimension": shape_row.dimension,
		# 				"no_of_stone": shape_row.no_of_stone,
		# 				"weight": shape_row.no_of_stone * 2
		# 			})

	def validate_variation_fields(self):
		# Implement your validation logic here
		list_keys_metal = {}
		list_keys_stone = {}

		for i in self.stone:
			# print(i)
			key_name = str(i.stone_setting_type) + "-"
			print(key_name)
			if i.impact_stone_shape:
				print(f"Impact Stone Shape: {i.stone_shape}")
				if ',' in i.stone_shape:
					list_keys_stone[str(key_name) + "stone_shape"] = [v.strip() for v in i.stone_shape.split(',')]
				else:
					list_keys_stone[str(key_name) + "stone_shape"] = [i.stone_shape]

			if i.impact_stone_setting:
				if ',' in i.stone_setting_type:
					list_keys_stone[str(key_name) + "stone_setting_type"] = [v.strip() for v in i.stone_setting_type.split(',')]
				else:
					list_keys_stone[str(key_name) + "stone_setting_type"] = [i.stone_setting_type]

			if i.impact_stone_family:
				if ',' in i.stone_family:
					list_keys_stone[str(key_name) + "stone_family"] = [v.strip() for v in i.stone_family.split(',')]
				else:
					list_keys_stone[str(key_name) + "stone_family"] = [i.stone_family]

			if i.impact_stone_nos:
				if ',' in i.no_of_stone:
					list_keys_stone[str(key_name) + "no_of_stone"] = [v.strip() for v in i.no_of_stone.split(',')]
				else:
					list_keys_stone[str(key_name) + "no_of_stone"] = [i.no_of_stone]

			if i.impact_stone_wt:
				if ',' in i.stone_wt:
					list_keys_stone[str(key_name) + "stone_wt"] = [v.strip() for v in i.stone_wt.split(',')]
				else:
					list_keys_stone[str(key_name) + "stone_wt"] = [i.stone_wt]

		for index,i in enumerate(self.metal):
			# print(i)
			key_name = index
			if i.impact_type_of_metal:
				if ',' in i.type_of_metal:
					list_keys_metal[str(key_name) + "type_of_metal"] = [v.strip() for v in i.type_of_metal.split(',')]
				else:
					list_keys_metal[str(key_name) + "type_of_metal"] = [i.type_of_metal]

			if i.impact_finger_size:
				if ',' in i.finger_size:
					list_keys_metal[str(key_name) + "finger_size"] = [v.strip() for v in i.finger_size.split(',')]
				else:
					list_keys_metal[str(key_name) + "finger_size"] = [i.finger_size]
			if i.impact_shank_base_width:
				if ',' in i.shank_base_width:
					list_keys_metal[str(key_name) + "shank_base_width"] = [v.strip() for v in i.shank_base_width.split(',')]
				else:
					list_keys_metal[str(key_name) + "shank_base_width"] = [i.shank_base_width]

			if i.impact_shank_style:
				if ',' in i.shank_style:
					list_keys_metal[str(key_name) + "shank_style"] = [v.strip() for v in i.shank_style.split(',')]
				else:
					list_keys_metal[str(key_name) + "shank_style"] = [i.shank_style]

			if i.impact_metal_colour:
				if ',' in i.metal_colour:
					list_keys_metal[str(key_name) + "metal_colour"] = [v.strip() for v in i.metal_colour.split(',')]
				else:
					list_keys_metal[str(key_name) + "metal_colour"] = [i.metal_colour]

			if i.impact_net_wt:
				if ',' in i.net_wt:
					list_keys_metal[str(key_name) + "net_wt"] = [v.strip() for v in i.net_wt.split(',')]
				else:
					list_keys_metal[str(key_name) + "net_wt"] = [i.net_wt]
			if i.impact_pure_wt:
				if ',' in i.pure_wt:
					list_keys_metal[str(key_name) + "pure_wt"] = [v.strip() for v in i.pure_wt.split(',')]
				else:
					list_keys_metal[str(key_name) + "pure_wt"] = [i.pure_wt]

		print(f"Metal Keys: {list_keys_metal}, Stone Keys: {list_keys_stone}")

		# Create a list of dictionaries for each combination of metal-impacting values
		self.pnc_of_metal = self._generate_combinations(list_keys_metal)
		self.pnc_of_stone = self._generate_combinations(list_keys_stone)

		print("Metal Combinations:")
		# for item in self.pnc_of_metal:
		# 	print(item)
		
		# print("Stone Combinations:")
		# for item in self.pnc_of_stone:
		# 	print(item)

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
		import json	

		# Clear previous entries in the child table
		self.rule_set_mapping = []

		# Helper: Convert dict → ASCII table
		def dict_to_ascii_table(d):
			# Find max lengths for key and value columns
			max_key_len = max(len(str(k)) for k in d.keys())
			max_val_len = max(len(str(v)) for v in d.values())

			# Build horizontal separator
			separator = f"+-{'-' * max_key_len}-+-{'-' * max_val_len}-+"

			# Build rows with proper padding
			rows = [separator]
			for k, v in d.items():
				rows.append(f"| {str(k).ljust(max_key_len)} | {str(v).ljust(max_val_len)} |")
			rows.append(separator)

			return "\n".join(rows)


		# Handle metal combinations
		for i in self.pnc_of_metal:
			self.append("rule_set_mapping", {
				"combination": json.dumps(i),  # keep JSON
				"ascii_table": dict_to_ascii_table(i)  # new Long Text field
			})

		# Handle stone combinations
		for i in self.pnc_of_stone:
			self.append("rule_set_mapping", {
				"combination": json.dumps(i),
				"ascii_table": dict_to_ascii_table(i)
			})

	# def stone_combinations(self):
	# 	"""
	# 	Build Stone Product Master child table from Stone and Stone Shape Combinations
	# 	"""

	# 	# Clear old rows
	# 	self.set("stone_product_master", [])

	# 	# Expand Stone table (split families & shapes)
	# 	stone_expanded = []
	# 	for row in self.stone:
	# 		families = [f.strip() for f in (row.stone_family or "").split(",") if f.strip()]
	# 		shapes = [s.strip() for s in (row.stone_shape or "").split(",") if s.strip()]
	# 		for fam in families:
	# 			stone_expanded.append({
	# 				"stone_setting_type": row.stone_setting_type,
	# 				"stone_family": fam,
	# 				"stone_shapes": shapes,
	# 				"no_of_stone": row.no_of_stone
	# 			})

	# 	counter = 1

	# 	# Loop through families & match with shape combinations
	# 	for stone_row in stone_expanded:
	# 		family = stone_row["stone_family"]
	# 		shapes = stone_row["stone_shapes"]

	# 		for shape_row in self.stone_shape_combinations:
	# 			if shape_row.shape not in shapes:
	# 				continue

	# 			# Product ID (base)
	# 			pid = f"{shape_row.stone_category[0]}{family[0]}{shape_row.shape[0]}"

	# 			# Add row
	# 			self.append("stone_product_master", {
	# 				"no": counter,
	# 				"product_id": pid.upper(),
	# 				"family": family,
	# 				"stone_category": shape_row.stone_category,
	# 				"shape": shape_row.shape,
	# 				"dimension": shape_row.dimension,
	# 				"no_of_stone": shape_row.no_of_stone,
	# 				# Replace with your actual weight logic
	# 				"weight": shape_row.no_of_stone * 10
	# 			})
	# 			counter += 1

	# 			# If secondary, create extended product_id variant
	# 			if shape_row.stone_category.startswith("Secondary"):
	# 				pid_sec = f"{pid}-S{shape_row.shape[0]}R"
	# 				self.append("stone_product_master", {
	# 					"no": counter,
	# 					"product_id": pid_sec.upper(),
	# 					"family": family,
	# 					"stone_category": shape_row.stone_category,
	# 					"shape": shape_row.shape,
	# 					"dimension": shape_row.dimension,
	# 					"no_of_stone": shape_row.no_of_stone,
	# 					"weight": shape_row.no_of_stone * 2
	# 				})
	# 				counter += 1