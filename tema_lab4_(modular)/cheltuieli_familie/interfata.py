from .domeniu import CATEGORIES
from .servicii import(
    get_day,get_amount,get_type,add_expense,update_expense,remove_by_day,remove_by_interval,remove_by_type,
    find_greater_than,find_before_day_less_than,find_by_type,total_for_type,day_with_max_total,find_by_amount,sort_by_type,remove_less_than
)

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
--- Cheltuieli de familie ---
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