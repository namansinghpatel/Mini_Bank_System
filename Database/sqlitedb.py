import sqlite3
from Backend.security import verify_password
from datetime import datetime


class SQLiteDB:

    def __init__(self, db_path="Database/xyz_bank.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number TEXT UNIQUE NOT NULL,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                balance REAL DEFAULT 0.0,
                failed_attempts INTEGER DEFAULT 0,
                locked_until TEXT)""")

        self.cursor.execute("""CREATE TABLE IF NOT EXISTS transactions
               (id INTEGER PRIMARY KEY AUTOINCREMENT,
                account_number TEXT NOT NULL,
                transaction_type TEXT NOT NULL,
                amount REAL NOT NULL,
                balance_after REAL NOT NULL,
                transaction_time TEXT NOT NULL)""")
        self.conn.commit()

    def user_exists(self, username):
        self.cursor.execute(
            """
            SELECT username
            FROM users
            WHERE username = ?
            """,
            (username,),
        )
        return self.cursor.fetchone() is not None

    def create_user(self, account_number, username, password):
        self.cursor.execute(
            """
        INSERT INTO users
        (
            account_number,
            username,
            password
        )
        VALUES (?, ?, ?)
        """,
            (account_number, username, password),
        )
        self.conn.commit()
        return True

    def authenticate_user(self, username, password):
        stored_hash = self.get_user_password_hash(username)
        if stored_hash is None:
            return (False, "Invalid Username or Password")
        if not verify_password(password, stored_hash):
            return (False, "Invalid Username or Password")
        return (True, "Login Successful")

    def get_user_password_hash(self, username):

        self.cursor.execute(
            """
            SELECT password
            FROM users
            WHERE username = ?
            """,
            (username,),
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def get_failed_attempts(self, username):
        self.cursor.execute(
            """
            SELECT failed_attempts
            FROM users
            WHERE username = ?
            """,
            (username,),
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return 0

    def get_locked_until(self, username):
        self.cursor.execute(
            """
            SELECT locked_until
            FROM users
            WHERE username = ?
            """,
            (username,),
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def update_failed_attempts(self, username, attempts):
        self.cursor.execute(
            """
            UPDATE users
            SET failed_attempts = ?
            WHERE username = ?
            """,
            (attempts, username),
        )
        self.conn.commit()

    def lock_user(self, username, lock_until):
        self.cursor.execute(
            """
            UPDATE users
            SET locked_until = ?
            WHERE username = ?
            """,
            (lock_until, username),
        )
        self.conn.commit()

    def reset_login_attempts(self, username):
        self.cursor.execute(
            """
            UPDATE users
            SET failed_attempts = 0,
                locked_until = NULL
            WHERE username = ?
            """,
            (username,),
        )
        self.conn.commit()

    def account_number_exists(self, account_number):
        self.cursor.execute(
            """
            SELECT account_number
            FROM users
            WHERE account_number = ?
            """,
            (account_number,),
        )
        return self.cursor.fetchone() is not None

    def get_account_number(self, username):
        self.cursor.execute(
            """
            SELECT account_number
            FROM users
            WHERE username = ?
            """,
            (username,),
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def get_balance(self, account_number):
        self.cursor.execute(
            """
            SELECT balance
            FROM users
            WHERE account_number = ?
            """,
            (account_number,),
        )
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

    def deposit_money(self, account_number, amount):
        self.cursor.execute(
            """
            UPDATE users
            SET balance = balance + ?
            WHERE account_number = ?
            """,
            (amount, account_number),
        )
        if self.cursor.rowcount > 0:
            balance = self.get_balance(account_number)
            self.add_transaction(account_number, "Deposit", amount, balance)
            self.conn.commit()
            return True
        return False

    def withdraw_money(self, account_number, amount):
        self.cursor.execute(
            """
            UPDATE users
            SET balance = balance - ?
            WHERE account_number = ?
            """,
            (amount, account_number),
        )
        if self.cursor.rowcount > 0:
            balance = self.get_balance(account_number)
            self.add_transaction(account_number, "Withdraw", amount, balance)
            self.conn.commit()
            return True
        return False

    def transfer_money(self, sender_account, receiver_account, amount):
        try:
            self.conn.execute("BEGIN")
            self.cursor.execute(
                """
                UPDATE users
                SET balance = balance - ?
                WHERE account_number = ?
                """,
                (amount, sender_account),)

            if self.cursor.rowcount == 0:
                raise Exception("Sender account not found.")
            self.cursor.execute(
                """
                UPDATE users
                SET balance = balance + ?
                WHERE account_number = ?
                """,
                (amount, receiver_account),)
            if self.cursor.rowcount == 0:
                raise Exception("Receiver account not found.")
            # Get updated balances
            sender_balance = self.get_balance(sender_account)
            receiver_balance = self.get_balance(receiver_account)
            # Record sender history
            self.add_transaction(sender_account, "Transfer Out", amount, sender_balance)
            # Record receiver history
            self.add_transaction(receiver_account, "Transfer In", amount, receiver_balance)
            self.conn.commit()
            return True
        except Exception:
            self.conn.rollback()
            return False

    def add_transaction(self, account_number, transaction_type, amount, balance_after):
        transaction_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.cursor.execute(
            """
            INSERT INTO transactions
               (account_number,
                transaction_type,
                amount,
                balance_after,
                transaction_time)
            VALUES (?, ?, ?, ?, ?)
            """,
            (account_number, transaction_type, amount, balance_after, transaction_time))

    def get_transactions(self, account_number):
        self.cursor.execute(
            """
            SELECT
                transaction_type,
                amount,
                balance_after,
                transaction_time
            FROM transactions
            WHERE account_number = ?
            ORDER BY id DESC
            """,
            (account_number,),)
        return self.cursor.fetchall()

    def delete_account(self, account_number):
        try:
            self.conn.execute("BEGIN")
            self.cursor.execute(
                """
                DELETE FROM transactions
                WHERE account_number = ?
                """,
                (account_number,),)
            self.cursor.execute(
                """
                DELETE FROM users
                WHERE account_number = ?
                """,
                (account_number,),)
            if self.cursor.rowcount == 0:
                self.conn.rollback()
                return False
            self.conn.commit()
            return True
        except Exception:
            self.conn.rollback()
            return False

    def get_user_password_hash_by_account(self, account_number):
        self.cursor.execute(
            """
            SELECT password
            FROM users
            WHERE account_number = ?
            """,
            (account_number,),)
        result = self.cursor.fetchone()
        if result:
            return result[0]
        return None

sqlitedb = SQLiteDB()
