import frappe
import requests
from raya_erp.raya_erp.doctype.raya_price_list.api.market_rate import create_log

API_BASE_URL =frappe.db.get_single_value("Live Rate Config", "curr_exchange_api")
API_KEY = frappe.db.get_single_value("Live Rate Config", "crr_api_key")

def before_insert(doc,method=None):
    if API_BASE_URL and API_KEY:
        try:
            response = requests.get(API_BASE_URL+"?api_key="+API_KEY+f"&from={doc.from_currency}")
            if response.status_code == 200:
                data = frappe._dict(response.json())
                doc.exchange_rate = data.rates.get(doc.to_currency,1)
            
            create_log(response.status_code, response.text, API_BASE_URL)

        except Exception as e:
                frappe.log_error(f"Error while getting exahange rate for {doc.to_currency}")


@frappe.whitelist()
def get_current_rate(doc_name=None):
    if not doc_name:
        all_crr_exchange = frappe.db.get_all("Currency Exchange",{"for_selling":1})
    else:
        all_crr_exchange = [doc_name]
    
    if API_BASE_URL and API_KEY:
        for exchange in all_crr_exchange:
            doc = frappe.get_doc("Currency Exchange",exchange)
            try:
                response = requests.get(API_BASE_URL+"?api_key="+API_KEY+f"&from={doc.from_currency}")
                if response.status_code == 200:
                    data = frappe._dict(response.json())
                    doc.exchange_rate = data.rates.get(doc.to_currency,1)
                    doc.save()
                create_log(response.status_code, response.text, API_BASE_URL)
            except Exception as e:
                frappe.log_error(f"Error while getting exahange rate for {doc.to_currency}")
    else:
        frappe.throw("Please update the API and API Key in setting.")