from .domeniu import CATEGORIES,get_day,get_amount,get_type
from .servicii import (add_expense,update_expense,remove_by_day,remove_by_interval,remove_by_type,find_greater_than,find_before_day_less_than,
                       find_by_type,find_by_amount,total_for_type,day_with_max_total,sort_by_type,filter_out_type,filter_out_less_than,load_sample_data,undo)

# Citire și Afișare

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
14. Elimină toate cheltuielile mai mici decât o sumă dată
15. Undo
16. Afișează toate cheltuielile
17. Încarcă 8 cheltuieli de test
 0. Ieșire""")

def ui_add_expense(expenses,history):
    day=read_int("Ziua (1-31): ")
    amount=read_amount("Suma: ")
    expense_type=read_type()
    add_expense(expenses,history,day,amount,expense_type)
    print("Cheltuială adăugată.")

def ui_update_expense(expenses,history):
    day=read_int("Ziua (1-31): ")
    amount=read_amount("Suma nouă: ")
    expense_type=read_type()
    update_expense(expenses,history,day,amount,expense_type)
    print("Cheltuială actualizată.")

def ui_remove_by_day(expenses,history):
    day=read_int("Ziua de șters (1-31): ")
    count=remove_by_day(expenses,history,day)
    print("Au fost eliminate " + str(count) + " cheltuieli.")

def ui_remove_by_interval(expenses,history):
    start_day=read_int("Ziua de început (1-31): ")
    end_day=read_int("Ziua de sfârșit (1-31): ")
    count=remove_by_interval(expenses, history,start_day,end_day)
    print("Au fost eliminate " + str(count) + " cheltuieli.")

def ui_remove_by_type(expenses,history):
    expense_type=read_type()
    count=remove_by_type(expenses,history,expense_type)
    print("Au fost eliminate " + str(count) + " cheltuieli.")

def ui_find_greater_than(expenses,history):
    amount=read_amount("Suma: ")
    print_expenses(find_greater_than(expenses,amount))

def ui_find_before_day_less_than(expenses,history):
    amount=read_amount("Suma (mai mici decât): ")
    day=read_int("Ziua (dinainte de): ")
    print_expenses(find_before_day_less_than(expenses,day,amount))

def ui_find_by_type(expenses,history):
    expense_type=read_type()
    print_expenses(find_by_type(expenses,expense_type))

def ui_total_for_type(expenses,history):
    expense_type=read_type()
    total=total_for_type(expenses,expense_type)
    print("Suma totală pentru %s: %.2f lei" % (expense_type,total))

def ui_day_with_max_total(expenses,history):
    result=day_with_max_total(expenses)
    if result is None:
        print("Nu există cheltuieli.")
    else:
        print("Ziua %d (total %.2f lei)" % (result[0],result[1]))

def ui_find_by_amount(expenses,history):
    amount=read_amount("Suma: ")
    print_expenses(find_by_amount(expenses,amount))

def ui_sort_by_type(expenses,history):
    print_expenses(sort_by_type(expenses))

def ui_filter_out_type(expenses,history):
    expense_type=read_type()
    print("Toate cheltuielile, fără cele de tipul '" + expense_type + "':")
    print_expenses(filter_out_type(expenses,expense_type))

def ui_filter_out_less_than(expenses,history):
    amount=read_amount("Suma (nu se afișează cele mai mici decât): ")
    print("Toate cheltuielile, fără cele mai mici decât " + str(amount) + " lei:")
    print_expenses(filter_out_less_than(expenses,amount))

def ui_print_all(expenses,history):
    print_expenses(expenses)

def ui_undo(expenses,history):
    undo(expenses,history)
    print("Ultima operație a fost refăcută.")

def ui_load_sample_data(expenses,history):
    count=load_sample_data(expenses,history)
    print("Au fost adăugate " + str(count) + " cheltuieli de test.")

COMMANDS={
    "1": ui_add_expense,
    "2": ui_update_expense,
    "3": ui_remove_by_day,
    "4": ui_remove_by_interval,
    "5": ui_remove_by_type,
    "6": ui_find_greater_than,
    "7": ui_find_before_day_less_than,
    "8": ui_find_by_type,
    "9": ui_total_for_type,
    "10": ui_day_with_max_total,
    "11": ui_find_by_amount,
    "12": ui_sort_by_type,
    "13": ui_filter_out_type,
    "14": ui_filter_out_less_than,
    "15": ui_undo,
    "16": ui_print_all,
    "17": ui_load_sample_data,
}

def run_command(command,expenses,history):
    if command in COMMANDS:
        COMMANDS[command](expenses,history)
    else:
        print("Eroare: comandă invalidă")