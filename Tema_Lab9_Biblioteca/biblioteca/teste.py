from unittest.mock import patch
from .domeniu import (ValidationError,create_book,create_client,create_rental,validate_id,validate_text,validate_name,validate_cnp)
from .repository import RepositoryError,BookRepository,ClientRepository,RentalRepository
from .controller import BOOK_TYPES,Controller,ControllerError,top_count
from .interfata import Console

# CNP-uri valide folosite în teste
CNP1="5031114121014"
CNP2="6040308402156"
CNP3="1980723354322"

def raises(error_type,function,*arguments):
    try:
        function(*arguments)
    except error_type:
        return True
    return False

def make_controller():
    return Controller(BookRepository(),ClientRepository(),RentalRepository())

def make_filled_controller():
    controller=make_controller()
    controller.add_book(1,"Ion","Roman rural","Liviu Rebreanu")
    controller.add_book(2,"Baltagul","Roman despre un cioban","Mihail Sadoveanu")
    controller.add_client(1,"Popescu Ion",CNP1)
    controller.add_client(2,"Ionescu Maria",CNP2)
    return controller

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

def test_create_rental():
    rental=create_rental(1,2)
    assert rental.get_client_id()==1
    assert rental.get_book_id()==2
    assert not rental.is_returned()
    rental.mark_returned()
    assert rental.is_returned()
    assert raises(ValidationError,create_rental,0,2)
    assert raises(ValidationError,create_rental,1,-2)

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

def test_repository_get_remove_update():
    repo=BookRepository()
    book=create_book(1,"Ion","Roman","Liviu Rebreanu")
    repo.add(book)
    assert repo.get(1) is book
    assert raises(RepositoryError,repo.get,2)
    new_book=create_book(1,"Ion (nou)","Roman nou","Liviu Rebreanu")
    repo.update(new_book)
    assert repo.get(1) is new_book
    assert repo.size()==1
    assert raises(RepositoryError,repo.update,create_book(2,"Alta","Alta","Altul"))
    assert repo.remove(1) is new_book
    assert repo.size()==0
    assert raises(RepositoryError,repo.remove,1)

def test_client_repository_update():
    repo=ClientRepository()
    repo.add(create_client(1,"Popescu Ion",CNP1))
    repo.add(create_client(2,"Ionescu Maria",CNP2))
    repo.update(create_client(1,"Popescu Ioan",CNP1))
    assert repo.get(1).get_name()=="Popescu Ioan"
    repo.update(create_client(1,"Popescu Ioan",CNP3))
    assert repo.get(1).get_cnp()==CNP3
    assert raises(RepositoryError,repo.update,create_client(1,"Popescu Ioan",CNP2))
    assert raises(RepositoryError,repo.update,create_client(7,"Vasilescu Ana",CNP1))
    assert repo.get(1).get_cnp()==CNP3

def test_book_search():
    repo=BookRepository()
    repo.add(create_book(1,"Ion","Roman rural","Liviu Rebreanu"))
    repo.add(create_book(12,"Baltagul","Roman","Mihail Sadoveanu"))
    assert len(repo.search("ion"))==1
    assert repo.search(" REBREANU ")[0].get_id()==1
    assert len(repo.search("a"))==2
    assert repo.search("12")[0].get_title()=="Baltagul"
    assert repo.search("roman")==[]
    assert repo.search("xyz")==[]

def test_client_search():
    repo=ClientRepository()
    repo.add(create_client(1,"Popescu Ion",CNP1))
    repo.add(create_client(2,"Ionescu Maria",CNP2))
    assert len(repo.search("ion"))==2
    assert repo.search("POPESCU")[0].get_id()==1
    assert repo.search(CNP2)[0].get_id()==2
    assert repo.search("604")[0].get_id()==2
    assert repo.get(2) in repo.search("2")
    assert repo.search("xyz")==[]

def test_rental_repository():
    repo=RentalRepository()
    assert repo.get_active()==[]
    first=create_rental(1,10)
    second=create_rental(1,11)
    third=create_rental(2,12)
    repo.add(first)
    repo.add(second)
    repo.add(third)
    assert repo.find_active_by_book(10) is first
    assert repo.find_active_by_book(99) is None
    assert len(repo.get_active_by_client(1))==2
    first.mark_returned()
    assert repo.find_active_by_book(10) is None
    assert len(repo.get_active())==2
    assert len(repo.get_all())==3
    repo.remove_by_book(10)
    assert len(repo.get_all())==2
    repo.remove_by_client(1)
    assert repo.get_all()==[third]

def test_rental_counts():
    repo=RentalRepository()
    assert repo.count_by_book(1)==0
    assert repo.count_by_client(1)==0
    first=create_rental(1,10)
    repo.add(first)
    first.mark_returned()
    repo.add(create_rental(2,10))
    repo.add(create_rental(1,11))
    assert repo.count_by_book(10)==2
    assert repo.count_by_book(11)==1
    assert repo.count_by_book(99)==0
    assert repo.count_by_client(1)==2
    assert repo.count_by_client(2)==1

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
    assert controller.load_sample_data(5)==(5,5,5)
    books=controller.get_books()
    clients=controller.get_clients()
    assert len(books)==len(clients)==5
    assert sum(count for _,count in controller.get_most_rented_books())==5
    assert len({book.get_author() for book in books})==5
    assert len({client.get_cnp() for client in clients})==5
    for book in books:
        assert len(book.get_title().split())==2
        assert book.get_description() in BOOK_TYPES
        validate_name(book.get_author())
    for client in clients:
        validate_name(client.get_name())
        validate_cnp(client.get_cnp())
    assert controller.load_sample_data(0)==(0,0,0)
    assert raises(ValidationError,controller.load_sample_data,-1)

def test_load_sample_data_with_existing():
    controller=make_controller()
    controller.add_book(3,"Altă carte","Descriere","Alt autor")
    controller.add_client(9,"Vasilescu Ana",CNP1)
    assert controller.load_sample_data(4)==(4,4,4)
    assert len(controller.get_books())==5
    assert len(controller.get_clients())==5
    assert sum(count for _,count in controller.get_most_rented_books())==4
    assert min(book.get_id() for book in controller.get_books() if book.get_id()!=3)>3
    assert min(client.get_id() for client in controller.get_clients() if client.get_id()!=9)>9

def test_load_sample_data_reuses_book_safely():
    controller=make_controller()
    def choose_first_except_rental_status(options):
        if options==(True,False):
            return False
        return options[0]
    with patch("biblioteca.controller.random.choice",side_effect=choose_first_except_rental_status):
        assert controller.load_sample_data(3)==(3,3,3)
    assert controller.get_books()[0].get_title()=="Amurgul zorilor"
    rentals=controller.get_active_rentals()
    assert len(rentals)==1
    assert sum(count for _,count in controller.get_most_rented_books())==3

def test_console_load_sample_data_reads_count():
    controller=make_controller()
    console=Console(controller)
    with patch("builtins.input",return_value="2"):
        console.run_command("14")
    assert len(controller.get_books())==2
    assert len(controller.get_clients())==2
    assert sum(count for _,count in controller.get_most_rented_books())==2

def test_get_book_and_client():
    controller=make_filled_controller()
    assert controller.get_book(1).get_title()=="Ion"
    assert controller.get_client(2).get_name()=="Ionescu Maria"
    assert raises(RepositoryError,controller.get_book,9)
    assert raises(RepositoryError,controller.get_client,9)
    assert raises(ValidationError,controller.get_book,0)
    assert raises(ValidationError,controller.get_client,-1)

def test_update_book():
    controller=make_filled_controller()
    book=controller.update_book(1,"Ion (ed. 2)","Roman rural","Liviu Rebreanu")
    assert book.get_title()=="Ion (ed. 2)"
    assert controller.get_book(1).get_title()=="Ion (ed. 2)"
    assert len(controller.get_books())==2
    assert raises(ValidationError,controller.update_book,1,"","Roman","Autor")
    assert raises(RepositoryError,controller.update_book,9,"Titlu","Roman","Autor")
    assert controller.get_book(1).get_title()=="Ion (ed. 2)"

def test_update_client():
    controller=make_filled_controller()
    controller.update_client(1,"Popescu Ioan",CNP1)
    assert controller.get_client(1).get_name()=="Popescu Ioan"
    controller.update_client(1,"Popescu Ioan",CNP3)
    assert controller.get_client(1).get_cnp()==CNP3
    assert raises(ValidationError,controller.update_client,1,"Popescu Ioan","123")
    assert raises(RepositoryError,controller.update_client,1,"Popescu Ioan",CNP2)
    assert raises(RepositoryError,controller.update_client,9,"Vasilescu Ana",CNP1)

def test_delete_book():
    controller=make_filled_controller()
    book=controller.delete_book(1)
    assert book.get_title()=="Ion"
    assert len(controller.get_books())==1
    assert raises(RepositoryError,controller.delete_book,1)
    assert raises(ValidationError,controller.delete_book,0)
    controller.rent_book(1,2)
    assert raises(ControllerError,controller.delete_book,2)
    assert len(controller.get_books())==1
    controller.return_book(2)
    controller.delete_book(2)
    assert controller.get_books()==[]

def test_delete_client():
    controller=make_filled_controller()
    controller.rent_book(1,1)
    assert raises(ControllerError,controller.delete_client,1)
    assert len(controller.get_clients())==2
    controller.return_book(1)
    client=controller.delete_client(1)
    assert client.get_name()=="Popescu Ion"
    assert len(controller.get_clients())==1
    assert raises(RepositoryError,controller.delete_client,1)
    assert raises(ValidationError,controller.delete_client,"1")

def test_search():
    controller=make_filled_controller()
    assert len(controller.search_books("roman"))==0
    assert controller.search_books("sado")[0].get_id()==2
    assert len(controller.search_clients("ion"))==2
    assert controller.search_clients("maria")[0].get_id()==2
    assert controller.search_clients("nimic")==[]
    assert raises(ValidationError,controller.search_books,"")
    assert raises(ValidationError,controller.search_clients,"   ")

def test_rent_book():
    controller=make_filled_controller()
    rental=controller.rent_book(1,2)
    assert rental.get_client_id()==1
    assert rental.get_book_id()==2
    assert len(controller.get_active_rentals())==1
    assert raises(ControllerError,controller.rent_book,2,2)
    assert raises(RepositoryError,controller.rent_book,9,1)
    assert raises(RepositoryError,controller.rent_book,1,9)
    assert raises(ValidationError,controller.rent_book,0,1)
    assert raises(ValidationError,controller.rent_book,1,"a")
    controller.rent_book(2,1)
    assert len(controller.get_active_rentals())==2

def test_return_book():
    controller=make_filled_controller()
    assert raises(ControllerError,controller.return_book,1)
    controller.rent_book(1,1)
    rental=controller.return_book(1)
    assert rental.is_returned()
    assert controller.get_active_rentals()==[]
    assert raises(ControllerError,controller.return_book,1)
    assert raises(ValidationError,controller.return_book,0)
    controller.rent_book(2,1)
    assert controller.get_active_rentals()[0].get_client_id()==2

def test_delete_removes_rental_history():
    controller=make_filled_controller()
    controller.rent_book(1,1)
    controller.return_book(1)
    controller.delete_book(1)
    controller.add_book(1,"Alta","Alta carte","Alt autor")
    controller.rent_book(2,1)
    assert len(controller.get_active_rentals())==1

def make_report_controller():
    controller=make_controller()
    controller.add_book(1,"Ion","Roman rural","Liviu Rebreanu")
    controller.add_book(2,"Baltagul","Roman despre un cioban","Mihail Sadoveanu")
    controller.add_book(3,"Alta","Descriere","Autor")
    controller.add_client(1,"Popescu Ion",CNP1)
    controller.add_client(2,"Ionescu Maria",CNP2)
    controller.add_client(3,"Zamfir Ana",CNP3)
    controller.rent_book(1,1)
    controller.return_book(1)
    controller.rent_book(2,1)
    controller.return_book(1)
    controller.rent_book(1,2)
    controller.return_book(2)
    controller.rent_book(1,1)
    controller.rent_book(2,2)
    return controller

def test_top_count():
    assert top_count(0,20)==0
    assert top_count(1,20)==1
    assert top_count(5,20)==1
    assert top_count(6,20)==2
    assert top_count(10,20)==2
    assert top_count(11,20)==3
    assert top_count(10,50)==5

def test_most_rented_books():
    controller=make_controller()
    assert controller.get_most_rented_books()==[]
    controller=make_report_controller()
    books=controller.get_most_rented_books()
    assert len(books)==2
    assert books[0][0].get_title()=="Ion"
    assert books[0][1]==3
    assert books[1][0].get_title()=="Baltagul"
    assert books[1][1]==2

def test_most_rented_books_tie():
    controller=make_report_controller()
    controller.return_book(2)
    controller.rent_book(1,2)
    books=controller.get_most_rented_books()
    assert books[0][0].get_title()=="Baltagul"
    assert books[0][1]==3
    assert books[1][0].get_title()=="Ion"
    assert books[1][1]==3
    controller.return_book(2)
    controller.rent_book(2,2)
    books=controller.get_most_rented_books()
    assert books[0][0].get_title()=="Baltagul"
    assert books[0][1]==4
    assert books[1][0].get_title()=="Ion"

def test_clients_by_name():
    controller=make_controller()
    assert controller.get_clients_by_name()==[]
    controller=make_report_controller()
    clients=controller.get_clients_by_name()
    assert len(clients)==2
    assert clients[0][0].get_name()=="Ionescu Maria"
    assert clients[0][1]==2
    assert clients[0][2]==1
    assert clients[1][0].get_name()=="Popescu Ion"
    assert clients[1][1]==3
    assert clients[1][2]==1

def test_clients_by_rentals():
    controller=make_report_controller()
    clients=controller.get_clients_by_rentals()
    assert len(clients)==2
    assert clients[0][0].get_name()=="Popescu Ion"
    assert clients[1][0].get_name()=="Ionescu Maria"
    controller.rent_book(3,3)
    controller.return_book(3)
    controller.rent_book(3,3)
    clients=controller.get_clients_by_rentals()
    assert len(clients)==3
    assert clients[1][0].get_name()=="Ionescu Maria"
    assert clients[2][0].get_name()=="Zamfir Ana"
    controller.return_book(3)
    controller.rent_book(3,3)
    clients=controller.get_clients_by_rentals()
    assert clients[0][0].get_name()=="Popescu Ion"
    assert clients[1][0].get_name()=="Zamfir Ana"
    assert clients[2][0].get_name()=="Ionescu Maria"

def test_most_active_clients():
    controller=make_controller()
    assert controller.get_most_active_clients()==[]
    controller=make_report_controller()
    top=controller.get_most_active_clients()
    assert len(top)==1
    assert top[0][0].get_name()=="Popescu Ion"
    assert top[0][1]==3

def test_never_rented():
    controller=make_controller()
    assert controller.get_never_rented()==([],[])
    controller=make_filled_controller()
    books,clients=controller.get_never_rented()
    assert [book.get_id() for book in books]==[1,2]
    assert [client.get_id() for client in clients]==[1,2]
    controller.rent_book(1,1)
    books,clients=controller.get_never_rented()
    assert [book.get_id() for book in books]==[2]
    assert [client.get_id() for client in clients]==[2]
    controller.return_book(1)
    books,clients=controller.get_never_rented()
    assert [book.get_id() for book in books]==[2]
    assert [client.get_id() for client in clients]==[2]

def test_never_rented_after_deletion():
    controller=make_filled_controller()
    controller.rent_book(1,1)
    controller.return_book(1)
    controller.delete_client(1)
    controller.add_client(1,"Alt Client",CNP1)
    books,clients=controller.get_never_rented()
    assert [book.get_id() for book in books]==[2]
    assert [client.get_id() for client in clients]==[2,1]

    controller.rent_book(1,1)
    controller.return_book(1)
    controller.delete_book(1)
    controller.add_book(1,"Alta","Descriere","Autor")
    books,clients=controller.get_never_rented()
    assert [book.get_id() for book in books]==[2,1]
    assert [client.get_id() for client in clients]==[2]

def test_console_never_rented():
    console=Console(make_filled_controller())
    with patch("builtins.print") as print_mock:
        console.run_command("19")
    output="\n".join(str(call.args[0]) for call in print_mock.call_args_list if call.args)
    assert "Cărți care nu au fost niciodată închiriate:" in output
    assert "Ion" in output
    assert "Clienți care nu au închiriat niciodată o carte:" in output
    assert "Popescu Ion" in output

def test_reports_from_sample_data():
    controller=make_controller()
    controller.load_sample_data(5)
    books=controller.get_most_rented_books()
    assert sum(count for _,count in books)==5
    clients=controller.get_clients_by_name()
    assert sum(total for _,total,_ in clients)==5
    clients=controller.get_clients_by_rentals()
    assert sum(total for _,total,_ in clients)==5
    top=controller.get_most_active_clients()
    assert len(top)<=len(clients)

# Rularea Testelor

def run_all_tests():
    test_validate_id()
    test_validate_text()
    test_validate_name()
    test_validate_cnp()
    test_create_book()
    test_create_client()
    test_create_rental()
    test_repository_add()
    test_repository_find_and_get_all()
    test_client_repository()
    test_repository_get_remove_update()
    test_client_repository_update()
    test_book_search()
    test_client_search()
    test_rental_repository()
    test_rental_counts()
    test_add_book()
    test_add_client()
    test_get_all_empty()
    test_load_sample_data()
    test_load_sample_data_with_existing()
    test_load_sample_data_reuses_book_safely()
    test_console_load_sample_data_reads_count()
    test_get_book_and_client()
    test_update_book()
    test_update_client()
    test_delete_book()
    test_delete_client()
    test_search()
    test_rent_book()
    test_return_book()
    test_delete_removes_rental_history()
    test_top_count()
    test_most_rented_books()
    test_most_rented_books_tie()
    test_clients_by_name()
    test_clients_by_rentals()
    test_most_active_clients()
    test_never_rented()
    test_never_rented_after_deletion()
    test_console_never_rented()
    test_reports_from_sample_data()
    print("Toate testele au trecut cu succes!")