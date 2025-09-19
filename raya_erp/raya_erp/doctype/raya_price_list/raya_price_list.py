# Copyright (c) 2025, Patel Aasif Khan and contributors
# For license information, please see license.txt

import frappe
from frappe import _
import re
from frappe.model.document import Document
from raya_erp.raya_erp.doctype.raya_price_list.api.market_rate import get_now_date


class RayaPriceList(Document):
    def before_insert(self):
        self.set_name_field()
        self.validate_duplicate()

    def on_update(self):
        self.check_width_height()
        if self.live_rate:
            self.update_price_list_for_metal()
        else:
            self.update_price_list_for_stone()

    def set_name_field(self):
        if not self.live_rate:
            self.list_rate_id = self.stone_type + "-" + self.stone_shape
        else:
            self.list_rate_id = (
                self.metal_type + "-" + self.purity + "-" + str(self.date_updated)
            )

    def validate_duplicate(self):
        exists = frappe.db.exists(
            "Raya Price List",
            {
                "metal_type": self.metal_type,
                "date_updated": get_now_date("America/Denver"),
                "purity": self.purity,
            },
        )
        if exists:
            frappe.throw(
                _("Duplicate entry for the Date {} : {}").format(
                    self.date_updated, exists
                )
            )

    def check_width_height(self):
        if (
            not self.live_rate
            and self.weight_carat >= 5
            and not (self.length and self.width)
        ):
            frappe.throw(_("Mandatory field required Length or Width."))

    def update_price_list_for_metal(self):
        all_item = frappe.db.sql(
            """
                SELECT iva.parent AS item_code
                FROM `tabItem Variant Attribute` iva
                WHERE (iva.attribute = "Metal Type" AND iva.attribute_value = %(metal_type)s)
                OR (iva.attribute = "Purity" AND iva.attribute_value = %(metal_purity)s)
                GROUP BY iva.parent
                HAVING COUNT(DISTINCT iva.attribute) = 2;
            """,
            {"metal_type": self.metal_type, "metal_purity": self.purity},
            as_dict=True,
        )
        for item in all_item:
            item_doc = frappe.get_doc("Item", item.get("item_code"))

            if not item_doc.has_variants:
                item_doc.save(ignore_permissions=True)
                # if item_doc.stock_uom == "Gram":
                #     net_wt, stone_wt = calculate_net_weight(item_doc.gross_weight,item_doc.stone_carat_wt)
                #     final_price = net_wt * self.rate_per_gm
                # else:
                #     #other UOM
                #     final_price = 0.0

                # update_price_list(item.get("item_code"), final_price, qty=net_wt)

    def update_price_list_for_stone(self):
        all_item = frappe.db.get_all(
            "Stone Details", {"price_list": self.name}, pluck="parent"
            )
        for item in all_item:
            item_doc = frappe.get_doc("Item", item)

            if not item_doc.has_variants:
                item_doc.save(ignore_permissions=True)


def get_metal_price(metal_name, purity):
    karat = re.search(r"\d+", purity)
    purity = karat.group() if karat else "0"
    price_data = frappe.db.get_all(
        "Raya Price List",
        {"metal_type": metal_name, "purity": purity + "kt"},
        ["name", "metal_type as metal_name", "purity", "weight_gm", "rate_per_gm"],
        order_by="modified desc",
        limit=1,
    )
    if len(price_data) > 0:
        return price_data[0]

    return price_data


def get_stone_price(
    stone_type,
    stone_shape,
    stone_colour,
    stone_clarity,
    sieve_size=None,
    length=None,
    width=None,
):
    filters = {
        "stone_type": stone_type,
        "stone_shape": stone_shape,
        "stone_colour": stone_colour,
        "stone_clarity": stone_clarity,
    }
    if not sieve_size:
        filters.update({"length": length, "width": width})
    else:
        filters.update({"sieve_size": sieve_size})

    price_data = frappe.db.get_all(
        "Raya Price List",
        filters,
        [
            "name",
            "stone_type as stone_name",
            "stone_shape",
            "stone_colour",
            "stone_clarity",
            "weight_carat",
            "stone_rate",
        ],
        order_by="modified desc",
        limit=1,
    )
    if price_data:
        return price_data[0]

    return price_data


def update_price_list(item_code, price, type="Metal", labor=0, qty=0):
    """
    Method to update rate of the Items in item price list.
    """
    ip_exists = frappe.db.exists(
        "Item Price", {"item_code": item_code, "price_list": "Standard Selling"}
    )
    if type == "Metal":
        rate_of = "metal_price"
    else:
        rate_of = "stones_price"

    if not ip_exists:
        doc = frappe.new_doc("Item Price")
        doc.item_code = item_code
        doc.price_list = "Standard Selling"
        if qty:
            doc.packing_unit = qty
        if labor:
            doc.labor_rate = labor
        setattr(doc, rate_of, price)
        doc.insert(ignore_permissions=True)
    else:
        doc = frappe.get_doc("Item Price", ip_exists)
        if qty:
            doc.packing_unit = qty
        if labor:
            doc.labor_rate = labor
        setattr(doc, rate_of, price)
        doc.save(ignore_permissions=True)


def calculate_net_weight(gross_weight, wt_in_carat):
    stones_weight = wt_in_carat * 0.2
    net_weight = gross_weight - stones_weight
    return net_weight, stones_weight
