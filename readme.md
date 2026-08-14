# 🏦 Mini Bank System

A desktop banking application built with **Python, PyQt6, SQLite, bcrypt, and pytest**.

This project was developed as a hands-on learning journey to understand how a real-world application can be structured using **layered architecture**, separation of responsibilities, secure authentication, database transactions, automated testing, mocking, and GUI development.

The project intentionally separates the application into three primary layers:

```text
┌──────────────────────────────┐
│          GUI Layer           │
│           PyQt6              │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Backend Layer          │
│      Business Logic          │
└──────────────┬───────────────┘
               │
               ▼
┌──────────────────────────────┐
│       Database Layer         │
│          SQLite              │
└──────────────────────────────┘
```

The goal is not to reproduce a production banking platform, but to build a realistic learning project while applying software engineering principles progressively.

---

# 📌 Project Overview

The Mini Bank System provides the core functionality expected from a small desktop banking application.

Users can:

* Create a bank account
* Log in securely
* Check account balance
* Deposit money
* Withdraw money
* Transfer money
* View transaction history
* Change their password
* Delete their account

The project also includes automated tests for the **Database, Backend, and GUI layers**.

---

# 🚀 Current Features

## 🔐 User Authentication

* Create New Account
* Login with Username & Password
* Username Validation
* Password Validation
* Duplicate Username Detection
* Secure Password Storage using bcrypt
* Account Number Generation
* Failed Login Attempt Tracking
* Account Locking
* Login Attempt Reset

---

## 🛡️ Password Security

Passwords are **never stored as plain text**.

For example, instead of storing:

```text
password123
```

the database stores a bcrypt hash:

```text
$2b$12$Pc4Qd5YJ....
```

Password verification is performed using bcrypt rather than comparing the plain-text password with the stored hash.

### Password Features

* bcrypt password hashing
* Password verification
* Minimum password length validation
* Change Password functionality
* Current password verification
* New password confirmation

---

# 💰 Banking Features

## Account Balance

Users can view their current account balance.

```text
Account
   │
   ▼
Get Balance
   │
   ▼
Display Current Balance
```

---

## Deposit Money

Users can deposit money into their account.

The system:

1. Validates the amount.
2. Checks that the amount is greater than zero.
3. Updates the account balance.
4. Records the transaction.
5. Stores the balance after the transaction.

---

## Withdraw Money

Users can withdraw money from their account.

The system:

1. Validates the amount.
2. Checks that the account exists.
3. Retrieves the current balance.
4. Checks sufficient funds.
5. Updates the balance.
6. Records the transaction.

Insufficient balance is rejected.

---

## Transfer Money

Users can transfer money between accounts.

The system validates:

* Sender account
* Receiver account
* Transfer amount
* Same-account transfers
* Sufficient balance

A transfer updates both accounts:

```text
Sender
  │
  │  - Amount
  ▼
Receiver
  │
  │  + Amount
  ▼
Transaction History
```

The transfer uses a database transaction so that both balance updates succeed together or the operation is rolled back.

---

## Transaction History

Every financial transaction is recorded.

Supported transaction types include:

```text
Deposit
Withdraw
Transfer Out
Transfer In
```

Each transaction stores:

* Account number
* Transaction type
* Amount
* Balance after transaction
* Transaction timestamp

Transactions are displayed in reverse chronological order.

---

# 🔑 Change Password

Users can change their password after logging in.

The process is:

```text
Current Password
       ↓
New Password
       ↓
Confirm Password
       ↓
Validate
       ↓
Verify Current Password
       ↓
Hash New Password
       ↓
Update Database
       ↓
Logout
       ↓
Login With New Password
```

### Current Password Validation

The current password must be correct before the new password can be stored.

### Password Rules

The project currently uses a simple password-strength rule:

```text
Minimum 8 characters
```

The new password must also:

* Match the confirmation password.
* Be different from the current password.

---

# 🗑️ Delete Account

Users can permanently delete their account.

The system requires the user's current password before deletion.

The deletion process is:

```text
Enter Password
      ↓
Verify Password
      ↓
Delete Transactions
      ↓
Delete User
      ↓
Commit
```

If any part of the database operation fails, the transaction is rolled back.

This prevents partially completed account deletion.

---

# 🖥️ GUI

The application is built using **PyQt6**.

## Login Page

The Login Page provides:

* Username input
* Password input
* Show / Hide Password
* Login button
* Create Account button
* Exit button

### 📸 Screenshot — Login Page

> **Add screenshot here**

```text
[ SCREENSHOT: GUI/login_page.py ]
```

---

## Create Account Page

Provides:

* Username input
* Password input
* Confirm Password input
* Account creation
* Validation messages
* Back button

### 📸 Screenshot — Create Account Page

> **Add screenshot here**

```text
[ SCREENSHOT: GUI/create_account_page.py ]
```

---

## Welcome Page

After successful login, the user reaches the main banking dashboard.

Available operations include:

```text
Check Balance
Deposit
Withdraw
Transfer
Transaction History
Change Password
Delete Account
```

### 📸 Screenshot — Welcome Page

> **Add screenshot here**

```text
[ SCREENSHOT: GUI/welcome_page.py ]
```

---

## Balance Page

Displays the current account balance.

### 📸 Screenshot — Balance Page

> **Add screenshot here**

```text
[ SCREENSHOT: GUI/balance_page.py ]
```

---

## Deposit Page

Allows the user to enter an amount and deposit money.

### 📸 Screenshot — Deposit Page

> **Add screenshot here**

```text
[ SCREENSHOT: GUI/deposit_page.py ]
```

---

## Withdraw Page

Allows the user to withdraw money while checking sufficient balance.

### 📸 Screenshot — Withdraw Page

> **Add screenshot here**

```text
[ SCREENSHOT: GUI/withdraw_page.py ]
```

---

## Transfer Page

Allows the user to transfer money to another account.

### 📸 Screenshot — Transfer Page

> **Add screenshot here**

```text
[ SCREENSHOT: GUI/transfer_page.py ]
```

---

## Transaction History Page

Displays the user's recorded transactions.

### 📸 Screenshot — Transaction History Page

> **Add screenshot here**

```text
[ SCREENSHOT: GUI/history_page.py ]
```

---

## Change Password Page

Allows the logged-in user to change their password.

### 📸 Screenshot — Change Password Page

> **Add screenshot here**

```text
[ SCREENSHOT: GUI/change_password_page.py ]
```

---

## Delete Account Page

Provides secure account deletion with password verification and confirmation.

### 📸 Screenshot — Delete Account Page

> **Add screenshot here**

```text
[ SCREENSHOT: GUI/delete_account_page.py ]
```

---

# 🏗️ Application Architecture

The application follows a layered architecture.

```text
                    ┌──────────────┐
                    │    User      │
                    └──────┬───────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │     GUI Layer     │
                 │      PyQt6        │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │   Backend Layer   │
                 │ Business Logic    │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Database Layer    │
                 │      SQLite       │
                 └───────────────────┘
```

---

# 📂 Project Structure

The current project is organized approximately as follows:

```text
Mini_Bank_System/
│
├── main.py
│
├── GUI/
│   ├── __init__.py
│   ├── login_page.py
│   ├── create_account_page.py
│   ├── welcome_page.py
│   ├── balance_page.py
│   ├── deposit_page.py
│   ├── withdraw_page.py
│   ├── transfer_page.py
│   ├── history_page.py
│   ├── change_password_page.py
│   └── delete_account_page.py
│
├── Backend/
│   ├── __init__.py
│   ├── account_service.py
│   ├── auth_service.py
│   ├── validators.py
│   └── security.py
│
├── Database/
│   ├── __init__.py
│   ├── sqlitedb.py
│   └── xyz_bank.db
│
├── Tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── sqlitedb_test.py
│   │
│   ├── test_Backend/
│   │   └── test_account_service.py
│   │
│   └── test_GUI/
│       ├── test_login.py
│       ├── test_create_account.py
│       ├── test_transfer_page.py
│       ├── test_transaction_history.py
│       ├── change_password_page_test.py
│       └── ...
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 🧩 Layer Responsibilities

## GUI Layer

The GUI is responsible for:

* Displaying information
* Collecting user input
* Handling button clicks
* Displaying success/error messages
* Navigating between pages

The GUI does **not** directly access SQLite.

Example:

```text
GUI
 ↓
Backend
```

---

## Backend Layer

The Backend contains business logic.

Examples:

```python
deposit_money()
withdraw_money()
transfer_money()
change_password()
delete_account()
get_transaction_history()
```

The Backend decides whether an operation is valid.

For example:

```text
Transfer Request
      ↓
Validate Amount
      ↓
Check Sender
      ↓
Check Receiver
      ↓
Check Balance
      ↓
Database Operation
```

---

## Database Layer

The Database layer is responsible for SQLite operations.

Examples:

```python
get_balance()
deposit_money()
withdraw_money()
transfer_money()
add_transaction()
get_transactions()
update_password()
delete_account()
```

The database layer does not contain GUI logic.

---

# 🗄️ Database Design

The application currently uses SQLite.

Database:

```text
Database/xyz_bank.db
```

## Users Table

```text
users
├── id
├── account_number
├── username
├── password
├── balance
├── failed_attempts
└── locked_until
```

---

## Transactions Table

```text
transactions
├── id
├── account_number
├── transaction_type
├── amount
├── balance_after
└── transaction_time
```

### Transaction Relationship

Transactions are associated with an account through:

```text
account_number
```

Conceptually:

```text
User Account
     │
     ├── Deposit
     ├── Withdraw
     ├── Transfer Out
     └── Transfer In
```

---

# 🔄 Database Transactions

Financial operations that involve multiple database changes use transactions.

For example, a transfer:

```text
BEGIN
  │
  ├── Decrease Sender Balance
  │
  ├── Increase Receiver Balance
  │
  ├── Record Sender Transaction
  │
  ├── Record Receiver Transaction
  │
  ▼
COMMIT
```

If an operation fails:

```text
ROLLBACK
```

This prevents inconsistent account balances.

---

# 🔐 Security Architecture

The project uses bcrypt for password hashing.

```text
Plain Password
      │
      ▼
bcrypt
      │
      ▼
Password Hash
      │
      ▼
SQLite
```

During login:

```text
User Password
      │
      ▼
bcrypt.verify()
      │
      ▼
Stored Hash
      │
      ▼
True / False
```

The application never needs to decrypt the stored password hash.

---

# 🧪 Testing Strategy

The project uses:

* **pytest**
* **pytest-qt**
* **unittest.mock**

Testing is separated according to application layers.

```text
                 Tests
                   │
       ┌───────────┼───────────┐
       │           │           │
       ▼           ▼           ▼
   Database     Backend       GUI
    Tests        Tests       Tests
```

---

# 🧪 Backend Testing

Backend tests use mocking to isolate business logic.

Example:

```python
@patch("Backend.account_service.sqlitedb")
def test_transfer_money_database_failure(mock_db):
    ...
```

The real SQLite database is not used.

Instead:

```text
Backend
   ↓
Mock Database
```

This makes backend tests:

* Fast
* Isolated
* Predictable
* Independent from database state

---

# 🗄️ Database Testing

Database tests use a dedicated test database fixture.

Example:

```python
def test_reset_login_attempts(test_db):
    ...
```

These tests intentionally execute real SQLite operations.

Database tests verify:

* User creation
* User lookup
* Balance operations
* Deposits
* Withdrawals
* Transfers
* Transactions
* Password updates
* Account deletion
* Login attempt handling

---

# 🖥️ GUI Testing

GUI tests use **pytest-qt**.

Example:

```python
@patch("GUI.transfer_page.transfer_money")
def test_transfer_button_click(mock_transfer, qtbot):
    ...
```

GUI tests verify things such as:

* Page creation
* Button clicks
* Input fields
* Backend calls
* Navigation
* Success/error handling

The backend is mocked so that GUI tests focus on GUI behavior.

---

# 🎭 Mocking Strategy

The project uses mocking to isolate individual layers.

### Backend Test

```text
Test
 ↓
Backend
 ↓
Mock Database
```

### GUI Test

```text
Test
 ↓
GUI
 ↓
Mock Backend
```

### Database Test

```text
Test
 ↓
Real Test Database
 ↓
SQLite
```

This separation makes it easier to determine exactly where a problem exists.

---

# 📊 Test Coverage

Test coverage is measured using `pytest-cov`.

Run:

```bash
pytest --cov=Backend --cov=Database --cov-report=term-missing
```

Coverage reports help identify code paths that have not yet been tested.

The project uses coverage not merely as a percentage target, but as a tool for finding missing test scenarios.

---

# 🧠 Important Software Engineering Concepts Learned

This project has been used to practice:

### Python

* Classes
* Objects
* Methods
* `self`
* Exception handling
* Tuples
* Functions
* Imports
* Modules
* Package structure

### GUI Development

* PyQt6
* Widgets
* Layouts
* Signals and slots
* `QStackedWidget`
* Dialog boxes
* GUI state management

### Backend Development

* Service-layer architecture
* Business validation
* Separation of concerns
* Error handling
* Return-value conventions

### Database

* SQLite
* SQL queries
* Parameterized queries
* `SELECT`
* `INSERT`
* `UPDATE`
* `DELETE`
* `COMMIT`
* `ROLLBACK`
* Database transactions

### Security

* bcrypt
* Password hashing
* Password verification
* Re-authentication
* Password change
* Account deletion security
* Account lockout

### Testing

* pytest
* pytest-qt
* Fixtures
* Assertions
* Mocking
* `@patch`
* GUI testing
* Database testing
* Code coverage

### Software Architecture

* Layered architecture
* Separation of responsibilities
* GUI → Backend → Database
* Dependency isolation
* Transaction boundaries
* Test isolation

---

# 📸 Code Architecture Screenshots

This section can be used to document the implementation and learning process.

## Backend Service

> **Attach screenshot of `Backend/account_service.py` here**

```text
[ SCREENSHOT — Backend/account_service.py ]
```

---

## Database Implementation

> **Attach screenshot of `Database/sqlitedb.py` here**

```text
[ SCREENSHOT — Database/sqlitedb.py ]
```

---

## Authentication & Security

> **Attach screenshot of `Backend/security.py` here**

```text
[ SCREENSHOT — Backend/security.py ]
```

---

## GUI Implementation

> **Attach screenshot of one or more GUI page implementations here**

```text
[ SCREENSHOT — GUI implementation ]
```

---

## Testing

> **Attach screenshot of pytest test cases here**

```text
[ SCREENSHOT — Tests ]
```

---

## Test Coverage

> **Attach screenshot of pytest coverage output here**

```text
[ SCREENSHOT — Test Coverage ]
```

---

# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/namansinghpatel/Python_Progs/tree/main/Python_Codes/Mini_Bank_System
```

> **Note:** If this repository is later moved to a dedicated GitHub repository, update this URL accordingly.

---

## Navigate to Project

```bash
cd Mini_Bank_System
```

---

## Create Virtual Environment

### Windows

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv venv
```

Activate:

```bash
source venv/bin/activate
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Application

```bash
python main.py
```

---

# 🧪 Run Tests

Run all tests:

```bash
pytest
```

Verbose output:

```bash
pytest -v
```

Run Backend tests:

```bash
pytest Tests/test_Backend/
```

Run GUI tests:

```bash
pytest Tests/test_GUI/
```

Run Database tests:

```bash
pytest Tests/sqlitedb_test.py
```

Run with coverage:

```bash
pytest --cov=Backend --cov=Database --cov-report=term-missing
```

---

# 🔄 Application Flow

## Create Account

```text
Create Account
      ↓
Validate Input
      ↓
Check Duplicate Username
      ↓
Generate Account Number
      ↓
Hash Password
      ↓
Store User
      ↓
Success
```

---

## Login

```text
Login
  ↓
Validate Input
  ↓
Check Account Lock
  ↓
Fetch Password Hash
  ↓
Verify Password
  ↓
Reset Attempts
  ↓
Welcome Page
```

Failed authentication follows the account-locking rules implemented by the application.

---

## Deposit

```text
Deposit Request
      ↓
Validate Amount
      ↓
Update Balance
      ↓
Get New Balance
      ↓
Record Transaction
      ↓
Commit
```

---

## Withdraw

```text
Withdraw Request
      ↓
Validate Amount
      ↓
Get Current Balance
      ↓
Check Sufficient Balance
      ↓
Update Balance
      ↓
Record Transaction
      ↓
Commit
```

---

## Transfer

```text
Transfer Request
      ↓
Validate Accounts
      ↓
Validate Amount
      ↓
Check Balance
      ↓
BEGIN TRANSACTION
      ↓
Decrease Sender Balance
      ↓
Increase Receiver Balance
      ↓
Record Both Transactions
      ↓
COMMIT
```

If something fails:

```text
ROLLBACK
```

---

## Change Password

```text
Change Password
      ↓
Validate Input
      ↓
Verify Current Password
      ↓
Validate New Password
      ↓
Hash New Password
      ↓
Update Password
      ↓
Success
      ↓
Return To Login
```

---

## Delete Account

```text
Delete Account
      ↓
Confirm User Action
      ↓
Verify Password
      ↓
BEGIN TRANSACTION
      ↓
Delete Transactions
      ↓
Delete User
      ↓
COMMIT
      ↓
Return To Login
```

---

# 🛣️ Future Roadmap

The following features are planned for future versions.

## Banking Features

* [ ] Profile / Account Dashboard
* [ ] Mini Statement
* [ ] Transaction Search & Filtering
* [ ] Export Bank Statement
* [ ] Account Information Page
* [ ] Interest Calculator
* [ ] Loan Calculator

---

## Security

* [ ] Forgot Password
* [ ] OTP Verification
* [ ] Session Management
* [ ] Role-Based Access Control
* [ ] Admin Authentication
* [ ] Audit Logs
* [ ] Stronger Password Policies
* [ ] Additional protection for sensitive operations

---

## Administration

* [ ] Admin Dashboard
* [ ] View All Accounts
* [ ] Search Accounts
* [ ] Lock / Unlock Accounts
* [ ] Account Management
* [ ] Bank-wide Statistics

---

## Testing

* [ ] Expand GUI Navigation Coverage
* [ ] End-to-End Tests
* [ ] Integration Tests
* [ ] Performance Testing
* [ ] Security Testing
* [ ] Increase and maintain high test coverage

---

# 🎯 Learning Objectives

This project is being developed incrementally rather than being generated as one large application.

Each feature follows the same development cycle:

```text
Requirement
    ↓
Understand Flow
    ↓
Database Design
    ↓
Backend Implementation
    ↓
GUI Implementation
    ↓
Database Tests
    ↓
Backend Tests
    ↓
GUI Tests
    ↓
Coverage Analysis
    ↓
Bug Fixing
```

This workflow is one of the most important outcomes of the project.

The goal is to understand **how software is designed, implemented, tested, debugged, and improved**, rather than simply writing code that works.

---

# 📚 Project Learning Journey

The Mini Bank System started as a basic Python banking application and has gradually evolved into a layered desktop application.

Major milestones include:

```text
Basic Python Banking Logic
          ↓
SQLite Database
          ↓
Authentication
          ↓
PyQt6 GUI
          ↓
Backend / Database Separation
          ↓
Secure Password Hashing
          ↓
Account Locking
          ↓
Financial Transactions
          ↓
Transaction History
          ↓
Database Transactions
          ↓
Account Deletion
          ↓
Password Change
          ↓
Automated Testing
          ↓
Mocking & Test Isolation
          ↓
Coverage Analysis
```

---

# ⚠️ Disclaimer

This application is a **learning project** and is not intended for handling real financial accounts, real money, or production banking data.

A production banking system would require significantly stronger security, compliance, auditing, encryption, infrastructure, reliability, monitoring, and regulatory controls.

---

# 👨‍💻 Author

**Naman Singh Patel**

Built as a learning project to understand:

* Python application development
* PyQt6 GUI development
* SQLite database design
* Authentication and security
* Backend architecture
* Automated testing
* Software engineering principles

---

# ⭐ Project Goal

The long-term goal of this project is to continuously evolve a simple Python banking application into a more complete software system while learning professional development practices along the way.

```text
Learn
  ↓
Build
  ↓
Test
  ↓
Debug
  ↓
Improve
  ↓
Repeat
```

---
