# Copyright (c) 2025, mw and contributors
# For license information, please see license.txt


import frappe
from frappe.model.document import Document
from frappe.utils import validate_email_address
import re

def validate_phone_number(mobile_number):
	if mobile_number:
		pattern = r"^\+?\d{8,15}$"  # allows + optional, 8–15 digits
		if not re.match(pattern, mobile_number):
			frappe.throw("Invalid mobile phone number format.", frappe.ValidationError)

class BWEmployee(Document):

	def validate(self):
		# call function to check empty fields
		self.check_empty_fields()

		# validate email address format
		if self.email_address:
			if not validate_email_address(self.email_address):
				frappe.throw("Invalid email address format", frappe.ValidationError)
		
		# Look for other employees with same email
		duplicate = frappe.db.exists(
			"BWEmployee",
			{
				"email_address": self.email_address,
				"name": ["!=", self.name]  # ignore same record during update
			}
		)

		#throw error if existing email found
		if duplicate:
			frappe.log_error(f"Duplicate email found: {self.email_address}", "BWEmployee Validation")
			frappe.throw(f"Email '{self.email_address}' is already linked to another employee.", frappe.ValidationError)

		# validate mobile number format
		if self.mobile_number:
			validate_phone_number(self.mobile_number)

		# Ensure that the selected department belongs to the selected company
		if self.department and self.company:

			dept_doc = frappe.get_doc("BWDepartment", self.department)			
			if dept_doc.company != self.company:
				frappe.throw("Selected Department does not belong to the selected Company")
		
	
	def check_empty_fields(self):
		if self.employee_name == None or self.email_address == None or self.company == None or self.department == None or self.mobile_number == None:
			frappe.throw("Employee Name, Email, Company, Department, and Mobile Number must be set for the Employee")

	# after inserting or updating an employee, update the counts of employees in the department and company
	def on_update(self):
		
		#update department employee count
		if self.department:
			department_doc = frappe.get_doc("BWDepartment", self.department)
			department_doc.update_employee_count()
		
		#update company employee count
		if self.company:
			company_doc = frappe.get_doc("BWCompany", self.company)
			company_doc.update_employee_count()
	

	#after deleting an employee, update the counts of employees in the department and company
	def after_delete(self):
		
		#update department employee count
		if self.department:
			department_doc = frappe.get_doc("BWDepartment", self.department)
			department_doc.update_employee_count()
		
		#update company employee count
		if self.company:
			company_doc = frappe.get_doc("BWCompany", self.company)
			company_doc.update_employee_count()
	



# Workflow

# Add a Frappe Workflow for employee_status to enforce allowed transitions.

# On status change to Hired, validate hired_on is provided.
