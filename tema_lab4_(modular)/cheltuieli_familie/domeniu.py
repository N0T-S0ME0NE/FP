CATEGORIES=['mâncare','întreținere','îmbrăcăminte','telefon','altele']
MIN_DAY=1
MAX_DAY=31
MAX_AMOUNT=1000000000

def validate_day(day):
    if not isinstance(day,int):
        raise ValueError("Ziua trebuie să fie un număr întreg")
    if day<MIN_DAY or day>MAX_DAY:
        raise ValueError("Ziua trebuie să fie între 1 și 31")

def validate_amount(amount):
    if not isinstance(amount,(int,float)):
        raise ValueError("Suma trebuie să fie un număr")
    if not (0.01<=amount<=MAX_AMOUNT):
        raise ValueError("Suma trebuie să fie între 0.01 și 1000000000")

def validate_limit(limit):
    if not isinstance(limit,(int,float)):
        raise ValueError("Suma trebuie să fie un număr")
    if not (0<=limit<=MAX_AMOUNT):
        raise ValueError("Suma trebuie să fie între 0 și 1000000000")

def validate_type(expense_type):
    if expense_type not in CATEGORIES:
        raise ValueError("Tip invalid. Tipuri permise: " + ", ".join(CATEGORIES))

def create_expense(day,amount,expense_type):
    validate_day(day)
    validate_amount(amount)
    validate_type(expense_type)
    return {'day': day, 'amount': round(amount, 2), 'type': expense_type}

def get_day(expense):
    return expense['day']

def get_amount(expense):
    return expense['amount']

def get_type(expense):
    return expense['type']