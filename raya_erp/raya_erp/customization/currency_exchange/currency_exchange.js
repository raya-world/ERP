// Copyright (c) 2025, Patel Aasif Khan and contributors
// For license information, please see license.txt

frappe.ui.form.on("Currency Exchange", {
	refresh(frm) {
        frm.add_custom_button("Update Rate",function(){
            frappe.call({
                method:"raya_erp.raya_erp.customization.currency_exchange.currency_exchange.get_current_rate",
                args:{
                    doc_name:frm.doc.name
                },
                callback:function(r){
                    frappe.msgprint("Updated successfully!")
                }
            })
        })
	},
});