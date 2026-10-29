from .domeniu import(
    CATEGORIES,MIN_DAY,MAX_DAY,validate_day,validate_limit,validate_type,create_expense,get_day,get_amount,get_type
)

# Adaugă/actualizează

def add_expense(expenses,day,amount,expense_type):
    expense=create_expense(day,amount,expense_type)
    expenses.append(expense)
    return expense

def update_expense(expenses,day,amount,expense_type):
    new_expense=create_expense(day,amount,expense_type)
    for i in range(len(expenses)):
        if get_day(expenses[i])==day and get_type(expenses[i])==expense_type:
            expenses[i]=new_expense
            return new_expense
    raise ValueError("Nu există nicio cheltuială în ziua " + str(day) + " de tipul '" + expense_type + "'")

# Ștergere

def remove_by_day(expenses,day):
    validate_day(day)
    kept=[]
    for expense in expenses:
        if get_day(expense)!=day:
            kept.append(expense)
    removed=len(expenses)-len(kept)
    expenses[:]=kept
    return removed

def remove_by_interval(expenses,start_day,end_day):
    validate_day(start_day)
    validate_day(end_day)
    if start_day>end_day:
        raise ValueError("Ziua de început nu poate fi după ziua de sfârșit")
    kept=[]
    for expense in expenses:
        if not (start_day<=get_day(expense)<=end_day):
            kept.append(expense)
    removed=len(expenses)-len(kept)
    expenses[:]=kept
    return removed

def remove_by_type(expenses,expense_type):
    validate_type(expense_type)
    kept=[]
    for expense in expenses:
        if get_type(expense)!=expense_type:
            kept.append(expense)
    removed=len(expenses)-len(kept)
    expenses[:]=kept
    return removed

# Căutare

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
            best_total=total
            best_day=day
    if best_day is None:
        return None
    return (best_day,best_total)

def find_by_amount(expenses,amount):
    validate_limit(amount)
    result=[]
    for expense in expenses:
        if get_amount(expense)==round(amount,2):
            result.append(expense)
    return result

def sort_by_type(expenses):
    result=[]
    for category in CATEGORIES:
        for expense in expenses:
            if get_type(expense)==category:
                result.append(expense)
    return result

# Filtrare

def remove_less_than(expenses,amount):
    validate_limit(amount)
    kept=[]
    for expense in expenses:
        if get_amount(expense)>=amount:
            kept.append(expense)
    removed=len(expenses)-len(kept)
    expenses[:]=kept
    return removed