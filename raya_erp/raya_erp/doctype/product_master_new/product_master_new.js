frappe.ui.form.on("Product Master New", {
    onload(frm) {
        if (!frm.doc.__islocal) {
            frappe.call({
                method: "frappe.client.get_list",
                args: {
                    doctype: "Item",
                    filters: {
                        custom_product_master: frm.doc.name
                    },
                    fields: [
                        "item_code",
                        "stones_weight",
                        "custom_net_weight_metal",
                        "net_weight",
                        "gross_weight",
                    ]
                },
                callback: function (r) {
                    if (r.message && r.message.length) {
                        let html = `
                            <table class="table table-bordered table-sm">
                                <thead>
                                    <tr>
                                        <th>Item Code</th>
                                        <th>Stone Weight</th>
                                        <th>Metal Weight in Kt</th>
                                        <th>Net Weight</th>
                                        <th>Gross Weight</th>
                                        <th>Metal Price</th>
                                        <th>Labour Price</th>
                                        <th>Stone Price</th>
                                        <th>Total Price</th>
                                    </tr>
                                </thead>
                                <tbody>
                        `;

                        r.message.forEach(item => {
                            let metal_price = 0;
                            let labour_price = 0;
                            let stone_price = 0;
                            let total_price = 0;

                            const metal_weight = parseFloat(item.custom_net_weight_metal) || 0;
                            const net_weight = parseFloat(item.net_weight) || 0;
                            const gross_weight = parseFloat(item.gross_weight) || 0;
                            const margin = parseFloat(frm.doc.margin) || 0;
                            const labour_rate = parseFloat(frm.doc.labour_rate) || 0;

                            // Labour calculation
                            if (frm.doc.labour_rate_on === "Net") {
                                labour_price = labour_rate * net_weight;
                            } else if (frm.doc.labour_rate_on === "Gross") {
                                labour_price = labour_rate * gross_weight;
                            }

                            // Fetch stone price
                            frappe.call({
                                method: "raya_erp.raya_erp.customization.item.item.fetch_stone_price",
                                args: { name: item.item_code },
                                async: false,
                                callback: function (res) {
                                    stone_price = parseFloat(res.message) || 0;
                                }
                            });

                            // Fetch metal price
                            frappe.call({
                                method: "raya_erp.raya_erp.customization.item.item.fetch_metal_price",
                                args: { name: item.item_code },
                                async: false,
                                callback: function (res) {
                                    metal_price = parseFloat(res.message) || 0;
                                }
                            });

                            const metal_total = metal_price * metal_weight;
                            const subtotal = metal_total + labour_price + stone_price;
                            const margin_value = subtotal * (margin / 100);
                            total_price = subtotal + margin_value;

                            // Helper to format to 3 decimals safely
                            const fmt = val => (isNaN(val) ? "" : val.toFixed(3));

                            html += `
                                <tr>
                                    <td>${item.item_code || ""}</td>
                                    <td>${fmt(item.stones_weight)}</td>
                                    <td>${fmt(metal_weight)}</td>
                                    <td>${fmt(net_weight)}</td>
                                    <td>${fmt(gross_weight)}</td>
                                    <td>${fmt(metal_total)}</td>
                                    <td>${fmt(labour_price)}</td>
                                    <td>${fmt(stone_price)}</td>
                                    <td>${fmt(total_price)}</td>
                                </tr>
                            `;
                        });

                        html += `
                                </tbody>
                            </table>
                        `;

                        frm.fields_dict.table_boml.$wrapper.html(html);
                    } else {
                        frm.fields_dict.table_boml.$wrapper.html("<p class='text-muted'>No variants found.</p>");
                    }
                }
            });
        } else {
            frm.fields_dict.table_boml.$wrapper.html("<p class='text-muted'>Save the document to load variants.</p>");
        }
    }
});
