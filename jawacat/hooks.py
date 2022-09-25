# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "jawacat"
app_title = "jawacat"
app_publisher = "Maysaa Elsafadi"
app_description = "jawacat"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "mesa_safd@hotmail.com"
app_license = "MIT"

# Includes in <head>
# ------------------

website_context = {
	"favicon": 	"/assets/jawacat/images/logo.jpeg",
	"splash_image": "/assets/jawacat/images/logo.jpeg"
}
# include js, css files in header of desk.html
# app_include_css = "/assets/jawacat/css/jawacat.css"
# app_include_js = "/assets/jawacat/js/jawacat.js"

# include js, css files in header of web template
# web_include_css = "/assets/jawacat/css/jawacat.css"
# web_include_js = "/assets/jawacat/js/jawacat.js"

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Website user home page (by function)
# get_website_user_home_page = "jawacat.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "jawacat.install.before_install"
# after_install = "jawacat.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "jawacat.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

doctype_js = {
	"Purchase Invoice" : "public/js/purchase_invoice.js",
	"Payment Entry" : "public/js/payment_entry.js"
}

doc_events = {
    "Sales Invoice": {
        "on_submit": "jawacat.controllers.base_controller.validate_controller"
    },
    "Purchase Invoice":{
        "on_submit": "jawacat.controllers.base_controller.validate_controller"
    },

    
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"jawacat.tasks.all"
# 	],
# 	"daily": [
# 		"jawacat.tasks.daily"
# 	],
# 	"hourly": [
# 		"jawacat.tasks.hourly"
# 	],
# 	"weekly": [
# 		"jawacat.tasks.weekly"
# 	]
# 	"monthly": [
# 		"jawacat.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "jawacat.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
	"erpnext.accounts.doctype.payment_entry.payment_entry.get_outstanding_reference_documents" : "jawacat.hook.whitelisted.get_outstanding_reference_documents"
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "jawacat.task.get_dashboard_data"
# }

