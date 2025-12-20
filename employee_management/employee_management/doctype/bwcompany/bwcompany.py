# Copyright (c) 2025, mw and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BWCompany(Document):

	def validate(self):
		self.check_fields()

	#check if company name is set
	def check_fields(self):
		if self.company_name == None:
			frappe.throw("Company name must be set for the Company")
	
	# before deleting a company, check if there are related departments or employees
	def on_trash(self):
		# Prevent deletion if there are related departments
		if frappe.db.exists("BWDepartment", {"company": self.name}):
			frappe.throw("Cannot delete company with existing departments")
		if frappe.db.exists("BWEmployee", {"company": self.name}):
			frappe.throw("Cannot delete company with employees")
	

	#update department count for a company
	def update_department_count(self):
		#get departments count 
		department_count = frappe.db.count("BWDepartment", {"company": self.name})
		self.number_of_departments = department_count

		self.save(ignore_permissions=True)
		frappe.db.commit()

	#update employee count for a company
	def update_employee_count(self):
		#get employees count
		employee_count = frappe.db.count("BWEmployee", {"company": self.name})
		self.number_of_employees = employee_count

		self.save(ignore_permissions=True)
		frappe.db.commit()

	


# Add on_update and on_trash hooks to auto-update counts when departments/employees change.
