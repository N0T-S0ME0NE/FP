from .domeniu import (CATEGORIES,MIN_DAY,MAX_DAY,validate_day,validate_limit,validate_type,create_expense,get_day,get_amount,get_type)

# Cheltuieli exemple
SAMPLE_DATA=(
    (3,120.50,'mâncare'),
    (5,300,'întreținere'),
    (5,45,'mâncare'),
    (10,80,'telefon'),
    (12,250,'îmbrăcăminte'),
    (12,30,'altele'),
    (20,45,'telefon'),
    (25,500,'întreținere'),
)

# Adăugare/Actualizare

def add_expense(expenses,history,day,amount,expense_type):
    expense=create_expense(day,amount,expense_type)
    save_state(expenses,history)
    expenses.append(expense)
    return expense

def update_expense(expenses,history,day,amount,expense_type):
    new_expense=create_expense(day,amount,expense_type)
    for i in range(len(expenses)):
        if get_day(expenses[i])==day and get_type(expenses[i])==expense_type:
            save_state(expenses,history)
            expenses[i]=new_expense
            return new_expense
    raise ValueError("Nu există nicio cheltuială în ziua " + str(day) + " de tipul '" + expense_type + "'")

def load_sample_data(expenses,history):
    save_state(expenses,history)
    for day,amount,expense_type in SAMPLE_DATA:
        expenses.append(create_expense(day,amount,expense_type))
    return len(SAMPLE_DATA)

# Ștergere

def _replace_if_changed(expenses,history,kept):
    removed=len(expenses)-len(kept)
    if removed>0:
        save_state(expenses,history)
        expenses[:]=kept
    return removed

def remove_by_day(expenses,history,day):
    validate_day(day)
    kept=[]
    for expense in expenses:
        if get_day(expense)!=day:
            kept.append(expense)
    return _replace_if_changed(expenses,history,kept)

def remove_by_interval(expenses,history,start_day,end_day):
    validate_day(start_day)
    validate_day(end_day)
    if start_day>end_day:
        raise ValueError("Ziua de început nu poate fi după ziua de sfârșit")
    kept=[]
    for expense in expenses:
        if get_day(expense)<start_day or get_day(expense)>end_day:
            kept.append(expense)
    return _replace_if_changed(expenses,history,kept)

def remove_by_type(expenses,history,expense_type):
    kept=filter_out_type(expenses,expense_type)
    return _replace_if_changed(expenses,history,kept)

# Căutări

def find_greater_than(expenses,amount):
    validate_limit(amount)
    result=[]
    for expense in expenses:
        if get_amount(expense)>amount:
            result.append(expense)
    return result

def find_before_day_less_than(expenses,day,amount):
    validate_day(day)
    validate_limit(amount)
    result=[]
    for expense in expenses:
        if get_day(expense)<day and get_amount(expense)<amount:
            result.append(expense)
    return result

def find_by_type(expenses,expense_type):
    validate_type(expense_type)
    result=[]
    for expense in expenses:
        if get_type(expense)==expense_type:
            result.append(expense)
    return result

def find_by_amount(expenses, amount):
    validate_limit(amount)
    result=[]
    for expense in expenses:
        if get_amount(expense)==round(amount,2):
            result.append(expense)
    return result

# Rapoarte

def total_for_type(expenses,expense_type):
    total=0
    for expense in find_by_type(expenses,expense_type):
        total+=get_amount(expense)
    return round(total,2)

def day_with_max_total(expenses):
    best_day=None
    best_total=0
    for day in range(MIN_DAY,MAX_DAY+1):
        total=0
        for expense in expenses:
            if get_day(expense)==day:
                total+=get_amount(expense)
        total=round(total,2)
        if total>best_total:
            best_day=day
            best_total=total
    if best_day is None:
        return None
    return (best_day,best_total)

def sort_by_type(expenses):
    result=[]
    for category in CATEGORIES:
        for expense in expenses:
            if get_type(expense)==category:
                result.append(expense)
    return result

# Filtrare

def filter_out_type(expenses,expense_type):
    validate_type(expense_type)
    result=[]
    for expense in expenses:
        if get_type(expense)!=expense_type:
            result.append(expense)
    return result

def filter_out_less_than(expenses,amount):
    validate_limit(amount)
    result=[]
    for expense in expenses:
        if get_amount(expense)>=amount:
            result.append(expense)
    return result

# Undo

def copy_expenses(expenses):
    copy=[]
    for expense in expenses:
        copy.append(expense[:])
    return copy

def save_state(expenses,history):
    history.append(copy_expenses(expenses))

def undo(expenses,history):
    if len(history)==0:
        raise ValueError("Nu există nicio operație de refăcut")
    expenses[:]=history.pop()