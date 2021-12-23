import frappe, json
from frappe import _, msgprint, throw
from frappe.utils import cint, flt, cstr, datetime
from frappe.utils import cint, flt, money_in_words
import sys



SALE = ["Sales Invoice"]
PURCHASE = ["Purchase Invoice"]

def validate_controller(doc, method):
    doctype = doc.meta.get("name")
    controller = None
    try:
        if doctype in SALE:
            if(method == "on_submit"):
                from jawa_logistics.controllers.sales_invoice import SellingController
                SellingController(doc, doctype, method).validate_sales()
        elif(doctype in PURCHASE):
            if(method == "on_submit"):
                from jawa_logistics.controllers.purchase_invoice import PurchaseController
                PurchaseController(doc, doctype, method).validate_purchase()

    except Exception as e:
        frappe.throw(_("There is an error in the process. Report this error to ERP Administrator. {0}").format(frappe.get_traceback()))



class BaseController(object):
    def __init__(self, doc, doctype, method):
        self.dt = doctype
        self.doc = doc
        self.method = method
