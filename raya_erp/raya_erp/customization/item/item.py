import frappe
from raya_erp.raya_erp.doctype.raya_price_list.raya_price_list import (
    get_stone_price, 
    update_price_list, 
    get_metal_price, 
    calculate_net_weight)

def after_insert(self, method=None):
    update_price(self)

def before_save(self,method=None):
    if not self.gross_weight:
        frappe.throw("Mandatory field required Gross Weight.")

    if not self.is_new():
        update_price(self)

def update_price(self):
    if not self.has_variants:
        total_stone_price = get_stone_details(self)
        
        self.net_weight, self.stones_weight = calculate_net_weight(self.gross_weight, self.stone_carat_wt)
        update_metal_price(self)
        update_price_list(self.name, total_stone_price, type="Stone")

def get_stone_details(self):
    total_stone_price = 0
    price_not_listed = []
    self.stone_carat_wt = 0
    for stone in self.stone_details:
        self.stone_carat_wt += stone.carat_weight
        price_data = get_stone_price(
            stone.stone_type,
            stone.stone_shape,
            stone.stone_colour,
            stone.stone_clarity,
            sieve_size=stone.sieve_size,
            length=stone.length,
            width=stone.width,
        )
        if price_data:
            total_stone_price += price_data.get("stone_rate") * stone.carat_weight
            stone.price_list = price_data.get("name")
        else:
            price_not_listed.append(stone.idx)
    

    if len(price_not_listed) > 1:
        formatted_string = "Rows "+", ".join(map(str, price_not_listed[:-1])) + f" and {price_not_listed[-1]}"
    else:
        formatted_string ="Row "+ str(price_not_listed[0]) if price_not_listed else ""

    if formatted_string:
        frappe.throw("<b>{0}:</b> Raya Price List not found for the given Stone Config at <b>{1}</b>".format(self.name, formatted_string))
    
    return total_stone_price

def update_metal_price(self):
    metal_name = ""
    purity = ""
    for att in self.attributes:
        if att.attribute == "Metal Type":
            metal_name = att.attribute_value
        if att.attribute == "Purity":
            purity = att.attribute_value
    
    if metal_name and purity:
        metal_price = get_metal_price(metal_name, purity)
        if metal_price:
            total_price = metal_price.get("rate_per_gm") * self.net_weight
            total_labor = self.labor_rate * self.gross_weight
            update_price_list(self.name,total_price,labor=total_labor,qty=self.net_weight)