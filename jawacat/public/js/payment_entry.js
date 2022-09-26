frappe.ui.form.on('Payment Entry', {
	refresh(frm){
		if(frappe.ui.form.get_event_handler_list("Payment Entry", "get_outstanding_documents").length){
			frappe.ui.form.handlers["Payment Entry"]["get_outstanding_documents"] = []
			frappe.ui.form.get_event_handler_list("Payment Entry", "get_outstanding_documents").push(cur_frm.events.get_outstanding_documents);
			
		}	
	},
	get_outstanding_documents: function(frm, filters) {
		frm.clear_table("references");

		if(!frm.doc.party) {
			return;
		}

		frm.events.check_mandatory_to_fetch(frm);
		var company_currency = frappe.get_doc(":Company", frm.doc.company).default_currency;

		var args = {
			"posting_date": frm.doc.posting_date,
			"company": frm.doc.company,
			"party_type": frm.doc.party_type,
			"payment_type": frm.doc.payment_type,
			"party": frm.doc.party,
			"party_account": frm.doc.payment_type=="Receive" ? frm.doc.paid_from : frm.doc.paid_to,
			"cost_center": frm.doc.cost_center
		}

		for (let key in filters) {
			args[key] = filters[key];
		}

		frappe.flags.allocate_payment_amount = filters['allocate_payment_amount'];

		return  frappe.call({
			method: 'erpnext.accounts.doctype.payment_entry.payment_entry.get_outstanding_reference_documents',
			args: {
				args:args
			},
			callback: function(r, rt) {
				if(r.message) {
					var total_positive_outstanding = 0;
					var total_negative_outstanding = 0;
					var add_rows = true;
					$.each(r.message, function(i, d) {
						add_rows = (["Sales Invoice","Purchase Invoice"].includes(d.voucher_type) && (d.total_amount < 0 || d.outstanding_amount < 0))? false: true ;
						if(add_rows){
							var c = frm.add_child("references");
							c.reference_doctype = d.voucher_type;
							c.reference_name = d.voucher_no;
							c.due_date = d.due_date
							c.total_amount = d.invoice_amount;
							c.outstanding_amount = d.outstanding_amount;
							c.bill_no = d.bill_no;

							if(!in_list(["Sales Order", "Purchase Order", "Expense Claim", "Fees"], d.voucher_type)) {
								if(flt(d.outstanding_amount) > 0)
									total_positive_outstanding += flt(d.outstanding_amount);
								else
									total_negative_outstanding += Math.abs(flt(d.outstanding_amount));
							}

							var party_account_currency = frm.doc.payment_type=="Receive" ?
								frm.doc.paid_from_account_currency : frm.doc.paid_to_account_currency;

							if(party_account_currency != company_currency) {
								c.exchange_rate = d.exchange_rate;
							} else {
								c.exchange_rate = 1;
							}
							if (in_list(['Sales Invoice', 'Purchase Invoice', "Expense Claim", "Fees"], d.reference_doctype)){
								c.due_date = d.due_date;
							}
						}
					});
					if(
						(frm.doc.payment_type=="Receive" && frm.doc.party_type=="Customer") ||
						(frm.doc.payment_type=="Pay" && frm.doc.party_type=="Supplier")  ||
						(frm.doc.payment_type=="Pay" && frm.doc.party_type=="Employee") ||
						(frm.doc.payment_type=="Receive" && frm.doc.party_type=="Student")
					) {
						if(total_positive_outstanding > total_negative_outstanding)
							if (!frm.doc.paid_amount)
								frm.set_value("paid_amount",
									total_positive_outstanding - total_negative_outstanding);
					} else if (
						total_negative_outstanding &&
						total_positive_outstanding < total_negative_outstanding
					) {
						if (!frm.doc.received_amount)
							frm.set_value("received_amount",
								total_negative_outstanding - total_positive_outstanding);
					}
					// setTimeout(function(){
					// 	references = cur_frm.doc.references;
					// 	console.log(references);
					// },1000);
				}

				frm.events.allocate_party_amount_against_ref_docs(frm,
					(frm.doc.payment_type=="Receive" ? frm.doc.paid_amount : frm.doc.received_amount));

			}
		});
	},

})