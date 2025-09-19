import frappe

def before_insert(doc, method=None):
    if doc.is_base_attribute:
        for att in doc.item_attribute_values:
            if not frappe.db.exists("Attribute Type",att.attribute_value):
                doc = frappe.new_doc("Attribute Type")
                doc.attribute_value = att.attribute_value
                doc.insert(ignore_permissions=True)