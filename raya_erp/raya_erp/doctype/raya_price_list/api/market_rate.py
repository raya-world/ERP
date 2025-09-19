import frappe
import requests
import re
from datetime import datetime
import pytz
from frappe.utils import getdate, now

API_BASE_URL = frappe.db.get_single_value("Live Rate Config", "api_end_point")


@frappe.whitelist()
def get_martket_rate():
    """Fetches Gold & Silver prices and stores them in the database."""
    if API_BASE_URL:
        metals = [
            {"name": "Silver", "symbol": "XAG"},
            {"name": "Gold", "symbol": "XAU"},
        ]
        for metal in metals:
            price_data = get_price(metal["symbol"])
            if price_data:
                save_gold_rate(frappe._dict(price_data))

        frappe.msgprint("Updated successfully!")
    else:
        frappe.throw("Please update the API endpoint in the setting first.")


def get_price(symbol):
    """Fetch the price of a given metal symbol."""
    try:
        response = requests.get(f"{API_BASE_URL}/price/{symbol}")
        if response.status_code == 200:
            return response.json()
        else:
            frappe.log_error(f"Error fetching price for {symbol}: {response.text}")
            return None
        create_log(
            response.status_code,
        )
    except Exception as e:
        frappe.log_error(f"Exception in get_price({symbol}): {str(e)}")
        return None


def save_gold_rate(data):
    """Save Gold/Silver price to Doctype."""
    deatils = {
        "doctype": "Raya Price List",
        "metal_type": data.name,
        "live_rate": 1,
        "date_updated": datetime.strptime(data.updatedAt, "%Y-%m-%dT%H:%M:%SZ").date(),
    }
    all_purities = get_all_purity_types(data.name)
    exchange_rate = get_exchange_rate("USD", "INR")
    oz_in_gram = 31.1035
    one_gm_usd = data.price / oz_in_gram

    for purity in all_purities:
        if data.name == "Gold":
            """Extracting karat value from purity text"""
            karat = re.search(r"\d+", purity)
            _purity = int(karat.group()) if karat else None

            if not _purity or _purity > 24:
                frappe.log_error(
                    f"Not a valid purity of {data.name}",
                    f"{purity} is not a valid Purity for Metal {data.name}",
                )
                continue

            """Rate as per purity"""
            karat_price = (_purity / 24) * (one_gm_usd * exchange_rate)
            deatils.update(
                {
                    "purity": purity,
                    "weight_gm": 1,
                    "rate_per_gm": karat_price,
                }
            )

        else:
            deatils.update(
                {
                    "purity": purity,
                    "weight_gm": 1,
                    "rate_per_gm": one_gm_usd * exchange_rate,
                }
            )

        rate_exist = frappe.db.exists(
            "Raya Price List",
            {
                "metal_type": data.name,
                "date_updated": get_now_date("America/Denver"),
                "purity": purity,
            },
        )

        if rate_exist:
            doc = frappe.get_doc("Raya Price List", rate_exist)
            doc.update(deatils)
            doc.save(ignore_permissions=True)
        else:
            doc = frappe.get_doc(deatils)
            doc.insert(ignore_permissions=True)


def get_all_purity_types(metal_name):
    all = frappe.db.get_all(
        "Item Attribute Value",
        {"attribute_type": metal_name, "parent": "Purity"},
        pluck="attribute_value",
    )
    if not all and metal_name == "Gold":
        return ["24kt"]
    elif not all and metal_name == "Silver":
        return ["950"]

    return all


def get_exchange_rate(from_crr, to_crr):
    ex_rate = frappe.db.get_value(
        "Currency Exchange",
        {"from_currency": from_crr, "to_currency": to_crr, "for_selling": 1},
        "exchange_rate",
    )
    if not ex_rate:
        doc = frappe.get_doc(
            {
                "doctype": "Currency Exchange",
                "date": getdate(now()),
                "from_currency": from_crr,
                "to_currency": to_crr,
                "exchange_rate": 1,
                "for_selling": 1,
            }
        )
        doc.insert(ignore_permissions=True)
        ex_rate = doc.exchange_rate

    return ex_rate


def create_log(status_code, response_text, url):
    doc = frappe.new_doc("API Logs")
    doc.status = status_code
    doc.data = response_text
    doc.requested_url = url
    doc.save(ignore_permissions=True)


def get_symbols_data():
    url = f"{API_BASE_URL}/symbols"
    try:
        response = requests.get(url)
        metals = None
        if response.status_code == 200:
            data = response.json()
            metals = [m for m in data if m["name"] in ["Gold", "Silver"]]
        return metals

    except Exception as e:
        frappe.log_error(f"Exception in get_gold_silver_symbols: {str(e)}")


def get_now_date(region):
    """Getting Amerca/Denver timezone to validate as our free api uses this timezone"""
    region_tz = pytz.timezone(region)
    date_bbj = datetime.now(region_tz)
    return date_bbj.strftime("%Y-%m-%d")
