CATEGORIES=['mâncare','întreținere','îmbrăcăminte','telefon','altele']
MIN_DAY=1
MAX_DAY=31
MAX_AMOUNT=1000000000

# Domeniu

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

# Teste

def raises_error(function,*args):
    try:
        function(*args)
    except ValueError:
        return True
    return False

def make_sample():
    expenses=[]
    add_expense(expenses,3,120.5,'mâncare')
    add_expense(expenses,5,300,'întreținere')
    add_expense(expenses,5,45,'mâncare')
    add_expense(expenses,10,80,'telefon')
    add_expense(expenses,12,250,'îmbrăcăminte')
    add_expense(expenses,12,30,'altele')
    add_expense(expenses,20,45,'mâncare')
    return expenses

def days_of(expenses):
    result=[]
    for expense in expenses:
        result.append(get_day(expense))
    return result

def test_validations():
    validate_day(1)
    validate_day(31)
    assert raises_error(validate_day,0)
    assert raises_error(validate_day,32)
    assert raises_error(validate_day,2.5)
    assert raises_error(validate_day,"5")
    validate_amount(0.01)
    assert raises_error(validate_amount,0)
    assert raises_error(validate_amount,-3)
    assert raises_error(validate_amount,"10")
    assert raises_error(validate_amount,float('nan'))
    validate_limit(0)
    assert raises_error(validate_limit,-1)
    validate_type('telefon')
    assert raises_error(validate_type,'transport')

def test_create_expense():
    expense=create_expense(5,120.456,'mâncare')
    assert get_day(expense)==5
    assert get_amount(expense)==120.46
    assert get_type(expense)=='mâncare'
    assert raises_error(create_expense,0,10,'telefon')
    assert raises_error(create_expense,5,-10,'telefon')
    assert raises_error(create_expense,5,10,'transport')

def test_add_expense():
    expenses=[]
    add_expense(expenses,5,100,'mâncare')
    add_expense(expenses,7,20.5,'telefon')
    assert days_of(expenses)==[5,7]
    assert raises_error(add_expense,expenses,0,10,'telefon')
    assert raises_error(add_expense,expenses,5,10,'transport')
    assert days_of(expenses)==[5,7]

def test_update_expense():
    expenses=make_sample()
    update_expense(expenses,5,99,'mâncare')
    assert get_amount(expenses[2])==99
    assert len(expenses)==7
    assert raises_error(update_expense,expenses,6,10,'mâncare')
    assert raises_error(update_expense,expenses,5,-2,'mâncare')

def test_removals():
    expenses = make_sample()
    assert remove_by_day(expenses,5)==2
    assert days_of(expenses)==[3,10,12,12,20]
    
    expenses=make_sample()
    assert remove_by_interval(expenses,5,12)==5
    assert days_of(expenses)==[3,20]
    
    expenses=make_sample()
    assert remove_by_type(expenses,'altele')==1
    assert len(expenses)==6
    
    assert raises_error(remove_by_day,expenses,40)
    assert raises_error(remove_by_interval,expenses,15,10)
    assert raises_error(remove_by_type,expenses,'transport')

def test_searches():
    expenses=make_sample()
    assert days_of(find_greater_than(expenses,100))==[3,5,12]
    assert find_greater_than(expenses,300)==[]
    assert raises_error(find_greater_than,expenses,-1)
    assert days_of(find_before_day_less_than(expenses,12,100))==[5,10]
    assert find_before_day_less_than(expenses,3,1000)==[]
    assert raises_error(find_before_day_less_than,expenses,40,10)
    assert days_of(find_by_type(expenses,'mâncare'))==[3,5,20]
    assert find_by_type([],'altele')==[]
    assert raises_error(find_by_type,expenses,'transport')

def test_reports():
    expenses=make_sample()
    assert total_for_type(expenses,'mâncare')==210.5
    assert total_for_type([],'telefon')==0
    assert day_with_max_total(expenses)==(5,345)
    assert day_with_max_total([]) is None
    assert days_of(find_by_amount(expenses,45))==[5,20]
    assert find_by_amount(expenses,46)==[]
    ordered=sort_by_type(expenses)
    assert days_of(ordered)==[3,5,20,5,12,10,12]
    assert days_of(expenses)==[3,5,5,10,12,12,20]

def test_filters():
    expenses=make_sample()
    assert remove_by_type(expenses,'altele')==1
    assert len(expenses)==6
    assert remove_less_than(expenses,50)==2
    assert days_of(expenses)==[3,5,10,12]
    assert remove_less_than(expenses,80)==0
    assert raises_error(remove_by_type,expenses,'transport')
    assert raises_error(remove_less_than,expenses,-5)

def run_all_tests():
    test_validations()
    test_create_expense()
    test_add_expense()
    test_update_expense()
    test_removals()
    test_searches()
    test_reports()
    test_filters()
run_all_tests()

# Meniu

def read_int(prompt):
    text=input(prompt).strip()
    try:
        return int(text)
    except ValueError:
        raise ValueError("'" + text + "' nu este un număr întreg")

def read_amount(prompt):
    text=input(prompt).strip()
    try:
        return float(text.replace(",", "."))
    except ValueError:
        raise ValueError("'" + text + "' nu este un număr")

def read_type():
    for i in range(len(CATEGORIES)):
        print("   " + str(i+1) + " - " + CATEGORIES[i])
    number=read_int("Tipul (1-5): ")
    if number<1 or number>len(CATEGORIES):
        raise ValueError("Tipul trebuie să fie un număr între 1 și 5")
    return CATEGORIES[number-1]

def print_expenses(expenses):
    if len(expenses)==0:
        print("Nu există cheltuieli.")
        return
    for expense in expenses:
        print("  Ziua %2d | %10.2f lei | %s" % (get_day(expense),get_amount(expense),get_type(expense)))
    print("Total: " + str(len(expenses)) + " cheltuieli")

def print_menu():
    print("""
--- Cheltuieli de familie (iterația 1) ---
 1. Adaugă o nouă cheltuială
 2. Actualizează o cheltuială
 3. Șterge cheltuielile pentru o zi dată
 4. Șterge cheltuielile pentru un interval de timp
 5. Șterge toate cheltuielile de un anumit tip
 6. Tipărește cheltuielile mai mari decât o sumă
 7. Tipărește cheltuielile dinainte de o zi și mai mici decât o sumă
 8. Tipărește cheltuielile de un anumit tip
 9. Suma totală pentru un tip de cheltuială
10. Ziua cu suma cheltuită maximă
11. Tipărește cheltuielile cu o anumită sumă
12. Tipărește cheltuielile sortate după tip
13. Elimină toate cheltuielile de un anumit tip
14. Elimină toate cheltuielile mai mici decât o sumă
15. Afișează toate cheltuielile
 0. Ieșire""")

def run_command(command, expenses):
    match command:
        case "1":
            day=read_int("Ziua (1-31): ")
            amount=read_amount("Suma: ")
            expense_type=read_type()
            add_expense(expenses,day,amount,expense_type)
            print("Cheltuială adăugată.")
        case "2":
            day=read_int("Ziua (1-31): ")
            amount=read_amount("Suma nouă: ")
            expense_type=read_type()
            update_expense(expenses,day,amount,expense_type)
            print("Cheltuială actualizată.")
        case "3":
            day=read_int("Ziua de șters (1-31): ")
            count=remove_by_day(expenses,day)
            print("Au fost eliminate " + str(count) + " cheltuieli.")
        case "4":
            start_day=read_int("Ziua de început (1-31): ")
            end_day=read_int("Ziua de sfârșit (1-31): ")
            count=remove_by_interval(expenses,start_day,end_day)
            print("Au fost eliminate " + str(count) + " cheltuieli.")
        case "5":
            expense_type=read_type()
            count=remove_by_type(expenses,expense_type)
            print("Au fost eliminate " + str(count) + " cheltuieli.")
        case "6":
            amount=read_amount("Suma: ")
            print_expenses(find_greater_than(expenses,amount))
        case "7":
            amount=read_amount("Suma (mai mici decât): ")
            day=read_int("Ziua (dinainte de): ")
            print_expenses(find_before_day_less_than(expenses,day,amount))
        case "8":
            expense_type=read_type()
            print_expenses(find_by_type(expenses,expense_type))
        case "9":
            expense_type=read_type()
            total=total_for_type(expenses,expense_type)
            print("Suma totală pentru %s: %.2f lei" % (expense_type,total))
        case "10":
            result=day_with_max_total(expenses)
            if result is None:
                print("Nu există cheltuieli.")
            else:
                print("Ziua %d (total %.2f lei)" % (result[0],result[1]))
        case "11":
            amount=read_amount("Suma: ")
            print_expenses(find_by_amount(expenses,amount))
        case "12":
            print_expenses(sort_by_type(expenses))
        case "13":
            expense_type=read_type()
            count=remove_by_type(expenses,expense_type)
            print("Au fost eliminate " + str(count) + " cheltuieli.")
        case "14":
            amount=read_amount("Suma (se elimină cele mai mici decât): ")
            count=remove_less_than(expenses,amount)
            print("Au fost eliminate " + str(count) + " cheltuieli.")
        case "15":
            print_expenses(expenses)
        case _:
            print("Eroare: comandă invalidă")

def main():
    expenses=[]
    finished=False
    while not finished:
        print_menu()
        try:
            command=input("Comandă: ").strip()
            if command=="0":
                finished=True
            else:
                run_command(command,expenses)
        except ValueError as error:
            print("Eroare: " + str(error))
        except EOFError:
            finished=True
    print("Programul se va închide...")
main()