import frappe
import re
from erpnext.stock.doctype.item.item import Item

class CustomItem(Item):
    def validate_attributes(self):
        print(".........................Custom validate_attributes called..........................")
        pass

def after_insert(self, method=None):
    pass

def before_save(self,method=None):
    if self.item_group == "Rings":
        self.stones_weight = calculate_stone_collection(self) * 0.2
        self.net_weight = self.gross_weight - self.stones_weight
        metal = frappe.get_doc("Metal Type", self.metal_type)
        self.custom_net_weight_metal = self.net_weight * metal.gram_covers

def calculate_stone_collection(self):
    stones_weight = 0.0
    stone_collections = {}

    for i in self.attributes:
        if i.attribute == "Metal":
            self.metal_type = i.value
        if i.stone_id:
            if i.stone_id not in stone_collections:
                stone_collections[i.stone_id] = {}
            stone_collections[i.stone_id][i.attribute] = i.value
        else:
            if i.attribute == "Band":
                band = frappe.get_doc("Ring Attributes", i.value)
                tmp = int(match.group(0)) if (match := re.match(r'\d+', band.dimension)) else None
                stones_weight = stones_weight + (tmp * band.no_of_stones)

            if i.attribute == "Halo":
                halo = frappe.get_doc("Ring Attributes", i.value)
                tmp = int(match.group(0)) if (match := re.match(r'\d+', halo.dimension)) else None
                stones_weight = stones_weight + (tmp * halo.no_of_stones)
    
    print(stone_collections)
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
    return stones_weight


def update_price(self):
    pass

def get_stone_details(self):
    pass

def update_metal_price(self):
    pass

@frappe.whitelist()
def fetch_metal_price(name):
    print("Fetching metal price for item:", name,'------------------')
    try:
        item = frappe.get_doc("Item", name)
        for i in item.attributes:
            if i.attribute == "Metal":
                metal_type = i.value
                break
        parts = metal_type.split('-')
        rate = frappe.db.get_value("Raya Price List", {"metal_type": parts[0],"purity": str(parts[1])+"kt"}, "rate_per_gm")
        return rate
    except Exception as e:
        print("Error fetching metal price:", e)
        return 0
    
@frappe.whitelist()
def fetch_stone_price(name):
    try:
        stone_list = frappe.get_doc("Item", name).custom_stones
        print("Fetching stone price for item:", stone_list,'------------------',list(stone_list))
        list_stones = stone_list.strip("[]").replace("'", "").split(", ")   
        price = 0.0
        total_stone_price = 0.0
        for i in list_stones:
                stone = frappe.get_doc("Stone Dimension", i)
                price = price + stone.price
        return price
    except Exception as e:
        print("Error fetching stone price:", e)
        return 0