class mba {

    setup_multiselect_s2 (frm, field, datasrc, separator=",") {
        if (!frm || !field || !datasrc || !separator) {
          frappe.throw('Missing parameters for initializing Multiselect.');
        }
        // console.log(frm.multiselect_fields);
        if (!frm.multiselect_fields) {
          frm.multiselect_fields = [];
        }
        if (frm.multiselect_fields.indexOf(field) == -1) {
          frm.multiselect_fields.push(field);
        }
        var propname = frm.doc.doctype + "-" + field + "-array";
    
        // Cache Select Options List
        if (datasrc.hasOwnProperty('doctype')) {
          //Not reqd for Ajax based sources
        } else if (datasrc.hasOwnProperty('array')) {
          if (!window[propname]) {
            window[propname] = $.map(datasrc.array, function (itm) {
              return { id: itm, text: itm};
            });
          }
        } else if (datasrc.hasOwnProperty('query')) {
          frappe.throw('Implement query datasource.');
        } else {
          frappe.throw('Invalid datasource.');
        }
      
        frm.fields_dict[field].$wrapper.html('<div><label class="control-label">' + frm.fields_dict[field].df.label + '</label><br/><select id="'+field+'-s2" multiple style="left: 321.5px; width: 100%; "></select></div>');
        if ($(`#${field}-s2`).data('select2')) {
          // console.log('Existing '+field+' Select2 found, destroying..');
          $(`#${field}-s2`).select2("destroy");
        }
        if (datasrc.hasOwnProperty('doctype')){
          // console.log('Initializing Select2 - with DocType...');
          $(`#${field}-s2`).select2({
            ajax:{
              url: "/api/method/frappe.desk.search.search_link",
              dataType: 'json',
              delay: 300,
              data: function (params) {
                return {
                  doctype: datasrc.doctype,
                  txt: params.term || ""
                };
              },
              headers:{
                "X-Frappe-CSRF-Token": frappe.csrf_token,
                "X-Requested-With": "XMLHttpRequest"
              },
              processResults: function (data, params) {
                // console.log('result ' + data.results);
                return {
                  results: $.map(data.results, function (itm) {
                    return {
                      id: itm["value"],
                      text: itm["value"]
                    };
                  })
                };
              },
              cache: true
            },
            //formatSelection: format,
            //formatResult: format,
            disabled: frm.fields_dict[field].df.read_only
          });
    
          // console.log(`Loading ${field} from doc: ` + frm.doc[`${field}`]);
          let lst = frm.doc[field] ? frm.doc[field].split(',') : null
          if(lst) {
            let this_select = $(`#${field}-s2`)
            lst.forEach(opt => {
              this_select.append(new Option(opt,opt,true,true));
            });
            // this_select.trigger('change');
          }
        } else if (datasrc.hasOwnProperty('array')) {
          // console.log('Initializing Select2 - with Array...');
          $(`#${field}-s2`).select2({
            data:window[propname],
            //formatSelection: format,
            //formatResult: format,
            disabled: frm.fields_dict[field].df.read_only
          });
          // console.log(`Loading ${field} from doc: ` + frm.doc[`${field}`]);
          $(`#${field}-s2`).val(frm.doc[`${field}`] ? frm.doc[`${field}`].split(separator) : '').trigger("change");
        }
      
        $(`#${field}-s2`).on('select2:select', function (e) {
          let field_val = $(`#${field}-s2`).val();
          // console.log(`Updating ${field} to doc: ` + field_val ? field_val : '');
          field_val = field_val ? field_val.join(separator) : '';
          frm.set_value(`${field}`, field_val);
        });
        $(`#${field}-s2`).on('select2:unselect', function (e) {
          let field_val = $(`#${field}-s2`).val();
          // console.log(`Updating ${field} to doc: ` + field_val ? field_val : '');
          field_val = field_val ? field_val.join(separator) : '';
          frm.set_value(`${field}`, field_val);
        });
      }
    load_multiselect_values (frm)  {
        if (!frm.multiselect_fields) {
          return;
        }
        frm.multiselect_fields.forEach(function (field) {
          // console.log(`Refresh occurred, loading ${field} from doc: ` + frm.doc[field]);
          $(`#${field}-s2`).val(frm.doc[field] ? frm.doc[field].split(',') : '').trigger("change");
          if (frm.fields_dict[field].df.read_only) {
            $(`#${field}-s2`).select2({
              disabled: frm.fields_dict[field].df.read_only
            });  
          }
        });
      }
}
