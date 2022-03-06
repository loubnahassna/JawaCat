# Copyright (c) 2013, mesa_safd@hotmail.com and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import cstr, today, flt, add_years, formatdate, getdate, add_months
from erpnext.accounts.report.financial_statements import get_period_list, get_fiscal_year_data, validate_fiscal_year

def execute(filters=None):
	filters = frappe._dict(filters or {})
	columns = get_columns(filters)
	data = get_data(filters)

	return columns, data

def get_conditions(filters):
	conditions = "ass.docstatus = 1"

	if filters.get('company'): conditions += " and company=%(company)s"
	if filters.get('from_date') and filters.get('to_date'):
		# conditions += " and IF (ass.status='Fully Depreciated', ass.purchase_date, dep.schedule_date) between %(from_date)s and %(to_date)s"
		conditions += " and dep.schedule_date between %(from_date)s and %(to_date)s"
	if filters.get('asset_category'): conditions += " and ass.asset_category=%(asset_category)s"
	if filters.get('cost_center'): conditions += " and ass.cost_center=%(cost_center)s"
	if filters.get('finance_book'): conditions+= " and dep.finance_book=%(finance_book)s"
	if filters.get('asset'): conditions += " and ass.name=%(asset)s"

	return conditions

def get_data(filters):

	data = []

	conditions = get_conditions(filters)
	pr_supplier_map = get_purchase_receipt_supplier_map()
	pi_supplier_map = get_purchase_invoice_supplier_map()

	# formatdate = add_months(filters.form_date, -1) 

	assets_record = frappe.db.sql('''Select ass.name as asset_id, ass.asset_name, ass.status, ass.department, dep.finance_book,
		ass.cost_center, ass.purchase_receipt,ass.asset_category, ass.purchase_date, ass.gross_purchase_amount, ass.location,
		ass.available_for_use_date, ass.purchase_invoice, ass.opening_accumulated_depreciation, dep.schedule_date,
		SUM(dep.depreciation_amount) as sum_depreciation_amount,dep.depreciation_amount, (dep.accumulated_depreciation_amount) as accumulated_depreciation_amount 
		FROM tabAsset as ass LEFT JOIN `tabDepreciation Schedule` as dep ON ass.name = dep.parent
		WHERE {conditions} group by ass.name'''.format(conditions=conditions),filters, as_dict=True)

	for asset in assets_record:
		opening_accumulated_depreciation = flt(asset.opening_accumulated_depreciation)
		doc = frappe.db.sql("""Select accumulated_depreciation_amount from `tabDepreciation Schedule` 
			where parent = '{0}' and schedule_date < %(from_date)s
			order by schedule_date desc limit  1 """.format(asset.asset_id ),filters ,as_dict=True)
		if doc:
			opening_accumulated_depreciation = flt(doc[0].accumulated_depreciation_amount)

		# asset_value = asset.gross_purchase_amount - flt(asset.opening_accumulated_depreciation) + flt(asset.depreciation_amount)
		accumulated_depreciation_amount = opening_accumulated_depreciation + flt(asset.sum_depreciation_amount)
		asset_value = asset.gross_purchase_amount - accumulated_depreciation_amount
		row = {
			"asset_id": asset.asset_id,
			"asset_name": asset.asset_name,
			"status": asset.status,
			"department": asset.department,
			"cost_center": asset.cost_center,
			"vendor_name": pr_supplier_map.get(asset.purchase_receipt) or pi_supplier_map.get(asset.purchase_invoice),
			"gross_purchase_amount": asset.gross_purchase_amount,
			"opening_accumulated_depreciation": opening_accumulated_depreciation,
			"depreciated_amount": asset.sum_depreciation_amount or 0.0,
			"accumulated_depreciation_amount": accumulated_depreciation_amount or 0.0,
			"available_for_use_date": asset.available_for_use_date,
			"location": asset.location,
			"asset_category": asset.asset_category,
			"purchase_date": asset.purchase_date,
			"asset_value": asset_value
			}
		data.append(row)

	return data

def get_purchase_receipt_supplier_map():
	return frappe._dict(frappe.db.sql(''' Select
		pr.name, pr.supplier
		FROM `tabPurchase Receipt` pr, `tabPurchase Receipt Item` pri
		WHERE
			pri.parent = pr.name
			AND pri.is_fixed_asset=1
			AND pr.docstatus=1
			AND pr.is_return=0'''))

def get_purchase_invoice_supplier_map():
	return frappe._dict(frappe.db.sql(''' Select
		pi.name, pi.supplier
		FROM `tabPurchase Invoice` pi, `tabPurchase Invoice Item` pii
		WHERE
			pii.parent = pi.name
			AND pii.is_fixed_asset=1
			AND pi.docstatus=1
			AND pi.is_return=0'''))

def get_columns(filters):
	return [
		{
			"label": _("Asset Id"),
			"fieldtype": "Link",
			"fieldname": "asset_id",
			"options": "Asset",
			"width": 160
		},
		{
			"label": _("Asset Name"),
			"fieldtype": "Data",
			"fieldname": "asset_name",
			"width": 140
		},
		{
			"label": _("Asset Category"),
			"fieldtype": "Link",
			"fieldname": "asset_category",
			"options": "Asset Category",
			"width": 100
		},
		{
			"label": _("Purchase Date"),
			"fieldtype": "Date",
			"fieldname": "purchase_date",
			"width": 90
		},
		{
			"label": _("Available For Use Date"),
			"fieldtype": "Date",
			"fieldname": "available_for_use_date",
			"width": 90
		},
		{
			"label": _("Status"),
			"fieldtype": "Data",
			"fieldname": "status",
			"width": 100
		},
		{
			"label": _("Gross Purchase Amount"),
			"fieldname": "gross_purchase_amount",
			"fieldtype": "Currency",
			"options": "company:currency",
			"width": 130
		},
		{
			"label": _("Opening Accumulated Depreciation"),
			"fieldname": "opening_accumulated_depreciation",
			"fieldtype": "Currency",
			"options": "company:currency",
			"width": 130
		},
		{
			"label": _("Depreciated Amount"),
			"fieldname": "depreciated_amount",
			"fieldtype": "Currency",
			"options": "company:currency",
			"width": 100
		},
		{
			"label": _("Accumulated Depreciation Amount"),
			"fieldname": "accumulated_depreciation_amount",
			"fieldtype": "Currency",
			"options": "company:currency",
			"width": 130
		},
		{
			"label": _("Asset Value"),
			"fieldname": "asset_value",
			"fieldtype": "Currency",
			"options": "company:currency",
			"width": 100
		},
		{
			"label": _("Cost Center"),
			"fieldtype": "Link",
			"fieldname": "cost_center",
			"options": "Cost Center",
			"width": 100
		},
		{
			"label": _("Department"),
			"fieldtype": "Link",
			"fieldname": "department",
			"options": "Department",
			"width": 100
		},
		{
			"label": _("Vendor Name"),
			"fieldtype": "Data",
			"fieldname": "vendor_name",
			"width": 100
		},
		{
			"label": _("Location"),
			"fieldtype": "Link",
			"fieldname": "location",
			"options": "Location",
			"width": 100
		},
	]

