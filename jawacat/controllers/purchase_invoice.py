import frappe
from frappe import _
from jawa_logistics.controllers.base_controller import BaseController
from frappe.utils import cint, cstr, date_diff, flt, formatdate, getdate, get_link_to_form, comma_or, get_fullname, add_days, nowdate, get_datetime_str
from datetime import datetime
from dateutil import relativedelta

class PurchaseController(BaseController):
    def validate_purchase(self):
        try:
            items = self.doc.items
            for item in items:
                if(item.enable_deferred_expense == 1):
                    self.update_gl_entries(item)
        except Exception as e:
            frappe.db.rollback()
            frappe.msgprint(str(e))

    def update_gl_entries(self, item):
        month = 0

        start_date = datetime.strptime(str(item.service_start_date), '%Y-%m-%d')
        end_date = datetime.strptime(str(item.service_end_date), '%Y-%m-%d')
        in_range = relativedelta.relativedelta(end_date, start_date)
        #month = in_range.months
        month = item.no_of_months

        if(month > 1):
            amount = item.amount/month

            for i in range(0, month):
                date = datetime.date(start_date) + relativedelta.relativedelta(months=i)

                if(item.expense_account):
                    self.add_gl(item.expense_account, amount,0, item.cost_center, date)

                if(item.deferred_expense_account):
                    self.add_gl(item.deferred_expense_account, 0, amount, item.cost_center, date)


    def add_gl(self, account, debit, credit, cost_center, date):
        doc = frappe.new_doc("GL Entry")
        doc.posting_date = date
        doc.account = account
        doc.cost_center = cost_center
        doc.debit = flt(debit, 3)
        doc.debit_in_account_currency = flt(debit, 3)
        doc.credit = flt(credit, 3)
        doc.credit_in_account_currency = flt(credit, 3)
        doc.account_currency = self.doc.currency
        doc.against = self.doc.supplier
        doc.voucher_type = "Purchase Invoice"
        doc.voucher_no = self.doc.name
        doc.remarks = "No Remarks"
        doc.company = self.doc.company
        doc.party_type = "Supplier"
        doc.party = self.doc.supplier
        doc.supplier = self.doc.supplier
        doc.save(ignore_permissions=True)
        doc.submit()

