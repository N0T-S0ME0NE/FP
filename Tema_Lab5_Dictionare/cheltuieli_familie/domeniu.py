CATEGORIES=('mâncare','întreținere','îmbrăcăminte','telefon','altele')
MIN_DAY=1
MAX_DAY=31
MAX_AMOUNT=1000000000

# Validări

def validate_day(day):
    if not isinstance(day,int) or isinstance(day,bool):
        raise ValueError("Ziua trebuie să fie un număr întreg între 1 și 31")
    if day<MIN_DAY or day>MAX_DAY:
        raise ValueError("Ziua trebuie să fie un număr întreg între 1 și 31")

def validate_amount(amount):
    if not isinstance(amount,(int,float)) or isinstance(amount,bool):
        raise ValueError("Suma trebuie să fie între 0.01 și 1000000000")
    if amount<0.01 or amount>MAX_AMOUNT:
        raise ValueError("Suma trebuie să fie între 0.01 și 1000000000")

def validate_limit(limit):
    if not isinstance(limit,(int,float)) or isinstance(limit,bool):
        raise ValueError("Limita trebuie să fie între 0 și 1000000000")
    if limit<0 or limit>MAX_AMOUNT:
        raise ValueError("Limita trebuie să fie între 0 și 1000000000")

def validate_type(expense_type):
    if expense_type not in CATEGORIES:
        raise ValueError("Tip invalid. Tipuri permise: " + ", ".join(CATEGORIES))

# Crearea și citirea unei cheltuieli

def create_expense(day,amount,expense_type):
    validate_day(day)
    validate_amount(amount)
    validate_type(expense_type)
    return {"ziua":day,"suma":round(amount,2),"tip":expense_type}

def get_day(expense):
    return expense["ziua"]

def get_amount(expense):
    return expense["suma"]

def get_type(expense):
    return expense["tip"]