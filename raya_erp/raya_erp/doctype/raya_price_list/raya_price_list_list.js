frappe.listview_settings["Raya Price List"] = {
    onload: function (listview) {
        listview.page.add_button("Fetch Latest Rate",function(){
            frappe.call({
                method:"raya_erp.raya_erp.doctype.raya_price_list.api.market_rate.get_martket_rate",
                freeze:true,
                freeze_message:"Communicating with Market...",
                callback:function(r){
                    frappe.msgprint("Success",r.message)
                }
            })
        }) 
    }
}