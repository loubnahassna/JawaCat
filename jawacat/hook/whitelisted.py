import frappe
from frappe import _
from six import string_types
import json

@frappe.whitelist()
def get_outstanding_reference_documents(args):
    from erpnext.accounts.doctype.payment_entry.payment_entry import get_outstanding_reference_documents
    data = get_outstanding_reference_documents(args)

    for d in data:
        if d.voucher_type in ("Sales Invoice", "Purchase Invoice"):
            d["total_amount"] = frappe.db.get_value(d.voucher_type, d.voucher_no, "grand_total") or d.total_amount
    return data
