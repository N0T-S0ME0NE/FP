from .domeniu import (create_expense,get_day,get_amount,get_type,validate_day,validate_amount,validate_limit,validate_type)
from .servicii import (SAMPLE_DATA,add_expense,update_expense,load_sample_data,filter_out_type,filter_out_less_than,remove_by_day,remove_by_interval,
                       remove_by_type,find_greater_than,find_before_day_less_than,find_by_type,find_by_amount,total_for_type,day_with_max_total,sort_by_type)

def raises_value_error(function,*arguments):
    try:
        function(*arguments)
    except ValueError:
        return True
    return False

# Creare exemplu folosit pentru Teste

def make_sample():
    expenses={}
    load_sample_data(expenses)
    return expenses

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
    expenses={}
    added=add_expense(expenses,5,100,'mâncare')
    add_expense(expenses,7,20.5,'telefon')
    assert len(expenses)==2
    assert added=={"ziua":5,"suma":100,"tip":"mâncare"}
    assert raises_value_error(add_expense,expenses,0,10,'altele')
    assert len(expenses)==2

def test_update_expense():
    expenses={}
    add_expense(expenses,5,100,'mâncare')
    update_expense(expenses,5,99,'mâncare')
    assert get_amount(expenses[1])==99
    assert raises_value_error(update_expense,expenses,6,99,'mâncare')
    assert raises_value_error(update_expense,expenses,5,99,'telefon')

def test_load_sample_data():
    expenses={}
    assert load_sample_data(expenses)==8
    assert len(expenses)==8
    assert len(SAMPLE_DATA)==8

# Ștergere

def test_remove_by_day():
    expenses=make_sample()
    assert remove_by_day(expenses,5)==2
    assert len(expenses)==6
    assert remove_by_day(expenses,5)==0
    assert raises_value_error(remove_by_day,expenses,99)

def test_remove_by_interval():
    expenses=make_sample()
    assert remove_by_interval(expenses,5,12)==5
    assert len(expenses)==3
    assert raises_value_error(remove_by_interval,expenses,12,5)

def test_remove_by_type():
    expenses=make_sample()
    assert remove_by_type(expenses,'altele')==1
    assert len(expenses)==7
    assert remove_by_type(expenses,'întreținere')==2
    assert len(expenses)==5
    assert raises_value_error(remove_by_type,expenses,'xyz')

# Căutări

def test_find_greater_than():
    expenses=make_sample()
    assert len(find_greater_than(expenses,100))==4
    assert len(find_greater_than(expenses,500))==0
    assert raises_value_error(find_greater_than,expenses,-1)

def test_find_before_day_less_than():
    expenses=make_sample()
    assert len(find_before_day_less_than(expenses,12,100))==2
    assert len(find_before_day_less_than(expenses,1,1000))==0
    assert raises_value_error(find_before_day_less_than,expenses,0,100)

def test_find_by_type():
    expenses=make_sample()
    assert len(find_by_type(expenses,'mâncare'))==2
    assert len(find_by_type(expenses,'altele'))==1
    assert raises_value_error(find_by_type,expenses,'xyz')

def test_find_by_amount():
    expenses=make_sample()
    assert len(find_by_amount(expenses,45))==2
    assert len(find_by_amount(expenses,120.5))==1
    assert len(find_by_amount(expenses,7))==0

# Rapoarte

def test_total_for_type():
    expenses=make_sample()
    assert total_for_type(expenses,'mâncare')==165.5
    assert total_for_type(expenses,'întreținere')==800
    assert total_for_type({},'mâncare')==0

def test_day_with_max_total():
    expenses=make_sample()
    assert day_with_max_total(expenses)==(25,500)
    remove_by_day(expenses,25)
    assert day_with_max_total(expenses)==(5,345)
    assert day_with_max_total({}) is None

def test_sort_by_type():
    expenses=make_sample()
    result=sort_by_type(expenses)
    assert len(result)==8
    assert get_type(next(iter(result.values())))=='mâncare'
    assert get_type(result[max(result)])=='altele'
    assert len(expenses)==8

# Filtrare

def test_filter_out_type():
    expenses=make_sample()
    result=filter_out_type(expenses,'telefon')
    assert len(result)==6
    for expense in result.values():
        assert get_type(expense)!='telefon'
    assert len(expenses)==8
    assert raises_value_error(filter_out_type,expenses,'xyz')

def test_filter_out_less_than():
    expenses=make_sample()
    result=filter_out_less_than(expenses,100)
    assert len(result)==4
    for expense in result.values():
        assert get_amount(expense)>=100
    assert len(filter_out_less_than(expenses,45))==7
    assert len(expenses)==8
    assert raises_value_error(filter_out_less_than,expenses,-1)

def test_failed_operations_do_not_change_expenses():
    expenses=make_sample()
    assert raises_value_error(add_expense,expenses,40,10,'altele')
    assert raises_value_error(update_expense,expenses,1,10,'altele')
    assert raises_value_error(remove_by_interval,expenses,10,5)
    assert remove_by_day(expenses,31)==0
    assert len(expenses)==8

# Rularea Testelor

def run_all_tests():
    test_validators()
    test_create_expense()
    test_failed_operations_do_not_change_expenses()
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