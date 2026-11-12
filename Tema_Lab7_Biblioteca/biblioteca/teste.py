from .domeniu import (ValidationError,create_book,create_client,validate_id,validate_text,validate_name,validate_cnp)
from .repository import RepositoryError,Repository,BookRepository,ClientRepository
from .controller import SAMPLE_BOOKS,SAMPLE_CLIENTS,Controller

# CNP-uri valide folosite în teste
CNP1="5031114121014"
CNP2="6040308402156"

def raises(error_type,function,*arguments):
    try:
        function(*arguments)
    except error_type:
        return True
    return False

def make_controller():
    return Controller(BookRepository(),ClientRepository())

# Teste Domeniu

def test_validate_id():
    validate_id(1)
    validate_id(5000)
    assert raises(ValidationError,validate_id,0)
    assert raises(ValidationError,validate_id,-3)
    assert raises(ValidationError,validate_id,2.5)
    assert raises(ValidationError,validate_id,"7")
    assert raises(ValidationError,validate_id,True)

def test_validate_text():
    validate_text("Ion","Titlul",10)
    validate_text("  Ion  ","Titlul",3)
    assert raises(ValidationError,validate_text,"","Titlul",10)
    assert raises(ValidationError,validate_text,"   ","Titlul",10)
    assert raises(ValidationError,validate_text,5,"Titlul",10)
    assert raises(ValidationError,validate_text,"abcd","Titlul",3)

def test_validate_name():
    validate_name("Popescu Ion")
    validate_name("Ionescu Maria-Elena")
    assert raises(ValidationError,validate_name,"")
    assert raises(ValidationError,validate_name,"Popescu 2")
    assert raises(ValidationError,validate_name,"Ion!")
    assert raises(ValidationError,validate_name,"-")

def test_validate_cnp():
    validate_cnp(CNP1)
    validate_cnp(CNP2)
    assert raises(ValidationError,validate_cnp,"123")
    assert raises(ValidationError,validate_cnp,"50311141210145")
    assert raises(ValidationError,validate_cnp,"503111412101a")
    assert raises(ValidationError,validate_cnp,5031114121014)
    assert raises(ValidationError,validate_cnp,"5033114121014")
    assert raises(ValidationError,validate_cnp,"5030014121014")
    assert raises(ValidationError,validate_cnp,"0031114121014")
    assert raises(ValidationError,validate_cnp,"5031114121015")

def test_create_book():
    book=create_book(1,"  Ion  ","Roman","Liviu Rebreanu")
    assert book.get_id()==1
    assert book.get_title()=="Ion"
    assert book.get_description()=="Roman"
    assert book.get_author()=="Liviu Rebreanu"
    assert raises(ValidationError,create_book,0,"Ion","Roman","Liviu Rebreanu")
    assert raises(ValidationError,create_book,1,"","Roman","Liviu Rebreanu")
    assert raises(ValidationError,create_book,1,"Ion","","Liviu Rebreanu")
    assert raises(ValidationError,create_book,1,"Ion","Roman","  ")
    assert raises(ValidationError,create_book,1,"a"*101,"Roman","Liviu Rebreanu")

def test_create_client():
    client=create_client(2,"  Popescu Ion ",CNP1)
    assert client.get_id()==2
    assert client.get_name()=="Popescu Ion"
    assert client.get_cnp()==CNP1
    assert raises(ValidationError,create_client,-1,"Popescu Ion",CNP1)
    assert raises(ValidationError,create_client,2,"",CNP1)
    assert raises(ValidationError,create_client,2,"Popescu Ion","123")

# Teste Repository

def test_repository_add():
    repo=BookRepository()
    assert repo.size()==0
    repo.add(create_book(1,"Ion","Roman","Liviu Rebreanu"))
    repo.add(create_book(2,"Baltagul","Roman","Mihail Sadoveanu"))
    assert repo.size()==2
    assert raises(RepositoryError,repo.add,create_book(1,"Alta","Alta","Altul"))
    assert repo.size()==2

def test_repository_find_and_get_all():
    repo=BookRepository()
    book=create_book(1,"Ion","Roman","Liviu Rebreanu")
    repo.add(book)
    assert repo.find_by_id(1) is book
    assert repo.find_by_id(2) is None
    books=repo.get_all()
    assert books==[book]
    books.append(create_book(2,"Baltagul","Roman","Mihail Sadoveanu"))
    assert repo.size()==1

def test_client_repository():
    repo=ClientRepository()
    client=create_client(1,"Popescu Ion",CNP1)
    repo.add(client)
    assert repo.find_by_cnp(CNP1) is client
    assert repo.find_by_cnp(CNP2) is None
    assert raises(RepositoryError,repo.add,create_client(1,"Ionescu Maria",CNP2))
    assert raises(RepositoryError,repo.add,create_client(2,"Ionescu Maria",CNP1))
    assert repo.size()==1
    repo.add(create_client(2,"Ionescu Maria",CNP2))
    assert repo.size()==2

# Teste Controller

def test_add_book():
    controller=make_controller()
    book=controller.add_book(1,"Ion","Roman","Liviu Rebreanu")
    assert book.get_title()=="Ion"
    assert len(controller.get_books())==1
    assert raises(ValidationError,controller.add_book,0,"Ion","Roman","Liviu Rebreanu")
    assert raises(RepositoryError,controller.add_book,1,"Alta","Alta","Altul")
    assert len(controller.get_books())==1

def test_add_client():
    controller=make_controller()
    client=controller.add_client(1,"Popescu Ion",CNP1)
    assert client.get_name()=="Popescu Ion"
    assert len(controller.get_clients())==1
    assert raises(ValidationError,controller.add_client,2,"Ionescu Maria","123")
    assert raises(RepositoryError,controller.add_client,2,"Ionescu Maria",CNP1)
    assert raises(RepositoryError,controller.add_client,1,"Ionescu Maria",CNP2)
    assert len(controller.get_clients())==1

def test_get_all_empty():
    controller=make_controller()
    assert controller.get_books()==[]
    assert controller.get_clients()==[]

def test_load_sample_data():
    controller=make_controller()
    assert controller.load_sample_data()==(5,4)
    assert len(controller.get_books())==len(SAMPLE_BOOKS)
    assert len(controller.get_clients())==len(SAMPLE_CLIENTS)
    assert controller.load_sample_data()==(0,0)
    assert len(controller.get_books())==5

def test_load_sample_data_with_existing():
    controller=make_controller()
    controller.add_book(3,"Altă carte","Descriere","Alt autor")
    controller.add_client(9,"Vasilescu Ana",CNP1)
    assert controller.load_sample_data()==(4,3)
    assert len(controller.get_books())==5
    assert len(controller.get_clients())==4

# Rularea Testelor

def run_all_tests():
    test_validate_id()
    test_validate_text()
    test_validate_name()
    test_validate_cnp()
    test_create_book()
    test_create_client()
    test_repository_add()
    test_repository_find_and_get_all()
    test_client_repository()
    test_add_book()
    test_add_client()
    test_get_all_empty()
    test_load_sample_data()
    test_load_sample_data_with_existing()

    print("Toate testele au trecut cu succes!")