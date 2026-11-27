from .domeniu import ValidationError
from .repository import RepositoryError
from .controller import ControllerError

# Citire și Afișare

def read_int(prompt):
    text=input(prompt).strip()
    try:
        return int(text)
    except ValueError:
        raise ValidationError("'"+text+"' nu este un număr întreg")

def read_text(prompt):
    return input(prompt).strip()

def read_optional(prompt,current):
    text=input(prompt+" (Enter = "+current+"): ").strip()
    if text=="":
        return current
    return text

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

def print_book_stats(stats):
    if len(stats)==0:
        print("Nu există închirieri.")
        return
    for i in range(len(stats)):
        book,count=stats[i]
        print("  %2d. %s | %s | închirieri: %d" % (i+1,book.get_title(),book.get_author(),count))

def print_client_stats(stats):
    if len(stats)==0:
        print("Nu există închirieri.")
        return
    for i in range(len(stats)):
        client,total,active=stats[i]
        print("  %2d. %-25s | închirieri: %d | în prezent: %d" % (i+1,client.get_name(),total,active))

def print_menu():
    print("""
--- Bibliotecă ---

 Cărți                            Clienți
  1. Adaugă                        6. Adaugă
  2. Afișează                      7. Afișează
  3. Modifică                      8. Modifică
  4. Șterge                        9. Șterge
  5. Caută                        10. Caută

 Închirieri                       Rapoarte
 11. Închiriază o carte           15. Cele mai închiriate cărți
 12. Returnează o carte           16. Clienți, ordonați după nume
 13. Cărți închiriate acum        17. Clienți, ordonați după număr
                                  18. Primii 20% clienți activi
 14. Încarcă date aleatoriu       19. Cărți și clienți fără închirieri
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
        n=read_int("Numărul de date de generat (n): ")
        books,clients,rentals=self._controller.load_sample_data(n)
        print("Au fost adăugate "+str(books)+" cărți, "+str(clients)+" clienți și închirieri de test.")

    def ui_update_book(self):
        book=self._controller.get_book(read_int("ID-ul cărții de modificat: "))
        title=read_optional("Titlu nou",book.get_title())
        description=read_optional("Descriere nouă",book.get_description())
        author=read_optional("Autor nou",book.get_author())
        self._controller.update_book(book.get_id(),title,description,author)
        print("Carte modificată.")

    def ui_delete_book(self):
        book=self._controller.delete_book(read_int("ID-ul cărții de șters: "))
        print("Cartea '"+book.get_title()+"' a fost ștearsă.")

    def ui_search_books(self):
        books=self._controller.search_books(read_text("Caută (titlu, autor sau ID): "))
        if len(books)==0:
            print("Nu s-a găsit nicio carte.")
        else:
            print_books(books)

    def ui_update_client(self):
        client=self._controller.get_client(read_int("ID-ul clientului de modificat: "))
        name=read_optional("Nume nou",client.get_name())
        cnp=read_optional("CNP nou",client.get_cnp())
        self._controller.update_client(client.get_id(),name,cnp)
        print("Client modificat.")

    def ui_delete_client(self):
        client=self._controller.delete_client(read_int("ID-ul clientului de șters: "))
        print("Clientul '"+client.get_name()+"' a fost șters.")

    def ui_search_clients(self):
        clients=self._controller.search_clients(read_text("Caută (Nume sau CNP): "))
        if len(clients)==0:
            print("Nu s-a găsit niciun client.")
        else:
            print_clients(clients)

    def ui_rent_book(self):
        client_id=read_int("ID client: ")
        book_id=read_int("ID carte: ")
        rental=self._controller.rent_book(client_id,book_id)
        client=self._controller.get_client(rental.get_client_id())
        book=self._controller.get_book(rental.get_book_id())
        print("Cartea '"+book.get_title()+"' a fost închiriată de "+client.get_name()+".")

    def ui_return_book(self):
        rental=self._controller.return_book(read_int("ID carte: "))
        book=self._controller.get_book(rental.get_book_id())
        print("Cartea '"+book.get_title()+"' a fost returnată.")

    def ui_print_rentals(self):
        rentals=self._controller.get_active_rentals()
        if len(rentals)==0:
            print("Nu există cărți închiriate.")
            return
        for rental in rentals:
            client=self._controller.get_client(rental.get_client_id())
            book=self._controller.get_book(rental.get_book_id())
            print("  Carte ID %3d | %s -> client ID %3d | %s" % (book.get_id(),book.get_title(),client.get_id(),client.get_name()))
        print("Total cărți închiriate: "+str(len(rentals)))

    def ui_report_books(self):
        print("Cele mai închiriate cărți:")
        print_book_stats(self._controller.get_most_rented_books())

    def ui_report_clients_by_name(self):
        print("Clienți cu cărți închiriate, ordonați după nume:")
        print_client_stats(self._controller.get_clients_by_name())

    def ui_report_clients_by_rentals(self):
        print("Clienți cu cărți închiriate, ordonați după numărul de cărți închiriate:")
        print_client_stats(self._controller.get_clients_by_rentals())

    def ui_report_top_clients(self):
        print("Primii 20% dintre cei mai activi clienți:")
        print_client_stats(self._controller.get_most_active_clients())

    def ui_report_never_rented(self):
        books,clients=self._controller.get_never_rented()
        print("Cărți care nu au fost niciodată închiriate:")
        print_books(books)
        print("Clienți care nu au închiriat niciodată o carte:")
        print_clients(clients)

    def run_command(self,command):
        match command:
            case "1":
                self.ui_add_book()
            case "2":
                self.ui_print_books()
            case "3":
                self.ui_update_book()
            case "4":
                self.ui_delete_book()
            case "5":
                self.ui_search_books()
            case "6":
                self.ui_add_client()
            case "7":
                self.ui_print_clients()
            case "8":
                self.ui_update_client()
            case "9":
                self.ui_delete_client()
            case "10":
                self.ui_search_clients()
            case "11":
                self.ui_rent_book()
            case "12":
                self.ui_return_book()
            case "13":
                self.ui_print_rentals()
            case "14":
                self.ui_load_sample_data()
            case "15":
                self.ui_report_books()
            case "16":
                self.ui_report_clients_by_name()
            case "17":
                self.ui_report_clients_by_rentals()
            case "18":
                self.ui_report_top_clients()
            case "19":
                self.ui_report_never_rented()
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
            except (ValidationError,RepositoryError,ControllerError) as error:
                print("Eroare: "+str(error))
            except EOFError:
                finished=1
        print("Programul se va închide...")