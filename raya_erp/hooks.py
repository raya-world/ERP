app_name = "raya_erp"
app_title = "Raya ERP"
app_publisher = "Patel Aasif Khan"
app_description = "Raya ERP"
app_email = "patelasif52@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "raya_erp",
# 		"logo": "/assets/raya_erp/logo.png",
# 		"title": "Raya ERP",
# 		"route": "/raya_erp",
# 		"has_permission": "raya_erp.api.permission.has_app_permission"
# 	}
# ]

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/raya_erp/css/raya_erp.css"
# app_include_js = "/assets/raya_erp/js/raya_erp.js"

# include js, css files in header of web template
# web_include_css = "/assets/raya_erp/css/raya_erp.css"
# web_include_js = "/assets/raya_erp/js/raya_erp.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "raya_erp/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {
    "Currency Exchange": "raya_erp/customization/currency_exchange/currency_exchange.js",
    # "Item":"raya_erp/customization/item/item.js"
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "raya_erp/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "raya_erp.utils.jinja_methods",
# 	"filters": "raya_erp.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "raya_erp.install.before_install"
# after_install = "raya_erp.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "raya_erp.uninstall.before_uninstall"
# after_uninstall = "raya_erp.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "raya_erp.utils.before_app_install"
# after_app_install = "raya_erp.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "raya_erp.utils.before_app_uninstall"
# after_app_uninstall = "raya_erp.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "raya_erp.notifications.get_notification_config"

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

# DocType Class
# ---------------
# Override standard doctype classes
# /workspace/development/frappe-bench/apps/raya_erp/raya_erp/raya_erp/customization/item/item.py
override_doctype_class = {
	"Item": "raya_erp.raya_erp.customization.item.item.CustomItem"
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "Currency Exchange": {
        "before_insert": "raya_erp.raya_erp.customization.currency_exchange.currency_exchange.before_insert",
    },
    "Item Attribute":{
        "before_save":"raya_erp.raya_erp.customization.item_attribute.item_attribute.before_insert"
    },
    "Item":{
        "before_save":"raya_erp.raya_erp.customization.item.item.before_save",
        "after_insert":"raya_erp.raya_erp.customization.item.item.after_insert",
        "autoname":"raya_erp.raya_erp.customization.item.item.custom_item_autoname"
    },
    "Item Price":{
        "validate":"raya_erp.raya_erp.customization.item_price.item_price.validate"
    },
    "Serial No":{
        "before_save":"raya_erp.raya_erp.customization.serial_no.serial_no.before_save",
    }
}

# Scheduled Tasks
# ---------------

scheduler_events = {
    "cron": {
        "0 */7 * * *": [
            "raya_erp.raya_erp.doctype.raya_price_list.api.market_rate.get_martket_rate",
        ]
    },
    # 	"all": [
    # 		"raya_erp.tasks.all"
    # 	],
    "daily": [
        "raya_erp.raya_erp.customization.currency_exchange.currency_exchange.get_current_rate",
    ],
    # 	"hourly": [
    # 		"raya_erp.tasks.hourly"
    # 	],
    # 	"weekly": [
    # 		"raya_erp.tasks.weekly"
    # 	],
    # 	"monthly": [
    # 		"raya_erp.tasks.monthly"
    # 	],
}

# Testing
# -------

# before_tests = "raya_erp.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "raya_erp.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "raya_erp.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["raya_erp.utils.before_request"]
# after_request = ["raya_erp.utils.after_request"]

# Job Events
# ----------
# before_job = ["raya_erp.utils.before_job"]
# after_job = ["raya_erp.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"raya_erp.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


fixtures = [
    {"dt": "Custom Field", "filters": [["module", "=", "Raya ERP"]]},
    {"dt": "Property Setter", "filters": [["module", "=", "Raya ERP"]]}
]
