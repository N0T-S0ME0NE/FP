class RepositoryError(Exception):
    pass

class Repository:
    def __init__(self,label):
        self._items=[]
        self._label=label

    def add(self,item):
        if self.find_by_id(item.get_id()) is not None:
            raise RepositoryError("Există deja "+self._label+" cu ID-ul "+str(item.get_id()))
        self._items.append(item)

    def find_by_id(self,item_id):
        for item in self._items:
            if item.get_id()==item_id:
                return item
        return None

    def get(self,item_id):
        item=self.find_by_id(item_id)
        if item is None:
            raise RepositoryError("Nu există "+self._label+" cu ID-ul "+str(item_id))
        return item

    def remove(self,item_id):
        item=self.get(item_id)
        self._items.remove(item)
        return item

    def update(self,new_item):
        old_item=self.get(new_item.get_id())
        self._items[self._items.index(old_item)]=new_item

    def get_all(self):
        return self._items[:]

    def size(self):
        return len(self._items)

class BookRepository(Repository):
    def __init__(self):
        super().__init__("o carte")

    def search(self,text):
        text=text.strip().lower()
        result=[]
        for book in self._items:
            if text in book.get_title().lower() or text in book.get_author().lower() or text==str(book.get_id()):
                result.append(book)
        return result

class ClientRepository(Repository):
    def __init__(self):
        super().__init__("un client")

    def find_by_cnp(self,cnp):
        for client in self._items:
            if client.get_cnp()==cnp:
                return client
        return None

    def add(self,client):
        if self.find_by_cnp(client.get_cnp()) is not None:
            raise RepositoryError("Există deja un client cu CNP-ul "+client.get_cnp())
        super().add(client)

    def update(self,client):
        self.get(client.get_id())
        other=self.find_by_cnp(client.get_cnp())
        if other is not None and other.get_id()!=client.get_id():
            raise RepositoryError("Există deja un client cu CNP-ul "+client.get_cnp())
        super().update(client)

    def search(self,text):
        text=text.strip().lower()
        result=[]
        for client in self._items:
            if text in client.get_name().lower() or text in client.get_cnp() or text==str(client.get_id()):
                result.append(client)
        return result

class RentalRepository:
    def __init__(self):
        self._rentals=[]
        self._rented_book_ids=set()
        self._client_ids_with_rentals=set()

    def add(self,rental):
        self._rentals.append(rental)
        self._rented_book_ids.add(rental.get_book_id())
        self._client_ids_with_rentals.add(rental.get_client_id())

    def has_rented_book(self,book_id):
        return book_id in self._rented_book_ids

    def has_client_rentals(self,client_id):
        return client_id in self._client_ids_with_rentals

    def find_active_by_book(self,book_id):
        for rental in self._rentals:
            if rental.get_book_id()==book_id and not rental.is_returned():
                return rental
        return None

    def get_active(self):
        result=[]
        for rental in self._rentals:
            if not rental.is_returned():
                result.append(rental)
        return result

    def get_active_by_client(self,client_id):
        result=[]
        for rental in self.get_active():
            if rental.get_client_id()==client_id:
                result.append(rental)
        return result

    def count_by_book(self,book_id):
        count=0
        for rental in self._rentals:
            if rental.get_book_id()==book_id:
                count+=1
        return count

    def count_by_client(self,client_id):
        count=0
        for rental in self._rentals:
            if rental.get_client_id()==client_id:
                count+=1
        return count

    def get_all(self):
        return self._rentals[:]

    def remove_by_book(self,book_id):
        kept=[]
        for rental in self._rentals:
            if rental.get_book_id()!=book_id:
                kept.append(rental)
        self._rentals=kept
        self._rented_book_ids.discard(book_id)

    def remove_by_client(self,client_id):
        kept=[]
        for rental in self._rentals:
            if rental.get_client_id()!=client_id:
                kept.append(rental)
        self._rentals=kept
        self._client_ids_with_rentals.discard(client_id)