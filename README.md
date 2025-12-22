# Employee Management Application

A comprehensive Frappe-based application for managing companies, departments, and employees with RESTful API support and role-based access control.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture & Implementation](#architecture--implementation)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Setup Instructions](#setup-instructions)
- [Task Completion Checklist](#task-completion-checklist)
- [Security Measures](#security-measures)
- [API Documentation](#api-documentation)
- [Usage Guide](#usage-guide)
- [Development](#development)
- [Contributing](#contributing)
- [License](#license)

---

## Overview

The Employee Management application is built on the Frappe framework (version 15) and provides a complete solution for managing organizational hierarchies. It enables administrators to create companies, organize departments within companies, and manage employee records with comprehensive validation and automated calculations.

### Key Capabilities

- **Company Management**: Create and manage company records with automatic department and employee count tracking
- **Department Management**: Organize departments within companies with employee count tracking
- **Employee Management**: Comprehensive employee records with validation, status tracking, and automated calculations
- **RESTful API**: Full CRUD operations via REST API with OpenAPI 3.0 documentation
- **Role-Based Access Control**: Granular permissions for different user roles
- **Data Validation**: Email, phone number, and referential integrity validation
- **Automated Calculations**: Days employed and employee counts are automatically calculated

---

## Features

### Core Features

✅ **Company Management**
- Create, read, update, and delete company records
- Automatic tracking of number of departments and employees
- Prevents deletion if departments or employees exist

✅ **Department Management**
- Create departments linked to companies
- Automatic employee count tracking
- Prevents deletion if employees exist
- Auto-updates company counts when departments change

✅ **Employee Management**
- Complete employee profile management
- Email and phone number validation
- Duplicate email prevention
- Department-company relationship validation
- Automatic calculation of days employed
- Employee status tracking (Application Received, Interview Scheduled, Hired, Not Accepted)

✅ **REST API**
- Full CRUD operations for all resources
- Authentication endpoints (login, account, update profile)
- Comprehensive OpenAPI 3.0 documentation
- Support for filtering, pagination, and field selection

✅ **User Interface**
- Standard Frappe forms with enhanced JavaScript interactions
- Department filtering based on selected company
- Real-time calculation of days employed
- Responsive design

---

## Architecture & Implementation

### Technology Stack

- **Framework**: Frappe Framework (v15)
- **Backend**: Python 3.10+
- **Database**: MariaDB/PostgreSQL (via Frappe)
- **Frontend**: Frappe UI (JavaScript/jQuery)
- **API Documentation**: OpenAPI 3.0.3 (Swagger)

### Application Structure

```
employee_management/
├── employee_management/
│   ├── auth.py                    # Authentication API endpoints
│   ├── hooks.py                   # Frappe hooks configuration
│   └── employee_management/
│       └── doctype/
│           ├── bwcompany/         # Company DocType
│           ├── bwdepartment/      # Department DocType
│           └── bwemployee/        # Employee DocType
├── openapi.yaml                   # API documentation (OpenAPI 3.0)
├── README.md                      # This file
└── EVALUATION_REPORT.md           # Detailed evaluation report
```

### Implementation Approach

#### 1. Data Model Design

The application follows a hierarchical data model:
- **Company** (Top level)
  - **Department** (Linked to Company)
    - **Employee** (Linked to both Company and Department)

This structure ensures:
- Data integrity through referential relationships
- Automatic count updates when records change
- Prevention of orphaned records

#### 2. Validation Strategy

**Email Validation**:
- Uses Frappe's built-in `validate_email_address()` function
- Checks for duplicate emails across all employees
- Throws validation errors with clear messages

**Phone Number Validation**:
- Custom regex pattern: `^\+?\d{8,15}$`
- Allows optional `+` prefix
- Requires 8-15 digits
- Validates format before saving

**Referential Integrity**:
- Validates that selected department belongs to selected company
- Prevents deletion of companies/departments with related records
- Ensures data consistency

#### 3. Automated Calculations

**Employee Counts**:
- Automatically updated when employees are created, updated, or deleted
- Uses `frappe.db.count()` for efficient counting
- Updates both department and company counts

**Days Employed**:
- Calculated in JavaScript on form load and when `hired_on` changes
- Uses client-side date calculation for real-time updates
- Formula: `(Today - Hired Date) in days`

#### 4. API Design

**RESTful Principles**:
- Standard HTTP methods (GET, POST, PUT, DELETE)
- Resource-based URLs (`/api/resource/{DocType}`)
- Consistent response formats
- Proper HTTP status codes

**Authentication**:
- Session-based authentication (cookie)
- API key authentication (token-based)
- Login endpoint for session creation
- Account endpoint for user information retrieval

#### 5. Security Implementation

**Role-Based Access Control (RBAC)**:
- Four distinct roles with different permission levels
- Document-level permissions (if_owner)
- Field-level read-only restrictions

**Input Validation**:
- Server-side validation for all inputs
- Type checking and format validation
- SQL injection prevention (via Frappe ORM)
- XSS protection (via Frappe's built-in sanitization)

### Design Decisions & Considerations

1. **Why Frappe Framework?**
   - Built-in ORM reduces boilerplate code
   - Automatic form generation
   - Integrated permission system
   - REST API out of the box

2. **Why Separate DocTypes?**
   - Clear separation of concerns
   - Independent permission management
   - Easier to extend and maintain
   - Better data organization

3. **Why Client-Side Days Calculation?**
   - Real-time user feedback
   - Reduces server load
   - Better user experience

4. **Why OpenAPI Documentation?**
   - Industry standard for API documentation
   - Tool-agnostic (works with Swagger, Postman, etc.)
   - Auto-generates client SDKs
   - Clear contract definition

---

## Prerequisites

Before installing the Employee Management application, ensure you have:

### Required Software

1. **Python 3.10 or higher**
   ```bash
   python3 --version  # Should be 3.10+
   ```

2. **Node.js 18+ and npm**
   ```bash
   node --version  # Should be 18+
   npm --version
   ```

3. **MariaDB 10.3+ or PostgreSQL 12+**
   - MariaDB is recommended for Frappe
   - Database server should be running and accessible

4. **Redis** (for caching and background jobs)
   ```bash
   redis-cli ping  # Should return PONG
   ```

5. **Git**
   ```bash
   git --version
   ```

### Frappe Bench

The application requires Frappe Bench to be installed. If you don't have it:

```bash
# Install bench
pip3 install frappe-bench

# Or using pipx (recommended)
pipx install frappe-bench
```

### System Requirements

- **Operating System**: Linux, macOS, or WSL2 (Windows)
- **RAM**: Minimum 4GB (8GB recommended)
- **Disk Space**: At least 2GB free space
- **Network**: Internet connection for initial setup

---

## Installation

### Step 1: Clone or Download the Application

If the application is in a Git repository:

```bash
cd /path/to/your/bench/apps
git clone <repository-url> employee_management
cd employee_management
```

If you have the application files locally, ensure they are in the `apps` directory of your Frappe bench.

### Step 2: Install Dependencies

The application uses Frappe's dependency management. Dependencies are automatically installed when you install the app.

### Step 3: Install the Application

From your Frappe bench directory:

```bash
# Navigate to bench directory
cd /path/to/your/bench

# Install the app
bench --site <your-site-name> install-app employee_management

# Example:
bench --site development.localhost install-app employee_management
```

### Step 4: Migrate Database

After installation, migrate the database to create the DocTypes:

```bash
bench --site <your-site-name> migrate
```

### Step 5: Build Assets (if needed)

Build frontend assets:

```bash
bench build --app employee_management
```

Or build all apps:

```bash
bench build
```

---

## Setup Instructions

### Initial Setup

1. **Create a Frappe Site** (if you don't have one):
   ```bash
   bench new-site <site-name>
   # Example: bench new-site development.localhost
   ```

2. **Install the Application**:
   ```bash
   bench --site <site-name> install-app employee_management
   ```

3. **Set Up Roles** (if not automatically created):
   - Navigate to: **Setup > Users and Permissions > Role**
   - Create the following roles if they don't exist:
     - `BWAdmin` - Full administrative access
     - `BWManager` - Manager-level access
     - `BWEmployee` - Employee-level access
     - `BWCompany` - Company-level access

4. **Assign Roles to Users**:
   - Go to: **Setup > Users and Permissions > User**
   - Edit users and assign appropriate roles

### Configuration

#### Database Configuration

The application uses Frappe's default database configuration. Ensure your `site_config.json` has proper database settings:

```json
{
  "db_name": "your_database_name",
  "db_host": "localhost",
  "db_port": 3306,
  "db_type": "mariadb"
}
```

#### API Configuration

The API is accessible at:
- **Base URL**: `http://your-site.com/api` (development) or `https://your-site.com/api` (production)
- **Local Development**: `http://localhost:8000/api` (default Frappe port)

### Running the Application

#### Development Mode

1. **Start the development server**:
   ```bash
   bench start
   ```

2. **Access the application**:
   - Web Interface: `http://localhost:8000`
   - API Base: `http://localhost:8000/api`

#### Production Mode

1. **Set up production configuration**:
   ```bash
   bench setup production
   ```

2. **Use a process manager** (PM2 recommended):
   ```bash
   bench setup supervisor
   sudo supervisorctl start all
   ```

3. **Set up Nginx** (for production):
   ```bash
   bench setup nginx
   sudo service nginx reload
   ```

### Additional Setup for API Access

1. **Generate API Keys** (for programmatic access):
   - Navigate to: **User > API Access**
   - Generate API Key and API Secret
   - Use format: `Authorization: token <api_key>:<api_secret>`

2. **Enable CORS** (if accessing from external domains):
   - Edit `site_config.json`:
   ```json
   {
     "allow_cors": "*"
   }
   ```

---

## Task Completion Checklist

### ✅ Completed Tasks

#### Core Functionality
- [x] **Company Management**
  - [x] Create Company DocType with required fields
  - [x] Implement company name validation
  - [x] Auto-calculate number of departments
  - [x] Auto-calculate number of employees
  - [x] Prevent deletion if departments/employees exist
  - [x] CRUD operations via API

- [x] **Department Management**
  - [x] Create Department DocType linked to Company
  - [x] Implement company and department name validation
  - [x] Auto-calculate number of employees
  - [x] Auto-update company counts on department changes
  - [x] Prevent deletion if employees exist
  - [x] CRUD operations via API

- [x] **Employee Management**
  - [x] Create Employee DocType with all required fields
  - [x] Link employee to Company and Department
  - [x] Implement email validation
  - [x] Implement phone number validation
  - [x] Prevent duplicate emails
  - [x] Validate department belongs to company
  - [x] Auto-calculate days employed
  - [x] Employee status tracking
  - [x] Auto-update department and company employee counts
  - [x] CRUD operations via API

#### API Development
- [x] **Authentication API**
  - [x] Login endpoint (`/api/method/employee_management.auth.login`)
  - [x] Account information endpoint (`/api/method/employee_management.auth.account`)
  - [x] Update profile endpoint (`/api/method/employee_management.auth.update_profile`)

- [x] **Resource API**
  - [x] Company endpoints (GET, POST, PUT, DELETE)
  - [x] Department endpoints (GET, POST, PUT, DELETE)
  - [x] Employee endpoints (GET, POST, PUT, DELETE)
  - [x] Filtering and pagination support
  - [x] Field selection support

#### Documentation
- [x] **API Documentation**
  - [x] Complete OpenAPI 3.0.3 specification
  - [x] All endpoints documented
  - [x] Request/response schemas defined
  - [x] Authentication methods documented
  - [x] Examples provided

- [x] **Code Documentation**
  - [x] README.md with setup instructions
  - [x] Code comments where necessary
  - [x] Evaluation report

#### Security & Permissions
- [x] **Role-Based Access Control**
  - [x] Define roles (BWAdmin, BWManager, BWEmployee, BWCompany)
  - [x] Set permissions for each role
  - [x] Implement document-level permissions
  - [x] Field-level read-only restrictions

- [x] **Data Validation**
  - [x] Email format validation
  - [x] Phone number format validation
  - [x] Duplicate email prevention
  - [x] Referential integrity checks

### ⚠️ Partially Completed / Future Enhancements

- [ ] **Workflow Implementation**
  - [ ] Employee status workflow (planned but not implemented)
  - [ ] Validate `hired_on` when status changes to "Hired"

- [ ] **Data Visualizations**
  - [ ] Dashboard with employee statistics
  - [ ] Charts for department distribution
  - [ ] Reports with visual elements

- [ ] **Advanced Features**
  - [ ] Manager detection logic (`is_manager` field exists but not implemented)
  - [ ] Email notifications
  - [ ] Custom reports
  - [ ] Export functionality enhancements

### Assumptions Made

1. **Frappe Framework**: Assumes users are familiar with Frappe framework or have access to Frappe documentation
2. **Database**: Assumes MariaDB or PostgreSQL is already set up and configured
3. **Roles**: Assumes roles will be created manually or via migration scripts
4. **API Usage**: Assumes API consumers understand REST principles and OpenAPI documentation
5. **Email Format**: Uses standard email validation; assumes international phone number format with optional `+` prefix
6. **Date Format**: Uses ISO 8601 date format (YYYY-MM-DD) for dates
7. **Session Management**: Relies on Frappe's built-in session management
8. **Error Handling**: Uses Frappe's standard error handling mechanisms

### Considerations

1. **Performance**: 
   - Count calculations happen on every save (acceptable for small to medium datasets)
   - For large datasets, consider caching or background jobs

2. **Scalability**:
   - Current implementation is suitable for organizations with hundreds to thousands of employees
   - For larger scale, consider indexing and query optimization

3. **Data Migration**:
   - No migration scripts provided; assumes fresh installation
   - For existing data, manual migration may be required

4. **Internationalization**:
   - Error messages are in English
   - Can be extended with Frappe's translation system

5. **Browser Compatibility**:
   - JavaScript features require modern browsers (ES6+)
   - Form interactions tested on Chrome, Firefox, Safari

---

## Security Measures

### Role-Based Access Control (RBAC)

The application implements a comprehensive role-based access control system with four distinct roles:

#### 1. System Manager
- **Full Access**: Complete CRUD operations on all resources
- **Permissions**: Create, Read, Update, Delete, Export, Print, Email, Share, Report
- **Use Case**: System administrators

#### 2. BWAdmin
- **Full Access**: Complete administrative control over Employee Management resources
- **Permissions**: Create, Read, Update, Delete, Export, Print, Email, Share, Report
- **Use Case**: Application administrators

#### 3. BWManager
- **Limited Write Access**: Can create and read employees, read-only for companies
- **Company Permissions**: Read-only
- **Department Permissions**: Read-only (if owner)
- **Employee Permissions**: Create, Read, Write
- **Use Case**: Department managers

#### 4. BWEmployee
- **Self-Service**: Can create and manage own employee record
- **Permissions**: Create, Read, Write, Share (only own records via `if_owner`)
- **Use Case**: Employees managing their own profiles

#### 5. BWCompany
- **Company-Specific Access**: Can manage departments within their company
- **Department Permissions**: Create, Delete, Read, Write, Share
- **Use Case**: Company administrators

### Permission Matrix

| Resource | System Manager | BWAdmin | BWManager | BWEmployee | BWCompany |
|----------|---------------|---------|-----------|------------|-----------|
| **Company** | Full | Full | Read | - | - |
| **Department** | Full | Full | Read (if owner) | - | Full |
| **Employee** | Full | Full | Create/Read/Write | Own only | - |

### Data Protection

#### 1. Input Validation

**Server-Side Validation**:
- All inputs are validated on the server before processing
- Email addresses validated using Frappe's `validate_email_address()`
- Phone numbers validated using regex pattern
- Date formats validated
- String length limits enforced

**Client-Side Validation**:
- Form-level validation before submission
- Real-time feedback for user experience
- Prevents invalid data submission

#### 2. SQL Injection Prevention

- Uses Frappe ORM for all database operations
- Parameterized queries (automatic via Frappe)
- No raw SQL queries
- Input sanitization built into framework

#### 3. XSS (Cross-Site Scripting) Protection

- Frappe automatically sanitizes user inputs
- Output encoding for all displayed data
- Content Security Policy (CSP) headers
- No inline JavaScript execution from user input

#### 4. CSRF (Cross-Site Request Forgery) Protection

- Frappe includes CSRF token validation
- Required for all state-changing operations (POST, PUT, DELETE)
- Token included in forms and API requests
- Automatic validation on server-side

#### 5. Authentication Security

**Login Endpoint**:
- Uses Frappe's built-in authentication system
- Password hashing (bcrypt)
- Session management with secure cookies
- Session expiration configured

**API Authentication**:
- API Key/Secret pairs for programmatic access
- Token-based authentication
- Session cookie authentication
- Both methods supported

#### 6. Authorization Checks

**Document-Level Permissions**:
- Checked on every read/write operation
- `if_owner` flag for owner-only access
- Role-based permission evaluation
- Enforced at database query level

**Field-Level Security**:
- Read-only fields cannot be modified
- Computed fields (like counts) are read-only
- Permission checks before field updates

#### 7. Data Integrity

**Referential Integrity**:
- Foreign key relationships enforced
- Prevents deletion of parent records with children
- Cascade updates where appropriate
- Validation before save operations

**Duplicate Prevention**:
- Email uniqueness enforced
- Database-level constraints
- Application-level checks before save

#### 8. Error Handling

**Information Leakage Prevention**:
- Generic error messages for authentication failures
- Detailed errors only for authorized users
- No stack traces in production
- Logging without exposing sensitive data

**Audit Trail**:
- Frappe automatically logs document changes
- `creation`, `modified`, `modified_by` fields tracked
- Activity log maintained
- User actions traceable

### Security Best Practices Implemented

✅ **Principle of Least Privilege**: Users only have permissions they need  
✅ **Defense in Depth**: Multiple layers of security (validation, permissions, encryption)  
✅ **Input Validation**: All inputs validated and sanitized  
✅ **Secure Defaults**: Restrictive permissions by default  
✅ **Error Handling**: Secure error messages without information leakage  
✅ **Session Management**: Secure session handling with expiration  
✅ **Password Security**: Relies on Frappe's secure password handling  

### Security Recommendations for Production

1. **Enable HTTPS**: Use SSL/TLS certificates for all API and web access
2. **Rate Limiting**: Implement rate limiting for login endpoint to prevent brute force attacks
3. **API Key Rotation**: Regularly rotate API keys
4. **Audit Logging**: Enable comprehensive audit logging
5. **Regular Updates**: Keep Frappe framework and dependencies updated
6. **Backup Strategy**: Regular database backups
7. **Environment Variables**: Store sensitive configuration in environment variables
8. **Firewall Rules**: Restrict database access to application servers only

---

## API Documentation

### Accessing API Documentation

The API documentation is available in OpenAPI 3.0.3 format in the file `openapi.yaml` located in the application root directory.

#### Viewing Documentation Online

1. **Swagger Editor** (Recommended):
   - Visit: https://editor.swagger.io/
   - Click "File" > "Import File"
   - Upload or paste the contents of `openapi.yaml`
   - View interactive API documentation

2. **Swagger UI** (Local):
   ```bash
   # Install swagger-ui-serve
   npm install -g swagger-ui-serve
   
   # Serve the documentation
   swagger-ui-serve openapi.yaml
   ```
   - Access at: `http://localhost:3000`

3. **Redoc**:
   ```bash
   # Install redoc-cli
   npm install -g redoc-cli
   
   # Serve documentation
   redoc-cli serve openapi.yaml
   ```
   - Access at: `http://localhost:8080`

#### Programmatic Access

The OpenAPI specification can be used to:
- Generate client SDKs in various languages
- Import into API testing tools (Postman, Insomnia)
- Generate server stubs
- Validate API requests/responses

### API Base URL

- **Development**: `http://localhost:8000/api` or `http://your-site.localhost:8013/api`
- **Production**: `https://your-domain.com/api`

### Authentication Methods

#### 1. Session Cookie Authentication

1. **Login** to get a session:
   ```bash
   POST /api/method/employee_management.auth.login
   Content-Type: application/json
   
   {
     "usr": "administrator@example.com",
     "pwd": "your_password"
   }
   ```

2. **Use Session Cookie** in subsequent requests:
   - Cookie `sid` is automatically set
   - Include cookie in all API requests
   - Session expires based on Frappe configuration

#### 2. API Key Authentication

1. **Generate API Key**:
   - Navigate to User > API Access
   - Generate API Key and API Secret

2. **Use in Requests**:
   ```bash
   Authorization: token <api_key>:<api_secret>
   ```

   Example:
   ```bash
   curl -H "Authorization: token abc123:secret456" \
        http://localhost:8000/api/resource/BWEmployee
   ```

### API Endpoints Overview

#### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/method/employee_management.auth.login` | User login |
| GET | `/api/method/employee_management.auth.account` | Get current user account |
| POST | `/api/method/employee_management.auth.update_profile` | Update user profile |

#### Resource Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/resource/BWCompany` | List companies |
| POST | `/api/resource/BWCompany` | Create company |
| GET | `/api/resource/BWCompany/{name}` | Get company |
| PUT | `/api/resource/BWCompany/{name}` | Update company |
| DELETE | `/api/resource/BWCompany/{name}` | Delete company |

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/resource/BWDepartment` | List departments |
| POST | `/api/resource/BWDepartment` | Create department |
| GET | `/api/resource/BWDepartment/{name}` | Get department |
| PUT | `/api/resource/BWDepartment/{name}` | Update department |
| DELETE | `/api/resource/BWDepartment/{name}` | Delete department |

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/resource/BWEmployee` | List employees |
| POST | `/api/resource/BWEmployee` | Create employee |
| GET | `/api/resource/BWEmployee/{name}` | Get employee |
| PUT | `/api/resource/BWEmployee/{name}` | Update employee |
| DELETE | `/api/resource/BWEmployee/{name}` | Delete employee |

### Query Parameters

#### Filtering

```bash
GET /api/resource/BWEmployee?filters={"company":"COMP-001","employee_status":"Hired"}
```

#### Pagination

```bash
GET /api/resource/BWEmployee?limit_start=0&limit_page_length=20
```

#### Field Selection

```bash
GET /api/resource/BWEmployee?fields=name,employee_name,email_address
```

#### Sorting

```bash
GET /api/resource/BWEmployee?order_by=modified desc
```

### Example API Calls

#### Create a Company

```bash
curl -X POST http://localhost:8000/api/resource/BWCompany \
  -H "Authorization: token <api_key>:<api_secret>" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Acme Corporation"
  }'
```

#### Create a Department

```bash
curl -X POST http://localhost:8000/api/resource/BWDepartment \
  -H "Authorization: token <api_key>:<api_secret>" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "COMP-00001",
    "department_name": "Engineering"
  }'
```

#### Create an Employee

```bash
curl -X POST http://localhost:8000/api/resource/BWEmployee \
  -H "Authorization: token <api_key>:<api_secret>" \
  -H "Content-Type: application/json" \
  -d '{
    "company": "COMP-00001",
    "department": "DEPT-00001",
    "employee_name": "John Doe",
    "email_address": "john.doe@example.com",
    "mobile_number": "+1-555-123-4567",
    "employee_status": "Hired",
    "hired_on": "2024-01-15"
  }'
```

#### Get Employees with Filters

```bash
curl -X GET "http://localhost:8000/api/resource/BWEmployee?filters=%7B%22company%22%3A%22COMP-00001%22%7D" \
  -H "Authorization: token <api_key>:<api_secret>"
```

### Response Formats

#### Success Response

```json
{
  "data": {
    "name": "EMP-00001",
    "employee_name": "John Doe",
    "email_address": "john.doe@example.com",
    ...
  }
}
```

#### Error Response

```json
{
  "exc_type": "ValidationError",
  "exc": "Email 'john.doe@example.com' is already linked to another employee.",
  "_server_messages": []
}
```

### HTTP Status Codes

- `200 OK`: Request successful
- `201 Created`: Resource created successfully
- `400 Bad Request`: Invalid input data
- `401 Unauthorized`: Authentication required
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Complete API Documentation

For complete API documentation including:
- All request/response schemas
- Detailed parameter descriptions
- Authentication methods
- Error responses
- Examples

Please refer to the `openapi.yaml` file in the application root directory or view it using one of the methods described above.

---

## Usage Guide

### Creating a Company

1. Navigate to **Employee Management > Company > New**
2. Enter **Company Name** (required)
3. Click **Save**
4. System automatically calculates department and employee counts

### Creating a Department

1. Navigate to **Employee Management > Department > New**
2. Select **Company** (required)
3. Enter **Department Name** (required)
4. Click **Save**
5. System automatically updates company counts

### Creating an Employee

1. Navigate to **Employee Management > Employee > New**
2. Select **Company** (required)
3. Select **Department** (required, filtered by company)
4. Enter **Employee Name** (required)
5. Enter **Email Address** (required, validated, must be unique)
6. Enter **Mobile Number** (required, validated)
7. Enter other optional fields
8. Select **Employee Status**
9. Enter **Hired On** date (if status is "Hired")
10. Click **Save**
11. System automatically:
    - Validates email and phone format
    - Checks for duplicate emails
    - Validates department belongs to company
    - Calculates days employed
    - Updates department and company employee counts

### Using the API

See [API Documentation](#api-documentation) section for detailed API usage examples.

---

## Development

### Code Structure

- **Python Files**: Located in `employee_management/` directory
- **JavaScript Files**: Located in `employee_management/employee_management/doctype/*/` directories
- **JSON Definitions**: DocType definitions in `doctype/*/*.json` files
- **API Documentation**: `openapi.yaml` in root directory

### Running Tests

```bash
# Run all tests
bench --site <site-name> run-tests --app employee_management

# Run specific test file
bench --site <site-name> run-tests --doctype BWEmployee
```

### Code Formatting

The project uses `pre-commit` hooks for code formatting:

```bash
# Install pre-commit
cd apps/employee_management
pre-commit install

# Run manually
pre-commit run --all-files
```

**Tools Used**:
- **ruff**: Python linting and formatting
- **eslint**: JavaScript linting
- **prettier**: Code formatting
- **pyupgrade**: Python version upgrades

### Development Workflow

1. Make changes to code
2. Pre-commit hooks automatically format code
3. Test locally
4. Commit changes
5. Push to repository

### Debugging

```bash
# Enable verbose logging
bench --site <site-name> set-config developer_mode 1

# View logs
bench --site <site-name> logs

# Console access
bench --site <site-name> console
```

---

## Contributing

### Contribution Guidelines

1. Follow Frappe coding standards
2. Write clear commit messages
3. Add tests for new features
4. Update documentation
5. Ensure pre-commit hooks pass

### Reporting Issues

When reporting issues, please include:
- Frappe version
- Application version
- Steps to reproduce
- Expected vs actual behavior
- Error messages/logs

---

## License

This application is licensed under the MIT License. See `license.txt` for details.

---

## Support

For issues, questions, or contributions:
- Check the [Frappe Documentation](https://frappeframework.com/docs)
- Review the `EVALUATION_REPORT.md` for known issues
- Contact: info@mail.com

---

## Changelog

### Version 1.0.0 (Current)
- Initial release
- Company, Department, and Employee management
- REST API with OpenAPI documentation
- Role-based access control
- Data validation and automated calculations

---

**Last Updated**: December 2024  
**Application Version**: 1.0.0  
**Frappe Version**: 15.x
