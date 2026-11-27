import calendar
import random
from .domeniu import MAX_TEXT,CNP_WEIGHTS,ValidationError,validate_id,validate_text,create_book,create_client,create_rental

class ControllerError(Exception):
    pass

BOOK_TITLE_PATTERNS=(
    ("Amurgul",("zorilor","serii","nopții")),
    ("Cântecul",("Poienii","codrului","mării","izvorului")),
    ("Umbra",("codrului","nopții","munților","trecutului")),
    ("Povestea",("copilăriei","satului","călătorului","mării")),
    ("Visul",("poetului","copilului","călătorului","primăverii")),
    ("Șoapta",("vântului","pădurii","izvorului","nopții")),
    ("Chemarea",("munților","mării","străbunilor","libertății")),
    ("Floarea",("soarelui","câmpului","grădinii","tinereții")),
    ("Taina",("castelului","pădurii","trecutului","lacului")),
    ("Răsăritul",("speranței","soarelui","vieții")),
)
BOOK_TYPES=("Nuvelă","Roman","Poezie","Schiță","Povestire","Basm","Dramă","Eseu")
FIRST_NAMES=("Ana","Andrei","Elena","Ioana","Maria","Mihai","Radu","Cristian","Teodora","Vlad")
SURNAMES=("Dumitrescu","Georgescu","Ionescu","Marin","Popa","Popescu","Radu","Stan","Vasilescu","Zamfir")
AUTHOR_FIRST_NAMES=("Alin","Cătălin","Daria","Emil","Florin","Irina","Laurențiu","Oana","Sorin","Veronica")
AUTHOR_SURNAMES=("Bălan","Bărbulescu","Cernat","Dobre","Enache","Filip","Grigorescu","Iliescu","Lupu","Matei")
TOP_PERCENT=20

def generate_author(existing_authors):
    while True:
        first_name=random.choice(AUTHOR_FIRST_NAMES)
        surnames=random.sample(AUTHOR_SURNAMES,len(AUTHOR_SURNAMES))
        author=first_name+" "+surnames[0]
        if author not in existing_authors:
            return author
        for surname in surnames[1:]:
            candidate=author+"-"+surname
            if len(candidate)>MAX_TEXT:
                break
            author=candidate
            if author not in existing_authors:
                return author

def generate_cnp(existing_cnps):
    while True:
        sex=random.choice((1,2,5,6))
        if sex in (1,2):
            year=random.randint(30,99)
            full_year=1900+year
        else:
            year=random.randint(0,26)
            full_year=2000+year
        month=random.randint(1,12)
        day=random.randint(1,calendar.monthrange(full_year,month)[1])
        county=random.randint(1,52)
        serial=random.randint(1,999)
        base="%d%02d%02d%02d%02d%03d" % (sex,year,month,day,county,serial)
        control=sum(int(base[i])*int(CNP_WEIGHTS[i]) for i in range(12))%11
        if control==10:
            control=1
        cnp=base+str(control)
        if cnp not in existing_cnps:
            return cnp

# Funcții pentru rapoarte

def top_count(total,percent):
    return (total*percent+99)//100

def key_books(entry):
    return (-entry[1],entry[0].get_title().lower())

def key_name(entry):
    return (entry[0].get_name().lower(),entry[0].get_id())

def key_count(entry):
    return (-entry[1],entry[0].get_name().lower(),entry[0].get_id())

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

    # Rapoarte

    def get_most_rented_books(self):
        result=[]
        for book in self._book_repo.get_all():
            count=self._rental_repo.count_by_book(book.get_id())
            if count>0:
                result.append((book,count))
        return sorted(result,key=key_books)

    def get_clients_with_rentals(self):
        result=[]
        for client in self._client_repo.get_all():
            total=self._rental_repo.count_by_client(client.get_id())
            if total>0:
                active=len(self._rental_repo.get_active_by_client(client.get_id()))
                result.append((client,total,active))
        return result

    def get_clients_by_name(self):
        return sorted(self.get_clients_with_rentals(),key=key_name)

    def get_clients_by_rentals(self):
        return sorted(self.get_clients_with_rentals(),key=key_count)

    def get_most_active_clients(self):
        clients=self.get_clients_by_rentals()
        return clients[:top_count(len(clients),TOP_PERCENT)]

    def get_never_rented(self):
        books=[]
        for book in self._book_repo.get_all():
            if not self._rental_repo.has_rented_book(book.get_id()):
                books.append(book)
        clients=[]
        for client in self._client_repo.get_all():
            if not self._rental_repo.has_client_rentals(client.get_id()):
                clients.append(client)
        return (books,clients)

    # Date de test

    def load_sample_data(self,n):
        if not isinstance(n,int) or isinstance(n,bool) or n<0:
            raise ValidationError("Numărul de date trebuie să fie un număr întreg nenegativ")
        if n==0:
            return (0,0,0)

        book_ids=[]
        next_book_id=max([book.get_id() for book in self._book_repo.get_all()]+[0])+1
        existing_authors={book.get_author() for book in self._book_repo.get_all()}
        for offset in range(n):
            title_start,title_endings=random.choice(BOOK_TITLE_PATTERNS)
            title=title_start+" "+random.choice(title_endings)
            description=random.choice(BOOK_TYPES)
            author=generate_author(existing_authors)
            book_id=next_book_id+offset
            self.add_book(book_id,title,description,author)
            book_ids.append(book_id)
            existing_authors.add(author)

        client_ids=[]
        next_client_id=max([client.get_id() for client in self._client_repo.get_all()]+[0])+1
        existing_cnps={client.get_cnp() for client in self._client_repo.get_all()}
        for offset in range(n):
            name=random.choice(FIRST_NAMES)+" "+random.choice(SURNAMES)
            client_id=next_client_id+offset
            cnp=generate_cnp(existing_cnps)
            self.add_client(client_id,name,cnp)
            client_ids.append(client_id)
            existing_cnps.add(cnp)

        for _ in range(n):
            book_id=random.choice(book_ids)
            if self._rental_repo.find_active_by_book(book_id) is not None:
                self.return_book(book_id)
            self.rent_book(random.choice(client_ids),book_id)
            if random.choice((True,False)):
                self.return_book(book_id)
        return (n,n,n)