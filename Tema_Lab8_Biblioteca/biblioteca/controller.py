from .domeniu import MAX_TEXT,validate_id,validate_text,create_book,create_client,create_rental
from .repository import RepositoryError

class ControllerError(Exception):
    pass

# Date de test: (id, titlu, descriere, autor) și (id, nume, CNP)
SAMPLE_BOOKS=(
    (1,"Ion","Roman despre viața satului ardelenesc","Liviu Rebreanu"),
    (2,"Moara cu noroc","Nuvelă despre dorința de îmbogățire","Ioan Slavici"),
    (3,"Enigma Otiliei","Roman realist despre o familie de burghezi","George Călinescu"),
    (4,"Baltagul","Roman despre căutarea unui cioban dispărut","Mihail Sadoveanu"),
    (5,"Maitreyi","Roman autobiografic despre o poveste de dragoste","Mircea Eliade"),
)
SAMPLE_CLIENTS=(
    (1,"Popescu Ion","5031114121014"),
    (2,"Ionescu Maria","6040308402156"),
    (3,"Georgescu Andrei","1980723354322"),
    (4,"Dumitru Elena","2991201061183"),
)

class Controller:
    def __init__(self,book_repo,client_repo,rental_repo):
        self._book_repo=book_repo
        self._client_repo=client_repo
        self._rental_repo=rental_repo

    # Cărți

    def add_book(self,book_id,title,description,author):
        book=create_book(book_id,title,description,author)
        self._book_repo.add(book)
        return book

    def get_books(self):
        return self._book_repo.get_all()

    def get_book(self,book_id):
        validate_id(book_id)
        return self._book_repo.get(book_id)

    def update_book(self,book_id,title,description,author):
        book=create_book(book_id,title,description,author)
        self._book_repo.update(book)
        return book

    def delete_book(self,book_id):
        validate_id(book_id)
        self._book_repo.get(book_id)
        if self._rental_repo.find_active_by_book(book_id) is not None:
            raise ControllerError("Cartea este închiriată și nu poate fi ștearsă")
        book=self._book_repo.remove(book_id)
        self._rental_repo.remove_by_book(book_id)
        return book

    def search_books(self,text):
        validate_text(text,"Textul căutat",MAX_TEXT)
        return self._book_repo.search(text)

    # Clienți

    def add_client(self,client_id,name,cnp):
        client=create_client(client_id,name,cnp)
        self._client_repo.add(client)
        return client

    def get_clients(self):
        return self._client_repo.get_all()

    def get_client(self,client_id):
        validate_id(client_id)
        return self._client_repo.get(client_id)

    def update_client(self,client_id,name,cnp):
        client=create_client(client_id,name,cnp)
        self._client_repo.update(client)
        return client

    def delete_client(self,client_id):
        validate_id(client_id)
        self._client_repo.get(client_id)
        if len(self._rental_repo.get_active_by_client(client_id))>0:
            raise ControllerError("Clientul are cărți nereturnate și nu poate fi șters")
        client=self._client_repo.remove(client_id)
        self._rental_repo.remove_by_client(client_id)
        return client

    def search_clients(self,text):
        validate_text(text,"Textul căutat",MAX_TEXT)
        return self._client_repo.search(text)

    # Închirieri

    def rent_book(self,client_id,book_id):
        rental=create_rental(client_id,book_id)
        self._client_repo.get(client_id)
        self._book_repo.get(book_id)
        if self._rental_repo.find_active_by_book(book_id) is not None:
            raise ControllerError("Cartea este deja închiriată")
        self._rental_repo.add(rental)
        return rental

    def return_book(self,book_id):
        validate_id(book_id)
        rental=self._rental_repo.find_active_by_book(book_id)
        if rental is None:
            raise ControllerError("Cartea cu ID-ul "+str(book_id)+" nu este închiriată")
        rental.mark_returned()
        return rental

    def get_active_rentals(self):
        return self._rental_repo.get_active()

    # Date de test

    def load_sample_data(self):
        books=0
        clients=0
        for book_id,title,description,author in SAMPLE_BOOKS:
            try:
                self.add_book(book_id,title,description,author)
                books+=1
            except RepositoryError:
                pass
        for client_id,name,cnp in SAMPLE_CLIENTS:
            try:
                self.add_client(client_id,name,cnp)
                clients+=1
            except RepositoryError:
                pass
        return (books,clients)