# import frappe


def validate(doc, method=None):
    doc.price_list_rate = doc.stones_price + doc.metal_price + doc.labor_rate
