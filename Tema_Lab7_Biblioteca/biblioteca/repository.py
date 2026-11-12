class RepositoryError(Exception):
    pass

class Repository:
    def __init__(self,label):
        self._items=[]
        self._label=label

    def add(self,item):
        if self.find_by_id(item.get_id()) is not None:
            raise RepositoryError("Există deja " + self._label + " cu ID-ul " + str(item.get_id()))
        self._items.append(item)

    def find_by_id(self,item_id):
        for item in self._items:
            if item.get_id()==item_id:
                return item
        return None

    def get_all(self):
        return self._items[:]

    def size(self):
        return len(self._items)

class BookRepository(Repository):
    def __init__(self):
        super().__init__("o carte")

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
            raise RepositoryError("Există deja un client cu CNP-ul " + client.get_cnp())
        super().add(client)