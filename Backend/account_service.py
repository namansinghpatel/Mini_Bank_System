import random
from Database.sqlitedb import sqlitedb


def generate_account_number():
    while True:
        account_number = str(random.randint(1000000, 9999999))
        if not sqlitedb.account_number_exists(account_number):
            return account_number


def get_account_balance(account_number):
    balance = sqlitedb.get_balance(account_number)
    if balance is None:
        return (False, "Account not found")
    return (True, balance)


def deposit_money(account_number, amount):
    # -------------------------
    # Validate Amount
    # -------------------------
    try:
        amount = float(amount)
    except ValueError:
        return (False, "Please enter a valid amount.")
    if amount <= 0:
        return (False, "Amount must be greater than zero.")
    # -------------------------
    # Deposit
    # -------------------------

    success = sqlitedb.deposit_money(account_number, amount)
    if not success:
        return (False, "Account not found.")
    return (True, f"₹{amount:.2f} deposited successfully.")


def withdraw_money(account_number, amount):

    try:
        amount = float(amount)
    except ValueError:
        return (False, "Please enter a valid amount.")
    if amount <= 0:
        return (False, "Amount must be greater than zero.")
    # ---------------------------------
    # Get Current Balance
    # ---------------------------------
    current_balance = sqlitedb.get_balance(account_number)
    if current_balance is None:
        return (False, "Account not found.")
    # ---------------------------------
    # Check Sufficient Balance
    # ---------------------------------
    if amount > current_balance:
        return (False, "Insufficient balance.")
    # ---------------------------------
    # Withdraw Money
    # ---------------------------------
    success = sqlitedb.withdraw_money(account_number, amount)
    if not success:
        return (False, "Withdrawal failed.")
    return (True, f"₹{amount:.2f} withdrawn successfully.")


def transfer_money(sender_account, receiver_account, amount):
    sender_balance = sqlitedb.get_balance(sender_account)
    receiver_balance = sqlitedb.get_balance(receiver_account)
    try:
        amount = float(amount)
    except ValueError:
        return False, "Please enter a valid amount."
    if amount <= 0:
        return False, "Amount must be greater than zero."
    if sender_balance is None:
        return False, "Sender account not found."
    if receiver_balance is None:
        return False, "Receiver account not found."
    if sender_account == receiver_account:
        return False, "Cannot transfer to the same account."
    if amount > sender_balance:
        return False, "Insufficient balance."
    
    success = sqlitedb.transfer_money(sender_account, receiver_account, amount)
    if success:
        return (True, f"₹{amount:.2f} transferred successfully.")
    return False, "Transfer failed."
