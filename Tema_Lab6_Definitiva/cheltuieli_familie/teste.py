from .domeniu import (create_expense,get_day,get_amount,get_type,validate_day,validate_amount,validate_limit,validate_type)
from .servicii import (SAMPLE_DATA,copy_expenses,save_state,undo,add_expense,update_expense,load_sample_data,filter_out_type,filter_out_less_than,remove_by_day,remove_by_interval,
                       remove_by_type,find_greater_than,find_before_day_less_than,find_by_type,find_by_amount,total_for_type,day_with_max_total,sort_by_type)

def raises_value_error(function, *arguments):
    try:
        function(*arguments)
    except ValueError:
        return True
    return False

# Creare exemplu folosit pentru Teste

def make_sample():
    expenses=[]
    history=[]
    load_sample_data(expenses,history)
    history.clear()
    return expenses,history

# Teste

# Validare

def test_validators():
    validate_day(1)
    validate_day(31)
    assert raises_value_error(validate_day,0)
    assert raises_value_error(validate_day,32)
    assert raises_value_error(validate_day,2.5)
    assert raises_value_error(validate_day,True)

    validate_amount(0.01)
    assert raises_value_error(validate_amount,0)
    assert raises_value_error(validate_amount,-5)
    assert raises_value_error(validate_amount,"10")

    validate_limit(0)
    assert raises_value_error(validate_limit,-1)

    validate_type('telefon')
    assert raises_value_error(validate_type,'distracție')

def test_create_expense():
    expense=create_expense(5,120.456,'mâncare')
    assert get_day(expense)==5
    assert get_amount(expense)==120.46
    assert get_type(expense)=='mâncare'
    assert raises_value_error(create_expense,40,10,'mâncare')
    assert raises_value_error(create_expense,5,-10,'mâncare')
    assert raises_value_error(create_expense,5,10,'xyz')

# Adăugare/Actualizare

def test_add_expense():
    expenses=[]
    history=[]
    added=add_expense(expenses,history,5,100,'mâncare')
    add_expense(expenses,history,7,20.5,'telefon')
    assert len(expenses)==2
    assert added==[5,100,'mâncare']
    assert raises_value_error(add_expense,expenses,history,0,10,'altele')
    assert len(expenses)==2

def test_update_expense():
    expenses=[]
    history=[]
    add_expense(expenses,history,5,100,'mâncare')
    update_expense(expenses,history,5,99,'mâncare')
    assert get_amount(expenses[0])==99
    assert raises_value_error(update_expense,expenses,history,6,99,'mâncare')
    assert raises_value_error(update_expense,expenses,history,5,99,'telefon')

def test_load_sample_data():
    expenses=[]
    history=[]
    assert load_sample_data(expenses,history)==8
    assert len(expenses)==8
    assert len(SAMPLE_DATA)==8
    assert len(history)==1

# Ștergere

def test_remove_by_day():
    expenses,history=make_sample()
    assert remove_by_day(expenses,history,5)==2
    assert len(expenses)==6
    assert remove_by_day(expenses,history,5)==0
    assert raises_value_error(remove_by_day,expenses,history,99)

def test_remove_by_interval():
    expenses,history=make_sample()
    assert remove_by_interval(expenses,history,5,12)==5
    assert len(expenses)==3
    assert raises_value_error(remove_by_interval,expenses,history,12,5)

def test_remove_by_type():
    expenses,history=make_sample()
    assert remove_by_type(expenses,history,'altele')==1
    assert len(expenses)==7
    assert remove_by_type(expenses,history,'întreținere')==2
    assert len(expenses)==5
    assert raises_value_error(remove_by_type,expenses,history,'xyz')

# Căutări

def test_find_greater_than():
    expenses,history=make_sample()
    assert len(find_greater_than(expenses,100))==4
    assert len(find_greater_than(expenses,500))==0
    assert raises_value_error(find_greater_than,expenses,-1)

def test_find_before_day_less_than():
    expenses,history=make_sample()
    assert len(find_before_day_less_than(expenses,12,100))==2
    assert len(find_before_day_less_than(expenses,1,1000))==0
    assert raises_value_error(find_before_day_less_than,expenses,0,100)

def test_find_by_type():
    expenses,history=make_sample()
    assert len(find_by_type(expenses,'mâncare'))==2
    assert len(find_by_type(expenses,'altele'))==1
    assert raises_value_error(find_by_type,expenses,'xyz')

def test_find_by_amount():
    expenses,history=make_sample()
    assert len(find_by_amount(expenses,45))==2
    assert len(find_by_amount(expenses,120.5))==1
    assert len(find_by_amount(expenses,7))==0

# Rapoarte

def test_total_for_type():
    expenses,history=make_sample()
    assert total_for_type(expenses,'mâncare')==165.5
    assert total_for_type(expenses,'întreținere')==800
    assert total_for_type([],'mâncare')==0

def test_day_with_max_total():
    expenses,history=make_sample()
    assert day_with_max_total(expenses)==(25,500)
    remove_by_day(expenses,history,25)
    assert day_with_max_total(expenses)==(5,345)
    assert day_with_max_total([]) is None

def test_sort_by_type():
    expenses,history=make_sample()
    result=sort_by_type(expenses)
    assert len(result)==8
    assert get_type(result[0])=='mâncare'
    assert get_type(result[-1])=='altele'
    assert len(expenses)==8

# Filtrare

def test_filter_out_type():
    expenses,history=make_sample()
    result=filter_out_type(expenses,'telefon')
    assert len(result)==6
    for expense in result:
        assert get_type(expense)!='telefon'
    assert len(expenses)==8
    assert len(history)==0
    assert raises_value_error(filter_out_type,expenses,'xyz')

def test_filter_out_less_than():
    expenses,history=make_sample()
    result=filter_out_less_than(expenses,100)
    assert len(result)==4
    for expense in result:
        assert get_amount(expense)>=100
    assert len(filter_out_less_than(expenses,45))==7
    assert len(expenses)==8
    assert len(history)==0
    assert raises_value_error(filter_out_less_than,expenses,-1)

# Undo

def test_copy_expenses():
    original=[[5,100,'mâncare']]
    copy=copy_expenses(original)
    assert copy==original
    copy[0][1]=999
    assert original[0][1]==100

def test_save_state_and_undo():
    expenses=[[5,100,'mâncare']]
    history=[]
    save_state(expenses,history)
    expenses.append([6,50,'telefon'])
    assert len(history)==1 and len(history[0])==1
    undo(expenses,history)
    assert expenses==[[5,100,'mâncare']]
    assert len(history)==0
    assert raises_value_error(undo,expenses,history)

def test_undo_after_each_operation():
    expenses,history=make_sample()
    before=copy_expenses(expenses)

    add_expense(expenses,history,7,10,'altele')
    undo(expenses,history)
    assert expenses==before

    update_expense(expenses,history,5,1,'mâncare')
    undo(expenses,history)
    assert expenses==before

    remove_by_day(expenses,history,5)
    undo(expenses,history)
    assert expenses==before

    remove_by_interval(expenses,history,1,31)
    undo(expenses,history)
    assert expenses==before

    remove_by_type(expenses,history,'telefon')
    undo(expenses,history)
    assert expenses==before

    load_sample_data(expenses,history)
    assert len(expenses)==16
    undo(expenses,history)
    assert expenses==before

def test_undo_multiple_steps():
    expenses=[]
    history=[]
    add_expense(expenses,history,1,10,'mâncare')
    add_expense(expenses,history,2,20,'telefon')
    remove_by_day(expenses,history,1)
    assert len(expenses)==1
    undo(expenses,history)
    assert len(expenses)==2
    undo(expenses,history)
    assert len(expenses)==1
    undo(expenses,history)
    assert len(expenses)==0

def test_failed_operations_do_not_change_history():
    expenses,history=make_sample()
    assert raises_value_error(add_expense,expenses,history,40,10,'altele')
    assert raises_value_error(update_expense,expenses,history,1,10,'altele')
    assert raises_value_error(remove_by_interval,expenses,history,10,5)
    assert remove_by_day(expenses,history,31)==0
    assert len(history)==0
    assert len(expenses)==8

# Rularea Testelor

def run_all_tests():
    test_validators()
    test_create_expense()
    test_copy_expenses()
    test_save_state_and_undo()
    test_undo_after_each_operation()
    test_undo_multiple_steps()
    test_failed_operations_do_not_change_history()
    test_add_expense()
    test_update_expense()
    test_load_sample_data()
    test_filter_out_type()
    test_filter_out_less_than()
    test_remove_by_day()
    test_remove_by_interval()
    test_remove_by_type()
    test_find_greater_than()
    test_find_before_day_less_than()
    test_find_by_type()
    test_find_by_amount()
    test_total_for_type()
    test_day_with_max_total()
    test_sort_by_type()

    print("Toate testele au trecut cu succes!")