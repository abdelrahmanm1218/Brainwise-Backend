import frappe 

@frappe.whitelist(allow_guest=True)
def login(usr, pwd):
    try:
        login_manager = frappe.auth.LoginManager()
        login_manager.authenticate(user=usr, pwd=pwd)
        login_manager.post_login()
    except frappe.AuthenticationError:
        frappe.clear_messages()
        frappe.local.response["http_status_code"] = 401
        frappe.local.response["message"] = {
            "success": False,
            "message": "Authentication Failed"
        }
        return

    user = frappe.get_doc('User', frappe.session.user)
    
    frappe.local.response["http_status_code"] = 200
    frappe.local.response["message"] = {
        "success": True,
        "message": "Authentication Success",
        "sid": frappe.session.sid,
        "user": frappe.session.user
    }
    return




@frappe.whitelist()
def account():
    user = frappe.get_doc("User", frappe.session.user)
    if user:
        role_names = [role.role for role in user.roles]
        return {
            "name": user.name,
            "creation": user.creation,
            "first_name": user.first_name,
            "middle_name": user.middle_name,
            "last_name": user.last_name,
            "full_name": user.full_name,
            "username": user.username,
            "roles": role_names,
            "mobile_no": user.mobile_no,
            "gender": user.gender,
            "birth_date": user.birth_date,
            "user_image": user.user_image,
            "language": user.language,
            "time_zone": user.time_zone,
            "location": user.location
        }
    else:
        frappe.throw(_("User not found."))




@frappe.whitelist()
def update_profile(first_name=None,middle_name=None, last_name=None , mobile_no=None ,gender=None,birth_date=None , user_image=None ,language=None , time_zone=None, location=None):
    try:
        user = frappe.get_doc('User', frappe.session.user)
        if first_name: user.first_name = first_name
        if middle_name:  user.middle_name = middle_name
        if user_image: user.user_image = user_image
        if last_name: user.last_name = last_name
        if last_name:  user.last_name = last_name
        if mobile_no: user.mobile_no = mobile_no
        if time_zone: user.time_zone = time_zone
        if language: user.language = language
        if birth_date: user.birth_date = birth_date
        if gender: user.gender = gender
        if location: user.location= location
        
        user.save()
        frappe.db.commit()

        frappe.response["message"] = {
            "success": 1,
            "message": "Profile updated successfully"
        }
    except Exception as e:
        frappe.response["message"] = {
            "success": 0,
            "message": "Failed to update profile: {}".format(str(e))
        }
    return
