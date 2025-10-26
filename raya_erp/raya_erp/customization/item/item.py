import frappe
import re
from erpnext.stock.doctype.item.item import Item
from frappe.model.naming import make_autoname

class CustomItem(Item):
    def validate_attributes(self):
        pass

def custom_item_autoname(self, method=None):
    """
    Custom naming for Item Doctype.
    Format: RY-{custom_product_master}-{####}
    """
    if self.custom_product_master:
        prefix = f"RY-{self.custom_product_master}-"
        self.name = make_autoname(prefix + ".####")
    else:
        # fallback to default
        self.name = make_autoname("RY-ITEM-.####")

def after_insert(self, method=None):
    pass

def before_save(self,method=None):
    if self.item_group == "Rings":
        self.stone_carat_wt = calculate_stone_collection(self)
        self.stones_weight = self.stone_carat_wt * 0.2
        self.net_weight = self.gross_weight - self.stones_weight
        metal = frappe.get_doc("Metal Type", self.metal_type)
        self.custom_net_weight_metal = self.net_weight * metal.gram_covers

def calculate_stone_collection(self):
    stones_weight = 0.0
    stone_collections = {}

    for i in self.custom_variant_attributes:
        if i.attribute == "Metal":
            self.metal_type = i.custom_value
        if i.custom_stone_id:
            if i.custom_stone_id not in stone_collections:
                stone_collections[i.custom_stone_id] = {}
            stone_collections[i.custom_stone_id][i.attribute] = i.custom_value
        else:
            if i.attribute == "Band":
                band = frappe.get_doc("Ring Attributes", i.custom_value)
                stones_weight = stones_weight + band.total_weight_in_ct

            if i.attribute == "Halo":
                halo = frappe.get_doc("Ring Attributes", i.custom_value)
                stones_weight = stones_weight + halo.total_weight_in_ct
    
    custom_stones_list = []
    for stone_collection in stone_collections.values():
        if stone_collection.get("Shape") and stone_collection.get("Stone Family") and stone_collection.get("Size"):
            if stone_collection["Size"][-2:] == "ct":
                stones_weight = stones_weight + float(stone_collection["Size"][:-2])
                sd = frappe.get_doc("Stone Dimension", {
                        "Shape": stone_collection["Shape"],
                        "stone_type": stone_collection["Stone Family"],
                        "estimated_weight_ct": round(float(stone_collection["Size"][:-2]),3)
                    })
                custom_stones_list.append(sd.name)
            else:
                #split size by x and get estimated weight from Stone Dimensions
                length = stone_collection["Size"].split("x")[0]
                width = stone_collection["Size"].split("x")[1] if "x" in stone_collection["Size"] else None
                height = stone_collection["Size"].split("x")[2] if stone_collection["Size"].count("x") == 2 else None
                if height:
                    sd = frappe.get_doc("Stone Dimension", {
                        "Shape": stone_collection["Shape"],
                        "stone_type": stone_collection["Stone Family"],
                        "length": round(float(length),3),
                        "width": round(float(width),3),
                        "height": round(float(height),3)
                    })
                    custom_stones_list.append(sd.name)
                    stones_weight = stones_weight + float(sd.estimated_weight_ct)
                else:
                    sd = frappe.get_doc("Stone Dimension", {
                        "Shape": stone_collection["Shape"],
                        "stone_type": stone_collection["Stone Family"],
                        "length": round(float(length),3),
                        "width": round(float(width),3)
                    })
                    stones_weight = stones_weight + float(sd.estimated_weight_ct)
                    custom_stones_list.append(sd.name)

    self.custom_stones = str(custom_stones_list)
    print("Total Stones Weight: ", stones_weight)
    return stones_weight


def update_price(self):
    pass

def get_stone_details(self):
    pass

def update_metal_price(self):
    pass

@frappe.whitelist()
def fetch_metal_price(name):
    try:
        item = frappe.get_doc("Item", name)
        for i in item.custom_variant_attributes:
            if i.attribute == "Metal":
                metal_type = i.custom_value
                break
        parts = metal_type.split('-')
        rate = frappe.db.get_value("Raya Price List", {"metal_type": parts[0],"purity": str(parts[1])+"kt"}, "rate_per_gm")
        return rate
    except Exception as e:
        return 0
    
@frappe.whitelist()
def fetch_stone_price(name):
    try:
        stone_list = frappe.get_doc("Item", name).custom_stones
        list_stones = stone_list.strip("[]").replace("'", "").split(", ")
        price = 0.0
        total_stone_price = 0.0
        for i in list_stones:
                stone = frappe.get_doc("Stone Dimension", i)
                price = price + stone.price
        return price
    except Exception as e:
        return 0