import frappe


def setup_roles():
	"""
	Creates the 4 default roles for the Employee Management application.
	This function is called by after_migrate hook.
	"""
	roles = [
		"BWAdmin",
		"BWEmployee",
		"BWManager",
		"BWCompany"
	]
	
	for role_name in roles:
		if not frappe.db.exists("Role", role_name):
			role = frappe.get_doc({
				"doctype": "Role",
				"role_name": role_name,
				"desk_access": 1
			})
			role.insert(ignore_permissions=True)
			frappe.db.commit()
			print(f"Created role: {role_name}")
		else:
			print(f"Role {role_name} already exists")


def create_admin_user():
	"""
	Creates a default admin user with BWAdmin role.
	Email: admin@mail.com
	Password: admin
	This function is called by after_migrate hook.
	"""
	email = "admin@mail.com"
	password = "admin"
	role = "BWAdmin"
	
	# Check if user already exists
	if not frappe.db.exists("User", email):
		user = frappe.get_doc({
			"doctype": "User",
			"email": email,
			"first_name": "Admin",
			"send_welcome_email": 0,
			"user_type": "System User"
		})
		user.insert(ignore_permissions=True)
		
		# Set password
		user.new_password = password
		user.save(ignore_permissions=True)
		
		# Add BWAdmin role
		user.add_roles(role)
		
		frappe.db.commit()
		print(f"Created admin user: {email} with role {role}")
	else:
		# User exists, ensure they have the BWAdmin role
		user = frappe.get_doc("User", email)
		if role not in [r.role for r in user.get("roles")]:
			user.add_roles(role)
			user.save(ignore_permissions=True)
			frappe.db.commit()
			print(f"Added {role} role to existing user: {email}")
		else:
			print(f"Admin user {email} already exists with {role} role")


def after_migrate():
	"""
	This function is called after migrations are completed.
	It sets up the application roles and creates the default admin user.
	"""
	setup_roles()
	create_admin_user()

