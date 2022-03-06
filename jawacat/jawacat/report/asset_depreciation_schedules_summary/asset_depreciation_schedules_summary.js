// Copyright (c) 2016, mesa_safd@hotmail.com and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Asset Depreciation Schedules Summary"] = {
	"filters": [
		{
			fieldname:"company",
			label: __("Company"),
			fieldtype: "Link",
			options: "Company",
			default: frappe.defaults.get_user_default("Company"),
			reqd: 1
		},
		{
			"fieldname":"from_date",
			"label": __("Start Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.nowdate(), -12),
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("End Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.nowdate(),
			"reqd": 1
		},
		{
			fieldname:"asset",
			label: __("Asset"),
			fieldtype: "Link",
			options: "Asset"
		},
		{
			fieldname:"asset_category",
			label: __("Asset Category"),
			fieldtype: "Link",
			options: "Asset Category"
		},
		{	
			fieldname:"finance_book",
			label: __("Finance Book"),
			fieldtype: "Link",
			options: "Finance Book"
		},
		{
			fieldname:"cost_center",
			label: __("Cost Center"),
			fieldtype: "Link",
			options: "Cost Center"
		},
	]
};