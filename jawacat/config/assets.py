from __future__ import unicode_literals
from frappe import _

def get_data():
	return [
        {
            "label": _("Reports"),
			"items": [
                {
                    "type": "report",
                    "is_query_report": True,
                    "name": "Asset Depreciation Schedules Summary",
                    "doctype": "Asset"
                }
            ]
        },

    ]
