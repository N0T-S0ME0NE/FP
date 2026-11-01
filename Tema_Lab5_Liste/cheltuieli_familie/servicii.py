from .domeniu import CATEGORIES, MIN_DAY, MAX_DAY, validate_day, validate_limit, validate_type, create_expense, get_day, get_amount, get_type

def add_expense(expenses,day,amount,expense_type):
    expense=create_expense(day,amount,expense_type); expenses.append(expense); return expense

def update_expense(expenses,day,amount,expense_type):
    new=create_expense(day,amount,expense_type)
    for i in range(len(expenses)):
        if get_day(expenses[i])==day and get_type(expenses[i])==expense_type:
            expenses[i]=new; return new
    raise ValueError("Nu există nicio cheltuială în ziua "+str(day)+" de tipul '"+expense_type+"'")

def _remove(expenses,predicate):
    kept=[]; removed=0
    for e in expenses:
        if predicate(e): removed+=1
        else: kept.append(e)
    expenses[:]=kept; return removed

def remove_by_day(expenses,day):
    validate_day(day); return _remove(expenses,lambda e:get_day(e)==day)

def remove_by_interval(expenses,start_day,end_day):
    validate_day(start_day); validate_day(end_day)
    if start_day>end_day: raise ValueError("Ziua de început nu poate fi după ziua de sfârșit")
    return _remove(expenses,lambda e:start_day<=get_day(e)<=end_day)

def remove_by_type(expenses,expense_type):
    validate_type(expense_type); return _remove(expenses,lambda e:get_type(e)==expense_type)

def find_greater_than(expenses,amount):
    validate_limit(amount); return [e for e in expenses if get_amount(e)>amount]

def find_before_day_less_than(expenses,day,amount):
    validate_day(day); validate_limit(amount); return [e for e in expenses if get_day(e)<day and get_amount(e)<amount]

def find_by_type(expenses,expense_type):
    validate_type(expense_type); return [e for e in expenses if get_type(e)==expense_type]

def total_for_type(expenses,expense_type):
    return round(sum(get_amount(e) for e in find_by_type(expenses,expense_type)),2)

def day_with_max_total(expenses):
    best_day=None; best_total=0
    for day in range(MIN_DAY,MAX_DAY+1):
        total=0
        for e in expenses:
            if get_day(e)==day: total+=get_amount(e)
        if round(total,2)>best_total: best_day=day; best_total=round(total,2)
    return None if best_day is None else (best_day,best_total)

def find_by_amount(expenses,amount):
    validate_limit(amount); return [e for e in expenses if get_amount(e)==round(amount,2)]

def sort_by_type(expenses):
    result=[]
    for category in CATEGORIES:
        for e in expenses:
            if get_type(e)==category: result.append(e)
    return result

def remove_less_than(expenses,amount):
    validate_limit(amount); return _remove(expenses,lambda e:get_amount(e)<amount)