// Copyright (c) 2025, Patel Aasif Khan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Live Rate Config", {
	refresh(frm) {
        frm.add_custom_button("Metal Rate",function(){
            frappe.call({
                method:"raya_erp.raya_erp.doctype.raya_price_list.api.market_rate.get_martket_rate",
                freeze:true,
                freeze_message:"Communicating with Market...",
                callback:function(r){
                    frappe.msgprint("Success",r.message)
                }
            })
        },
        "Fetch Now")
        frm.add_custom_button("Currency Conversion",function(){
            frappe.call({
                method:"raya_erp.raya_erp.customization.currency_exchange.currency_exchange.get_current_rate",
                freeze:true,
                freeze_message:"Communicating with Market...",
                callback:function(r){
                    frappe.msgprint("Updated successfully!")
                }
            })
        },
        "Fetch Now")
	},
});
