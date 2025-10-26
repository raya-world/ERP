from frappe.custom.doctype.custom_field.custom_field import create_custom_fields

custom_fields = {
    "Item": [
        {
            "label": "Is In Stock",
            "fieldname": "custom_is_in_stock",
            "insert_after": "is_stock_item",
            "default": "1",
            "fieldtype": "Check",
        },
    ],
    "Serial No":[
        {
            "label":"Product Info",
            "fieldname": "custom_product_info",
            "insert_after": "purchase_document_no",
            "fieldtype": "Section Break",
        },
        {
            "label": "Gross Weight",
            "fieldname": "custom_gross_weight",
            "insert_after": "custom_product_info",
            "fieldtype": "Float",
        },
        {
            "label": "Net Weight",
            "fieldname": "custom_net_weight",
            "insert_after": "custom_gross_weight",
            "fieldtype": "Float",
        },
        {
            "label": "Pure Weight",
            "fieldname": "custom_pure_weight",
            "insert_after": "custom_net_weight",
            "fieldtype": "Float",
        },
        {
            "label": "All Stone Value",
            "fieldname": "custom_total_stone_value",
            "insert_after": "custom_pure_weight",
            "fieldtype": "Currency",
        },
        {
            "label": "Stone Details",
            "fieldname": "custom_stone_detials",
            "insert_after": "custom_pure_weight",
            "fieldtype": "Table",
            "Options":"Stone Details"
        },

    ]
}

def execute():
    create_custom_fields(custom_fields)