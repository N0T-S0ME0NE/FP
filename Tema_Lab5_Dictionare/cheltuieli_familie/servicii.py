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

def next_id(expenses):
    if len(expenses)==0:
        return 1
    return max(expenses)+1

def add_expense(expenses,day,amount,expense_type):
    expense=create_expense(day,amount,expense_type)
    expenses[next_id(expenses)]=expense
    return expense

def update_expense(expenses,day,amount,expense_type):
    new_expense=create_expense(day,amount,expense_type)
    for expense_id in expenses:
        if get_day(expenses[expense_id])==day and get_type(expenses[expense_id])==expense_type:
            expenses[expense_id]=new_expense
            return new_expense
    raise ValueError("Nu există nicio cheltuială în ziua " + str(day) + " de tipul '" + expense_type + "'")

def load_sample_data(expenses):
    for day,amount,expense_type in SAMPLE_DATA:
        expenses[next_id(expenses)]=create_expense(day,amount,expense_type)
    return len(SAMPLE_DATA)

# Ștergere

def _replace_if_changed(expenses,kept):
    removed=len(expenses)-len(kept)
    if removed>0:
        expenses.clear()
        expenses.update(kept)
    return removed

def remove_by_day(expenses,day):
    validate_day(day)
    kept={}
    for expense_id in expenses:
        expense=expenses[expense_id]
        if get_day(expense)!=day:
            kept[expense_id]=expense
    return _replace_if_changed(expenses,kept)

def remove_by_interval(expenses,start_day,end_day):
    validate_day(start_day)
    validate_day(end_day)
    if start_day>end_day:
        raise ValueError("Ziua de început nu poate fi după ziua de sfârșit")
    kept={}
    for expense_id in expenses:
        expense=expenses[expense_id]
        if get_day(expense)<start_day or get_day(expense)>end_day:
            kept[expense_id]=expense
    return _replace_if_changed(expenses,kept)

def remove_by_type(expenses,expense_type):
    kept=filter_out_type(expenses,expense_type)
    return _replace_if_changed(expenses,kept)

# Căutări

def find_greater_than(expenses,amount):
    validate_limit(amount)
    result={}
    for expense_id in expenses:
        expense=expenses[expense_id]
        if get_amount(expense)>amount:
            result[expense_id]=expense
    return result

def find_before_day_less_than(expenses,day,amount):
    validate_day(day)
    validate_limit(amount)
    result={}
    for expense_id in expenses:
        expense=expenses[expense_id]
        if get_day(expense)<day and get_amount(expense)<amount:
            result[expense_id]=expense
    return result

def find_by_type(expenses,expense_type):
    validate_type(expense_type)
    result={}
    for expense_id in expenses:
        expense=expenses[expense_id]
        if get_type(expense)==expense_type:
            result[expense_id]=expense
    return result

def find_by_amount(expenses,amount):
    validate_limit(amount)
    result={}
    for expense_id in expenses:
        expense=expenses[expense_id]
        if get_amount(expense)==round(amount,2):
            result[expense_id]=expense
    return result

# Rapoarte

def total_for_type(expenses,expense_type):
    total=0
    for expense in find_by_type(expenses,expense_type).values():
        total+=get_amount(expense)
    return round(total,2)

def day_with_max_total(expenses):
    best_day=None
    best_total=0
    for day in range(MIN_DAY,MAX_DAY+1):
        total=0
        for expense in expenses.values():
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
    result={}
    result_id=1
    for category in CATEGORIES:
        for expense_id in expenses:
            expense=expenses[expense_id]
            if get_type(expense)==category:
                result[result_id]=expense
                result_id+=1
    return result

# Filtrare

def filter_out_type(expenses,expense_type):
    validate_type(expense_type)
    result={}
    for expense_id in expenses:
        expense=expenses[expense_id]
        if get_type(expense)!=expense_type:
            result[expense_id]=expense
    return result

def filter_out_less_than(expenses,amount):
    validate_limit(amount)
    result={}
    for expense_id in expenses:
        expense=expenses[expense_id]
        if get_amount(expense)>=amount:
            result[expense_id]=expense
    return result