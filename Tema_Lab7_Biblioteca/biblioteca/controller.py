from .domeniu import create_book,create_client
from .repository import RepositoryError

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
    def __init__(self,book_repo,client_repo):
        self._book_repo=book_repo
        self._client_repo=client_repo

    # Cărți

    def add_book(self,book_id,title,description,author):
        book=create_book(book_id,title,description,author)
        self._book_repo.add(book)
        return book

    def get_books(self):
        return self._book_repo.get_all()

    # Clienți

    def add_client(self,client_id,name,cnp):
        client=create_client(client_id,name,cnp)
        self._client_repo.add(client)
        return client

    def get_clients(self):
        return self._client_repo.get_all()

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