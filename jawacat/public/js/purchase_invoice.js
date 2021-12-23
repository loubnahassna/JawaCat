frappe.ui.form.on('Purchase Invoice Item', {

    service_start_date: function (frm, cdt, cdn) {
        set_end_month(frm, cdt, cdn)
    },
    no_of_months: function (frm, cdt, cdn) {
        set_end_month(frm, cdt, cdn)
    },
    
})


var set_end_month = function(frm, cdt, cdn) {
    var d = frappe.model.get_doc(cdt, cdn);
    if (d.no_of_months && d.service_start_date) {
        var start_date = new Date(d.service_start_date);
        var end_date = new Date(start_date.setMonth(start_date.getMonth() + d.no_of_months));
        frappe.model.set_value(cdt, cdn, "service_end_date", end_date);
    }
}

