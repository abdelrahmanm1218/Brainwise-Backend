# Copyright (c) 2025, mw and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class BWDepartment(Document):

	def validate(self):
		self.check_fields()

	#check if company and department name are set
	def check_fields(self):
		if self.company == None or self.department_name == None:
			frappe.throw("Company or Department name must be set for the Department")


	#after insert a department or update the department, update the counts of (deps, employees) in the company
	def on_update(self):
		if self.company: #check if company is set
			company_doc = frappe.get_doc("BWCompany", self.company)
			company_doc.update_department_count()
			company_doc.update_employee_count()



	# Prevent deletion if there are related Employee
	def on_trash(self):
		if frappe.db.exists("BWEmployee", {"department": self.name}):
			frappe.throw("Cannot delete Department with employees")
	

	#after delete a department, update the counts of (deps, employees) in the company
	def after_delete(self):
		if self.company:
			company_doc = frappe.get_doc("BWCompany", self.company)
			company_doc.update_department_count()
			company_doc.update_employee_count()
	

	def update_employee_count(self):
		#get employees count 
		employee_count = frappe.db.count("BWEmployee", {"department": self.name})
		self.number_of_employees = employee_count

		self.save(ignore_permissions=True)
		frappe.db.commit()

