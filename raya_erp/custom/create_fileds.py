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
    "Item Variant Attribute": [
        {
            "label": "Stone Family",
            "fieldname": "custom_stone_family",
            "insert_after": "custom_value",
            "fieldtype": "Data",
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
            "label": "Metal Rate",
            "fieldname": "custom_metal_rate",
            "insert_after": "custom_pure_weight",
            "fieldtype": "Float",
        },
        {
            "label": "",
            "fieldname": "custom_column_break",
            "insert_after": "custom_metal_rate",
            "fieldtype": "Column Break",
        },
        {
            "label": "Labour Rate on",
            "fieldname": "custom_labour_rate_on",
            "insert_after": "custom_column_break",
            "fieldtype": "Select",
            "options": "\nNet\nGross\n",
        },
        {
            "label": "Labour Rate",
            "fieldname": "custom_labour_rate",
            "insert_after": "custom_labour_rate_on",
            "fieldtype": "Float",
        },
        {
            "label": "Labour Value",
            "fieldname": "custom_labour_value",
            "insert_after": "custom_labour_rate",
            "fieldtype": "Float",
        },
        {
            "label": "All Stone Value",
            "fieldname": "custom_total_stone_value",
            "insert_after": "custom_pure_weight",
            "fieldtype": "Currency",
        },
        {
            "label":"",
            "fieldname": "custom_stone_info",
            "insert_after": "custom_total_stone_value",
            "fieldtype": "Section Break",
        },
        {
            "label": "Stone Details",
            "fieldname": "custom_stone_detials",
            "insert_after": "custom_stone_info",
            "fieldtype": "Table",
            "Options":"Stone Details"
        },

    ]
}

def execute():
    create_custom_fields(custom_fields)