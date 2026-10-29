from .domeniu import(
    validate_day,validate_amount,validate_limit,validate_type,create_expense,get_day,get_amount,get_type
)

from .servicii import(
    add_expense,update_expense,remove_by_day,remove_by_interval,remove_by_type,find_greater_than,find_before_day_less_than,find_by_type,total_for_type,day_with_max_total,find_by_amount,sort_by_type,remove_less_than
)

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

print("Toate testele au trecut cu succes!")