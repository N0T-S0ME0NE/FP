from .domeniu import ValidationError
from .repository import RepositoryError

# Citire și Afișare

def read_int(prompt):
    text=input(prompt).strip()
    try:
        return int(text)
    except ValueError:
        raise ValidationError("'"+text+"' nu este un număr întreg")

def read_text(prompt):
    return input(prompt).strip()

def print_books(books):
    if len(books)==0:
        print("Nu există cărți.")
        return
    for book in books:
        print("  ID %3d | %s | %s" % (book.get_id(),book.get_title(),book.get_author()))
        print("         "+book.get_description())
    print("Total cărți: "+str(len(books)))

def print_clients(clients):
    if len(clients)==0:
        print("Nu există clienți.")
        return
    for client in clients:
        print("  ID %3d | %-25s | CNP %s" % (client.get_id(),client.get_name(),client.get_cnp()))
    print("Total clienți: "+str(len(clients)))

def print_menu():
    print("""
--- Bibliotecă ---
 1. Adaugă o carte
 2. Afișează cărțile
 3. Adaugă un client
 4. Afișează clienții
 5. Încarcă date de test
 0. Ieșire""")

class Console:
    def __init__(self,controller):
        self._controller=controller

    def ui_add_book(self):
        book_id=read_int("ID: ")
        title=read_text("Titlu: ")
        description=read_text("Descriere: ")
        author=read_text("Autor: ")
        self._controller.add_book(book_id,title,description,author)
        print("Carte adăugată.")

    def ui_print_books(self):
        print_books(self._controller.get_books())

    def ui_add_client(self):
        client_id=read_int("ID: ")
        name=read_text("Nume: ")
        cnp=read_text("CNP: ")
        self._controller.add_client(client_id,name,cnp)
        print("Client adăugat.")

    def ui_print_clients(self):
        print_clients(self._controller.get_clients())

    def ui_load_sample_data(self):
        books,clients=self._controller.load_sample_data()
        print("Au fost adăugate "+str(books)+" cărți și "+str(clients)+" clienți de test.")

    def run_command(self,command):
        match command:
            case "1":
                self.ui_add_book()
            case "2":
                self.ui_print_books()
            case "3":
                self.ui_add_client()
            case "4":
                self.ui_print_clients()
            case "5":
                self.ui_load_sample_data()
            case _:
                print("Eroare: comandă invalidă")

    def run(self):
        finished=0
        while not finished:
            print_menu()
            try:
                command=input("Comandă: ").strip()
                if command=="0":
                    finished=1
                else:
                    self.run_command(command)
            except (ValidationError,RepositoryError) as error:
                print("Eroare: "+str(error))
            except EOFError:
                finished=1
        print("Programul se va închide...")