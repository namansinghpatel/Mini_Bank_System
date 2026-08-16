# 🏦 Mini Bank System

A desktop banking application built with **Python, PyQt6, SQLite, bcrypt, and pytest**.

This project is a hands-on learning journey focused on understanding how a real-world application can be designed, implemented, tested, debugged, and improved using layered architecture, separation of responsibilities, secure authentication, database transactions, automated testing, mocking, and GUI development.

> **Project status:** Core banking, authentication, transaction, account-management, GUI, and automated-testing features implemented.

---

# 📌 Table of Contents

- [Project Overview](#-project-overview)
- [Current Features](#-current-features)
- [Application Architecture](#-application-architecture)
- [Project Structure](#-project-structure)
- [GUI](#️-gui)
- [Authentication & Security](#-authentication--security)
- [Banking Operations](#-banking-operations)
- [Transaction System](#-transaction-system)
- [Account Management](#-account-management)
- [Database Design](#️-database-design)
- [Backend Services](#-backend-services)
- [Testing Strategy](#-testing-strategy)
- [Mocking Strategy](#-mocking-strategy)
- [Test Coverage](#-test-coverage)
- [Code Implementation Screenshots](#-code-implementation-screenshots)
- [Installation](#️-installation)
- [Running the Application](#️-running-the-application)
- [Running Tests](#-running-tests)
- [Application Flows](#-application-flows)
- [Software Engineering Concepts Learned](#-software-engineering-concepts-learned)
- [Development Workflow](#-development-workflow)
- [Future Roadmap](#️-future-roadmap)
- [Disclaimer](#️-disclaimer)
- [Author](#-author)

---

# 📌 Project Overview

The Mini Bank System is a desktop banking application designed as a practical Python software-engineering project.

The application provides:

- Account creation
- Secure login
- Account-number generation
- Password hashing and verification
- Failed-login tracking and account locking
- Balance checking
- Deposits
- Withdrawals
- Money transfers
- Transaction history
- Password changes
- Account deletion
- Automated Database tests
- Automated Backend tests
- Automated GUI tests
- Mocking and test isolation
- Coverage analysis

The application follows a simple layered architecture:

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
│           SQLite             │
└──────────────────────────────┘
```

The GUI is responsible for user interaction, the Backend is responsible for business rules, and the Database layer is responsible for persistent storage.

---

# 🚀 Current Features

## 🔐 User Authentication

- Create New Account
- Login with Username & Password
- Username validation
- Password validation
- Duplicate username detection
- Secure password storage using bcrypt
- Automatic account-number generation
- Failed login-attempt tracking
- Account locking
- Login-attempt reset

## 🛡️ Password Security

Passwords are never stored as plain text.

Example:

```text
Plain password:
password123

Stored value:
$2b$12$Pc4Qd5YJ....
```

The application uses bcrypt hashing and password verification.

### Password functionality

- bcrypt hashing
- bcrypt verification
- Minimum password-length validation
- Current-password verification
- New-password confirmation
- Change Password feature
- Re-authentication after password change

The current password-strength rule used by the application is intentionally simple:

```text
Minimum 8 characters
```

---

# 💰 Banking Operations

## 💵 Deposit

The deposit flow is:

```text
Deposit Request
      ↓
Validate Amount
      ↓
Check Amount > 0
      ↓
Update Balance
      ↓
Get Updated Balance
      ↓
Record Transaction
      ↓
Commit
```

A successful deposit records:

- Account number
- Transaction type
- Amount
- Balance after transaction
- Transaction timestamp

---

## 💸 Withdraw

The withdrawal flow is:

```text
Withdraw Request
      ↓
Validate Amount
      ↓
Check Account
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

The application rejects:

- Invalid amounts
- Zero or negative amounts
- Unknown accounts
- Withdrawals greater than the current balance

---

## 🔄 Transfer Money

Users can transfer money from one account to another.

Validation includes:

- Sender account exists
- Receiver account exists
- Amount is valid
- Sender and receiver are not the same account
- Sender has sufficient balance

The transfer is treated as one database transaction:

```text
BEGIN
  │
  ├── Decrease Sender Balance
  │
  ├── Increase Receiver Balance
  │
  ├── Record Transfer Out
  │
  ├── Record Transfer In
  │
  ▼
COMMIT
```

If an operation fails:

```text
ROLLBACK
```

This prevents a transfer from leaving the accounts in an inconsistent state.

---

# 📜 Transaction History

The application records financial transactions in a dedicated `transactions` table.

Supported transaction types:

```text
Deposit
Withdraw
Transfer Out
Transfer In
```

Each transaction contains:

- Account number
- Transaction type
- Amount
- Balance after transaction
- Transaction time

Transactions are retrieved in reverse order so the newest transaction appears first.

---

# 🔑 Change Password

The Change Password feature follows this flow:

```text
Current Password
       ↓
New Password
       ↓
Confirm Password
       ↓
Validate Inputs
       ↓
Verify Current Password
       ↓
Check New Password
       ↓
Hash New Password
       ↓
Update Database
       ↓
Success
       ↓
Return To Login
```

Validation includes:

- Current password cannot be empty
- New password cannot be empty
- Confirmation password cannot be empty
- New and confirmation passwords must match
- New password must be at least 8 characters
- New password must differ from the current password
- Current password must be correct
- Account must exist

The new password is hashed before it is stored.

Changing a password does **not** change transaction history or account balance.

---

# 🗑️ Delete Account

Account deletion requires password verification.

Flow:

```text
Delete Account
      ↓
Confirm Action
      ↓
Enter Password
      ↓
Verify Password
      ↓
Delete Account Data
      ↓
Commit
      ↓
Return To Login
```

If a database operation fails, the transaction is rolled back.

This protects against partially completed deletion.

---

# 🖥️ GUI

The application is built with **PyQt6** and uses a `QStackedWidget` to navigate between pages.

## 🔑 Login Page

Features:

- Username input
- Password input
- Show / Hide password
- Login button
- Create Account button
- Exit button

### Screenshot

<p align="center">
  <img src="Docs/Images/GUI/login_page.png" alt="🔑 Login Page screenshot" width="700">

---

## 👤 Create Account Page

Features:

- Username input
- Password input
- Confirm Password input
- Account creation
- Validation messages
- Back button

### Screenshot

<p align="center">
  <img src="Docs/Images/GUI/create_account_page.png" alt="👤 Create Account Page screenshot" width="700">

---

## 🏦 Welcome Page

The Welcome Page acts as the main banking dashboard.

Available operations include:

- Check Balance
- Deposit
- Withdraw
- Transfer
- Transaction History
- Change Password
- Delete Account

### Screenshot

<p align="center">
  <img src="Docs/Images/GUI/welcome_page.png" alt="🏦 Welcome Page screenshot" width="700">


---

## 💰 Balance Page

Displays the current balance of the logged-in account.

### Screenshot

<p align="center">
  <img src="Docs/Images/GUI/balance_page.png" alt="💰 Balance Page screenshot" width="700">
</p>
<img src="Docs/Images/GUI/balance_page.png" alt="Mini Bank System Balance Page" width="700">

---

## 💵 Deposit Page

Allows the logged-in user to enter an amount and deposit money.

### Screenshot

<p align="center">
  <img src="Docs/Images/GUI/deposit_page.png" alt="💵 Deposit Page screenshot" width="700">
</p>


---

## 💸 Withdraw Page

Allows the user to withdraw money after validating the amount and available balance.

### Screenshot

<p align="center">
  <img src="Docs/Images/GUI/withdraw_page.png" alt="💸 Withdraw Page screenshot" width="700">


---

## 🔄 Transfer Page

Allows the logged-in user to transfer money to another account.

### Screenshot

<p align="center">
  <img src="Docs/Images/GUI/transfer_page.png" alt="🔄 Transfer Page screenshot" width="700">

---

## 📜 Transaction History Page

Displays the transactions associated with the logged-in account.

### Screenshot

<p align="center">
  <img src="Docs/Images/GUI/history_page.png" alt="📜 Transaction History Page screenshot" width="700">

---

## 🔐 Change Password Page

Allows the user to securely change the current password.

### Screenshot

<p align="center">
  <img src="Docs/Images/GUI/change_password_page.png" alt="🔐 Change Password Page screenshot" width="700">

---

## 🗑️ Delete Account Page

Provides the account-deletion interface and password verification.

### Screenshot

<p align="center">
  <img src="Docs/Images/GUI/delete_account_page.png" alt="🗑️ Delete Account Page screenshot" width="700">

---

# 🏗️ Application Architecture

The application is intentionally divided into three layers.

```text
                    ┌──────────────┐
                    │     User     │
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

## GUI Layer

Responsible for:

- Displaying information
- Collecting user input
- Handling button clicks
- Showing success/error dialogs
- Page navigation
- Passing user input to Backend services

The GUI does not directly execute SQL.

## Backend Layer

Responsible for:

- Business validation
- Password verification
- Password hashing
- Account operations
- Banking rules
- Calling Database operations
- Returning success/failure results to the GUI

Examples:

```python
generate_account_number()
get_account_balance()
deposit_money()
withdraw_money()
transfer_money()
get_transaction_history()
delete_account()
change_password()
```

## Database Layer

Responsible for:

- Creating tables
- Reading data
- Inserting data
- Updating data
- Deleting data
- Database transactions
- Recording transaction history

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

---

# 📂 Project Structure

The application source is organized into separate responsibilities:

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
├── Docs/
│   └── Images/
│       ├── GUI/
│       │   ├── login_page.png
│       │   ├── create_account_page.png
│       │   ├── welcome_page.png
│       │   ├── balance_page.png
│       │   ├── deposit_page.png
│       │   ├── withdraw_page.png
│       │   ├── transfer_page.png
│       │   ├── history_page.png
│       │   ├── change_password_page.png
│       │   └── delete_account_page.png
│       │
│       └── Code/
│           ├── account_sevices/
│           │   ├── image_1.png
│           │   ├── image_2.png
│           │   ├── image_3.png
│           │   └── image_4.png
│           │
│           ├── auth_service/
│           │   ├── image_1.png
│           │   ├── image_2.png
│           │   └── image_3.png
│           │
│           ├── database/
│           │   ├── image_1.png
│           │   ├── image_2.png
│           │   ├── image_3.png
│           │   ├── image_4.png
│           │   ├── image_5.png
│           │   ├── image_6.png
│           │   ├── image_7.png
│           │   ├── image_8.png
│           │   ├── image_9.png
│           │   └── image_10.png
│           │
│           ├── validators.png
│           └── security.png
│
├── requirements.txt
├── .gitignore
└── README.md
```

> **Note:** The folder name `account_sevices` is intentionally kept exactly as specified for the current project structure.

---

# 🗄️ Database Design

The application uses SQLite.

Database file:

```text
Database/xyz_bank.db
```

## `users` Table

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

## `transactions` Table

```text
transactions
├── id
├── account_number
├── transaction_type
├── amount
├── balance_after
└── transaction_time
```

The transaction history is linked to an account through `account_number`.

---

# 🔄 Database Transactions

The transfer operation uses explicit transaction handling:

```text
BEGIN
  ↓
Update Sender
  ↓
Update Receiver
  ↓
Add Sender Transaction
  ↓
Add Receiver Transaction
  ↓
COMMIT
```

If an exception or failure occurs:

```text
ROLLBACK
```

This is important because a transfer contains multiple changes that should be treated as one logical operation.

---

# 🔐 Security Architecture

Password lifecycle:

```text
User Password
      │
      ▼
hash_password()
      │
      ▼
bcrypt Hash
      │
      ▼
SQLite
```

Login/password verification:

```text
Entered Password
      │
      ▼
verify_password()
      │
      ▼
Stored bcrypt Hash
      │
      ▼
True / False
```

The application does not decrypt bcrypt hashes.

---

# 🧪 Testing Strategy

The project uses:

- `pytest`
- `pytest-qt`
- `unittest.mock`
- `pytest-cov`

Tests are divided by layer.

```text
                    Tests
                      │
          ┌───────────┼───────────┐
          │           │           │
          ▼           ▼           ▼
      Database     Backend       GUI
       Tests        Tests       Tests
```

## Backend Tests

Backend tests isolate the business logic by mocking the database.

Example style:

```python
@patch("Backend.account_service.sqlitedb")
def test_transfer_money_database_failure(mock_db):
    mock_db.get_balance.side_effect = [1000, 500]
    mock_db.transfer_money.return_value = False

    success, message = transfer_money("1001", "1002", "300")

    assert success is False
    assert message == "Transfer failed."
```

This means:

```text
Test
 ↓
Backend
 ↓
Mock Database
```

The real SQLite database is not required for these tests.

## Database Tests

Database tests use the `test_db` fixture and execute real SQLite operations.

Example style:

```python
def test_reset_login_attempts(test_db):
    test_db.create_user("1234567", "prashant", "password123")

    test_db.update_failed_attempts("prashant", 3)
    test_db.lock_user("prashant", "2099-01-01T00:00:00")

    test_db.reset_login_attempts("prashant")

    attempts = test_db.get_failed_attempts("prashant")
    locked_until = test_db.get_locked_until("prashant")

    assert attempts == 0
    assert locked_until is None
```

## GUI Tests

GUI tests use `pytest-qt` and mock the Backend.

Example style:

```python
@patch("GUI.transfer_page.transfer_money")
def test_transfer_button_click(mock_transfer, qtbot):
    page = TransferPage(None)
    qtbot.addWidget(page)

    page.account_number = "1001"
    page.receiver_input.setText("1002")
    page.amount_input.setText("300")

    mock_transfer.return_value = (True, "Success")

    page.transfer_btn.click()

    mock_transfer.assert_called_once()
```

The GUI test therefore focuses on GUI behavior rather than database behavior.

---

# 🎭 Mocking Strategy

The project intentionally tests each layer in isolation.

### Backend

```text
Test
 ↓
Backend
 ↓
Mock Database
```

### GUI

```text
Test
 ↓
GUI
 ↓
Mock Backend
```

### Database

```text
Test
 ↓
Real Test Database
 ↓
SQLite
```

Benefits:

- Faster tests
- Isolated failures
- Predictable behavior
- Easier debugging
- No unnecessary dependency between layers

---

# 📊 Test Coverage

Coverage is measured with `pytest-cov`.

Run:

```bash
pytest --cov=Backend --cov=Database --cov-report=term-missing
```

Coverage was actively used during development to identify untested branches.

For example, missing coverage was investigated for:

- Password validation branches
- Account-not-found branches
- Database failure branches
- Transfer failure branches
- Delete-account failure branches
- GUI error paths

The goal is not simply to display a high percentage. Coverage is used to discover which logical paths still need tests.

---

# 📸 Code Implementation Screenshots

The following screenshots document important parts of the implementation.

## Backend — `account_service.py`

The Account Service contains banking business logic such as:

- Account number generation
- Balance retrieval
- Deposit
- Withdrawal
- Transfer
- Transaction history
- Account deletion
- Password change

There are **4 screenshots** for this file.

### Account Service — Image 1

<p align="center">
  <img src="Docs/Images/Code/account_service/image_1.png" alt="Account Service — Image 1 code screenshot" width="850">

### Account Service — Image 2

<p align="center">
  <img src="Docs/Images/Code/account_service/image_2.png" alt="Account Service — Image 2 code screenshot" width="850">

### Account Service — Image 3

<p align="center">
  <img src="Docs/Images/Code/account_service/image_3.png" alt="Account Service — Image 3 code screenshot" width="850">

### Account Service — Image 4

<p align="center">
  <img src="Docs/Images/Code/account_service/image_4.png" alt="Account Service — Image 4 code screenshot" width="850">

---

## Backend — `auth_service.py`

The Authentication Service handles authentication-related business logic.

There are **3 screenshots** for this file.

### Authentication Service — Image 1

<p align="center">
  <img src="Docs/Images/Code/auth_service/image_1.png" alt="Authentication Service — Image 1 code screenshot" width="850">

### Authentication Service — Image 2

<p align="center">
  <img src="Docs/Images/Code/auth_service/image_2.png" alt="Authentication Service — Image 2 code screenshot" width="850">

### Authentication Service — Image 3

<p align="center">
  <img src="Docs/Images/Code/auth_service/image_3.png" alt="Authentication Service — Image 3 code screenshot" width="850">

---

## Database — `sqlitedb.py`

The Database layer contains SQLite operations for:

- User creation
- User lookup
- Password lookup
- Balance operations
- Deposits
- Withdrawals
- Transfers
- Transaction recording
- Transaction retrieval
- Password updates
- Account deletion
- Login-attempt handling

There are **10 screenshots** for the Database implementation.

### Database — Image 1

<p align="center">
  <img src="Docs/Images/Code/database/image_1.png" alt="Database — Image 1 code screenshot" width="850">

### Database — Image 2

<p align="center">
  <img src="Docs/Images/Code/database/image_2.png" alt="Database — Image 2 code screenshot" width="850">

### Database — Image 3

<p align="center">
  <img src="Docs/Images/Code/database/image_3.png" alt="Database — Image 3 code screenshot" width="850">

### Database — Image 4

<p align="center">
  <img src="Docs/Images/Code/database/image_4.png" alt="Database — Image 4 code screenshot" width="850">

### Database — Image 5

<p align="center">
  <img src="Docs/Images/Code/database/image_5.png" alt="Database — Image 5 code screenshot" width="850">

### Database — Image 6

<p align="center">
  <img src="Docs/Images/Code/database/image_6.png" alt="Database — Image 6 code screenshot" width="850">

### Database — Image 7

<p align="center">
  <img src="Docs/Images/Code/database/image_7.png" alt="Database — Image 7 code screenshot" width="850">

### Database — Image 8

<p align="center">
  <img src="Docs/Images/Code/database/image_8.png" alt="Database — Image 8 code screenshot" width="850">

### Database — Image 9

<p align="center">
  <img src="Docs/Images/Code/database/image_9.png" alt="Database — Image 9 code screenshot" width="850">

### Database — Image 10

<p align="center">
  <img src="Docs/Images/Code/database/image_10.png" alt="Database — Image 10 code screenshot" width="850">

---

## Validators

<p align="center">
  <img src="Docs/Images/Code/validators.png" alt="Validators code" width="850">
</p>

The validation layer contains reusable validation rules used by the application.

---

## Security

<p align="center">
  <img src="Docs/Images/Code/security.png" alt="Security code" width="850">
</p>

The security module contains password hashing and password verification functionality.



# ⚙️ Installation

## Clone Repository

```bash
git clone https://github.com/namansinghpatel/Python_Progs/tree/main/Python_Codes/Mini_Bank_System
```

> If the repository is later moved to a dedicated GitHub repository, update the URL accordingly.

## Navigate to the Project

```bash
cd Mini_Bank_System
```

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

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Application

```bash
python main.py
```

---

# 🧪 Running Tests

Run all tests:

```bash
pytest
```

Verbose:

```bash
pytest -v
```

Backend tests:

```bash
pytest Tests/test_Backend/
```

GUI tests:

```bash
pytest Tests/test_GUI/
```

Database tests:

```bash
pytest Tests/sqlitedb_test.py
```

Coverage:

```bash
pytest --cov=Backend --cov=Database --cov-report=term-missing
```

---

# 🔄 Application Flows

## Create Account

```text
Create Account
      ↓
Validate Username
      ↓
Validate Password
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

## Login

```text
Login
  ↓
Validate Input
  ↓
Check Account Lock
  ↓
Fetch Stored Password Hash
  ↓
Verify Password
  ↓
Reset Login Attempts
  ↓
Welcome Page
```

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

Failure:

```text
ROLLBACK
```

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
Update Database
      ↓
Success
      ↓
Return To Login
```

## Delete Account

```text
Delete Account
      ↓
Confirm Action
      ↓
Verify Password
      ↓
Delete Account Data
      ↓
Commit
      ↓
Return To Login
```

---

# 🧠 Software Engineering Concepts Learned

## Python

- Classes
- Objects
- Methods
- `self`
- Functions
- Imports
- Modules
- Packages
- Tuples
- Exception handling
- Return values

## GUI Development

- PyQt6
- `QWidget`
- `QLabel`
- `QPushButton`
- `QLineEdit`
- Layouts
- Signals and slots
- `QStackedWidget`
- `QMessageBox`
- GUI state management

## Backend

- Service-layer architecture
- Business validation
- Separation of concerns
- Error handling
- GUI/backend separation
- Consistent success/failure return values

## Database

- SQLite
- SQL queries
- Parameterized queries
- `SELECT`
- `INSERT`
- `UPDATE`
- `DELETE`
- `COMMIT`
- `ROLLBACK`
- Database transactions
- Transaction history

## Security

- bcrypt
- Password hashing
- Password verification
- Secure password storage
- Re-authentication
- Password change
- Account deletion protection
- Account locking

## Testing

- pytest
- pytest-qt
- Fixtures
- Assertions
- `@patch`
- `MagicMock`
- GUI testing
- Backend testing
- Database testing
- Test isolation
- Coverage analysis

---

# 🔁 Development Workflow

Each feature was developed incrementally:

```text
Requirement
    ↓
Understand the Flow
    ↓
Database Implementation
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
Run Test Suite
    ↓
Coverage Analysis
    ↓
Fix Failures
    ↓
Repeat
```

This project therefore focuses not only on writing code, but also on:

- Understanding the reason behind each layer
- Debugging test failures
- Improving test coverage
- Separating responsibilities
- Handling database failures
- Using mocks correctly
- Testing GUI behavior independently

---

# 🛣️ Future Roadmap

## Banking

- [ ] Profile / Account Dashboard
- [ ] Mini Statement
- [ ] Transaction Search and Filtering
- [ ] Export Bank Statement
- [ ] Interest Calculator
- [ ] Loan Calculator

## Security

- [ ] Forgot Password
- [ ] OTP Verification
- [ ] Session Management
- [ ] Role-Based Access Control
- [ ] Admin Authentication
- [ ] Audit Logs
- [ ] Stronger Password Policies
- [ ] Additional protection for sensitive operations

## Administration

- [ ] Admin Dashboard
- [ ] View All Accounts
- [ ] Search Accounts
- [ ] Lock / Unlock Accounts
- [ ] Account Management
- [ ] Bank-wide Statistics

## Testing

- [ ] Expand GUI navigation coverage
- [ ] End-to-End tests
- [ ] Integration tests
- [ ] Performance tests
- [ ] Security tests
- [ ] Maintain high test coverage

---

# 🎯 Project Learning Goal

The project is being developed as a progressive learning exercise rather than as a single large code dump.

The central development loop is:

```text
Learn
  ↓
Design
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

The objective is to understand how a software project evolves from basic functionality into a structured, tested application.

---

# ⚠️ Disclaimer

This is a **learning project**.

It is not intended to handle real financial accounts, real money, or production banking data.

A real banking system would require substantially stronger security, encryption, compliance, auditing, authorization, infrastructure, monitoring, reliability, disaster recovery, and regulatory controls.

---

# 👨‍💻 Author

**Naman Singh Patel**

Built as a learning project to understand:

- Python application development
- PyQt6 GUI development
- SQLite database design
- Authentication and security
- Backend architecture
- Automated testing
- Mocking
- Software engineering practices

---

# ⭐ Project Goal

The long-term goal is to continue evolving this Mini Bank System while learning professional software development practices.

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

## 📁 Documentation Folder

The complete documentation image structure used by this README is:

```text
Docs/
└── Images/
    │
    ├── GUI/
    │   ├── login_page.png
    │   ├── create_account_page.png
    │   ├── welcome_page.png
    │   ├── balance_page.png
    │   ├── deposit_page.png
    │   ├── withdraw_page.png
    │   ├── transfer_page.png
    │   ├── history_page.png
    │   ├── change_password_page.png
    │   └── delete_account_page.png
    │
    └── Code/
        ├── account_sevices/
        │   ├── image_1.png
        │   ├── image_2.png
        │   ├── image_3.png
        │   └── image_4.png
        │
        ├── auth_service/
        │   ├── image_1.png
        │   ├── image_2.png
        │   └── image_3.png
        │
        ├── database/
        │   ├── image_1.png
        │   ├── image_2.png
        │   ├── image_3.png
        │   ├── image_4.png
        │   ├── image_5.png
        │   ├── image_6.png
        │   ├── image_7.png
        │   ├── image_8.png
        │   ├── image_9.png
        │   └── image_10.png
        │
        ├── validators.png
        └── security.png
```

> The screenshot files themselves are not included in this generated package because they were not uploaded in this conversation. Place your existing screenshots at the exact paths above and the README links will work on GitHub.
