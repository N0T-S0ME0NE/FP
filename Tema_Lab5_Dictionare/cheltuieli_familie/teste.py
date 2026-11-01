STORAGE='dict'
from .domeniu import create_expense, get_day, get_amount, get_type, validate_day, validate_amount, validate_limit, validate_type
from .servicii import *

def sample():
    x={} if STORAGE=='dict' else []
    add_expense(x,3,120.5,'mâncare'); add_expense(x,5,300,'întreținere'); add_expense(x,5,45,'mâncare')
    add_expense(x,10,80,'telefon'); add_expense(x,12,250,'îmbrăcăminte'); add_expense(x,12,30,'altele'); add_expense(x,20,45,'mâncare')
    return x

def values(x): return x.values() if STORAGE=='dict' else x

def run_all_tests():
    validate_day(1); validate_amount(0.01); validate_limit(0); validate_type('telefon')
    assert create_expense(5,120.456,'mâncare') and get_amount(create_expense(5,120.456,'mâncare'))==120.46
    x={} if STORAGE=='dict' else []
    add_expense(x,5,100,'mâncare'); add_expense(x,7,20.5,'telefon')
    assert len(x)==2
    update_expense(x,5,99,'mâncare')
    assert get_amount(list(values(x))[0])==99
    x=sample(); assert remove_by_day(x,5)==2 and len(x)==5
    x=sample(); assert remove_by_interval(x,5,12)==5 and len(x)==2
    x=sample(); assert remove_by_type(x,'altele')==1 and len(x)==6
    x=sample(); assert len(find_greater_than(x,100))==3
    assert len(find_before_day_less_than(x,12,100))==2
    assert len(find_by_type(x,'mâncare'))==3
    assert total_for_type(x,'mâncare')==210.5
    assert day_with_max_total(x)==(5,345)
    assert len(find_by_amount(x,45))==2
    assert len(sort_by_type(x))==7
    remove_by_type(x,'altele')
    assert remove_less_than(x,50)==2
    try: validate_day(40)
    except ValueError: pass
    else: assert False
    print('Toate testele au trecut cu succes!')
run_all_tests()