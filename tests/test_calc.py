from .calculation import add,sub,mul,div,BankAccount
import pytest

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1,num2,result",[(3,2,5),(1,2,3),(5,2,7),(10,2,12)])
def test_add(num1,num2,result):
    assert add(num1,num2) == result


def test_sub():
    assert sub(1,2) == -1

def test_mul():
    assert mul(1,2) == 2

def test_div():
    assert div(1,2) == 0.5


def test_balance_zero(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_balance_regular(bank_account):
    assert bank_account.balance == 50

def test_deposit(bank_account):
    bank_account.deposit(50)
    assert bank_account.balance == 100

def test_withdraw(bank_account):
    bank_account.withdraw(50)
    assert bank_account.balance == 0

def test_interest(bank_account):
    bank_account.interest()
    assert round(bank_account.balance,2) == 55


@pytest.mark.parametrize("deposited,withdrawn,expected",[(200,100,100),(150,100,50)])
def test_transaction(zero_bank_account,deposited,withdrawn,expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawn)
    assert zero_bank_account.balance == expected

def test_insufficient_funds(bank_account):
    with pytest.raises(ValueError):
        bank_account.withdraw(100)

def test_div_zero():
    with pytest.raises(ZeroDivisionError):
        div(1,0)