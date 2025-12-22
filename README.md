# Employee Management Application

A Frappe-based application for managing companies, departments, and employees with RESTful API support and role-based access control.

## Overview

Built on Frappe Framework (v15), this application provides a complete solution for managing organizational hierarchies with automatic validations, calculations, and role-based permissions.

**Key Capabilities:**
- Company, Department, and Employee management
- RESTful API with OpenAPI 3.0 documentation
- Role-based access control (4 roles)
- Data validation and automated calculations
- Real-time employee count tracking

---

## Technology Stack

- **Framework**: Frappe Framework (v15)
- **Backend**: Python 3.10+
- **Database**: MariaDB/PostgreSQL
- **Frontend**: Frappe UI (JavaScript/jQuery)
- **API**: REST API with OpenAPI 3.0.3 specification

---

## Features

### Core Functionality
- ✅ **Company Management**: CRUD operations with automatic department/employee count tracking
- ✅ **Department Management**: Linked to companies with employee count tracking
- ✅ **Employee Management**: Complete profiles with email/phone validation, status tracking, and days employed calculation
- ✅ **REST API**: Full CRUD operations for all resources with authentication endpoints
- ✅ **Role-Based Access**: 4 roles (BWAdmin, BWManager, BWEmployee, BWCompany) with granular permissions
- ✅ **Data Validation**: Email format, phone number format, duplicate prevention, referential integrity


### Key Validations
- Email format validation and duplicate prevention
- Phone number format validation (`^\+?\d{8,15}$`)
- Department-company relationship validation
- `hired_on` and `days_employeed` can only be set when `employee_status = "Hired"`
- Prevents deletion of companies/departments with related records

---

## Quick Installation

### Prerequisites
- Python 3.10+, Node.js 18+, MariaDB/PostgreSQL, Redis
- Frappe Bench installed (`pip3 install frappe-bench`)

**Note:** For easier frontend setup, create your Frappe site as `brain.localhost:8013`. This lets the example frontend `baseURL` work without extra proxy configuration. If you created the site with a different hostname or port, update the frontend proxy to point to your site URL — see `README.md` in Frontend Folder for details on how and where to change the proxy.


### Installation Steps

1. **Navigate to bench directory:**
   ```bash
   cd /path/to/your/bench
   ```

2. **Install the application:**
   ```bash
   bench --site <your-site-name> install-app employee_management
   # Example: bench --site brain.localhost install-app employee_management
   ```

3. **Migrate database:**
   ```bash
   bench --site <your-site-name> migrate
   ```

   **Automatic Setup:**
   - Creates 4 roles: `BWAdmin`, `BWManager`, `BWEmployee`, `BWCompany`
   - Creates default admin user:
     - **Email**: `admin@mail.com`
     - **Password**: `admin`
     - **Role**: `BWAdmin`

4. **Build assets (if needed):**
   ```bash
   bench build --app employee_management
   ```

5. **Start development server:**
   ```bash
   bench start
   ```

6. **Access the application:**
   - Web Interface: `http://your-site.localhost:8013`
   - API Base: `http://your-site.localhost:8013/api`

---

## Application Structure

```
employee_management/
├── employee_management/
│   ├── auth.py                    # Authentication API endpoints
│   ├── hooks.py                   # Frappe hooks configuration
│   ├── migrate.py                 # Migration scripts (roles & admin user)
│   └── employee_management/
│       └── doctype/
│           ├── bwcompany/         # Company DocType
│           ├── bwdepartment/      # Department DocType
│           └── bwemployee/        # Employee DocType
├── openapi.yaml                   # Complete API documentation
└── README.md                      # This file
```

---

## API Documentation

Complete API documentation is available in `openapi.yaml` (OpenAPI 3.0.3 format).

**View documentation:**
- Upload `openapi.yaml` to [Swagger Editor](https://editor.swagger.io/)
- Or use `redoc-cli serve openapi.yaml`

**API Endpoints:**
- **Authentication**: `/api/method/employee_management.auth.login`
- **Resources**: `/api/resource/BWCompany`, `/api/resource/BWDepartment`, `/api/resource/BWEmployee`
- **Methods**: GET, POST, PUT, DELETE with filtering, pagination, and field selection

**Authentication:**
- Session cookie (login endpoint)
- API Key/Secret (token-based)

---

## Role-Based Access Control

| Role | Company | Department | Employee |
|------|---------|------------|----------|
| **BWAdmin** | Full | Full | Full |
| **BWManager** | Read | Read (if owner) | Create/Read/Write |
| **BWEmployee** | - | - | Own only (if_owner) |
| **BWCompany** | - | Full | - |

---

## Key Technical Details

### Data Model
- **Hierarchical structure**: Company → Department → Employee
- **Automatic counts**: Department and employee counts updated on create/update/delete
- **Days employed**: Calculated client-side from `hired_on` date

### Validation Rules
- Email: Frappe's built-in validation + duplicate check
- Phone: Regex pattern `^\+?\d{8,15}$` (8-15 digits, optional `+` prefix)
- `hired_on`/`days_employeed`: Only settable when `employee_status = "Hired"`, otherwise enforced empty
- Referential integrity: Department must belong to selected company

### Automated Features
- Employee counts updated automatically in departments and companies
- Days employed calculated in real-time
- Role and admin user creation during migration

---

## Development

### Running Tests
```bash
bench --site <site-name> run-tests --app employee_management
```

### Code Formatting
Uses `pre-commit` hooks with ruff (Python), eslint/prettier (JavaScript).

### Debugging
```bash
bench --site <site-name> set-config developer_mode 1
bench --site <site-name> logs
bench --site <site-name> console
```


**Last Updated**: December 2025  
**Application Version**: 1.0.0  
**Frappe Version**: 15.x
