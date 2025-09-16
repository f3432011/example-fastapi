import pytest
from app.calculations import add, sub, mul, div, BankAccount, InsufficientFunds


@pytest.fixture
def zero_bank_account():
    print("Creating empty bank account")
    return BankAccount()


@pytest.fixture
def bank_account():
    print("Creating bank account with 50 balance")
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", [(5, 3, 8), (10, 5, 15), (0, 0, 0)])
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected


def test_subtract():
    print("testing subtract function")
    assert sub(5, 3) == 2


def test_multiply():
    print("testing multiply function")
    assert mul(5, 3) == 15


def test_divide():
    print("testing divide function")
    assert div(5, 0) == "Cannot divide by zero"
    assert div(6, 3) == 2


def test_bank_set_initial_amount(bank_account):
    print("testing bank account class")

    assert bank_account.balance == 50


def test_bank_default_amount(zero_bank_account):
    print("testing bank account class")

    assert zero_bank_account.balance == 0


def test_withdraw(bank_account):
    print("testing withdraw method")
    bank_account.withdraw(40)
    assert bank_account.balance == 10


def test_deposit(bank_account):
    print("testing deposit method")
    bank_account.deposit(40)
    assert bank_account.balance == 90


def test_collect_interest(bank_account):
    print("testing collect interest method")
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55.0


@pytest.mark.parametrize(
    "deposited, withdrew, expected",
    [(200, 100, 100), (50, 10, 40), (1200, 200, 1000)],
)
def test_bank_transaction(zero_bank_account, deposited, withdrew, expected):
    print("testing multiple transactions")
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds) as excinfo:
        bank_account.withdraw(200)
    assert str(excinfo.value) == "Insufficient funds in account"
