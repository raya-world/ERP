import frappe

def before_save(self,method=None):
    stone_weight_in_ct = 0
    total_stone_value = 0
    for i in self.custom_stone_detials:
        stone_weight_in_ct = stone_weight_in_ct + (i.carat_weight * i.no_of_stones)
        i.stone_value = i.stone_rate * (i.carat_weight * i.no_of_stones)
        i.labour_value = i.labour_rate * (i.carat_weight * i.no_of_stones)
        total_stone_value = total_stone_value + i.stone_value

    self.custom_net_weight = self.custom_gross_weight - (stone_weight_in_ct * 0.2)
    item = frappe.get_doc("Item Variant Attribute", {"parent":self.item_code.split(":")[0],"attribute":"Metal"})
    metal = frappe.get_doc("Metal Type", item.custom_value)
    self.custom_pure_weight = self.custom_net_weight * metal.gram_covers
    self.custom_total_stone_value = total_stone_value

