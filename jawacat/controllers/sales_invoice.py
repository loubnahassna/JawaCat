import frappe
from frappe import _
from jawacat.controllers.base_controller import BaseController
from frappe.utils import cint, cstr, date_diff, flt, formatdate, getdate, get_link_to_form, comma_or, get_fullname, add_days, nowdate, get_datetime_str
from datetime import datetime
from dateutil import relativedelta

class SellingController(BaseController):
    def validate_sales(self):
        try:
            items = self.doc.items
            for item in items:
                if(item.enable_deferred_revenue == 1):
                    self.update_gl_entries(item)

        except Exception as e:
            frappe.db.rollback()
            frappe.msgprint(str(e))

    def update_gl_entries(self, item):
        month = 0

        start_date = datetime.strptime(str(item.service_start_date), '%Y-%m-%d')
        end_date = datetime.strptime(str(item.service_end_date), '%Y-%m-%d')
        in_range = relativedelta.relativedelta(end_date, start_date)
        # month = in_range.months
        month = item.no_of_months
        
        if(month > 1):
            amount = item.amount/month
            for m in range(0, month):
                date = datetime.date(start_date) + relativedelta.relativedelta(months=m)

                if(item.deferred_revenue_account):
                    self.add_gl(item.deferred_revenue_account, 0, amount, item.cost_center, date)

                if(item.income_account):
                    self.add_gl(item.income_account, amount, 0, item.cost_center, date)
        else:
            pass

    def add_gl(self, account, credit, debit, cost_center, date):
        doc = frappe.new_doc("GL Entry")
        doc.posting_date = date
        doc.account = account
        doc.cost_center = cost_center
        doc.debit = flt(debit, 3)
        doc.debit_in_account_currency = flt(debit, 3)
        doc.credit = flt(credit, 3)
        doc.credit_in_account_currency = flt(credit, 3)
        doc.account_currency = self.doc.currency
        doc.against = self.doc.customer
        doc.voucher_type = "Sales Invoice"
        doc.voucher_no = self.doc.name
        doc.remarks = "No Remarks"
        doc.party_type = "Customer"
        doc.party = self.doc.customer
        doc.company = self.doc.company
        doc.customer = self.doc.customer
        doc.save(ignore_permissions=True)
        doc.submit()
