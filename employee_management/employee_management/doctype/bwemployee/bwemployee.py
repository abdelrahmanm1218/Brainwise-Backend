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
		
		# Validate hired_on and days_employeed based on employee_status
		self.validate_hired_fields()
	
	def check_empty_fields(self):
		if self.employee_name == None or self.email_address == None or self.company == None or self.department == None or self.mobile_number == None:
			frappe.throw("Employee Name, Email, Company, Department, and Mobile Number must be set for the Employee")
	
	def validate_hired_fields(self):
		"""
		Validates that hired_on and days_employeed can only have values 
		when employee_status is 'Hired'. Otherwise, these fields must be empty.
		Enforces empty values when status is not 'Hired'.
		"""
		is_hired = self.employee_status == "Hired"
		
		if not is_hired:
			# If status is not "Hired", enforce empty values
			# Clear the fields automatically and log the action and throw a validation error
			if self.hired_on:
				frappe.log_error(f"Hired On date cleared for employee {self.name} due to status change.", "BWEmployee Validation")
				self.hired_on = None
				frappe.throw("Hired On date must be empty when Employee Status is not 'Hired'. It has been cleared automatically.", frappe.ValidationError)
			
			if self.days_employeed:
				frappe.log_error(f"Days Employeed cleared for employee {self.name} due to status change.", "BWEmployee Validation")
				self.days_employeed = None
				frappe.throw("Days Employeed must be empty when Employee Status is not 'Hired'. It has been cleared automatically.", frappe.ValidationError)	

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
	

