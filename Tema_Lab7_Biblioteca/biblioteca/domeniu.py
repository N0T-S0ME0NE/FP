MAX_TEXT=100
MAX_DESCRIPTION=300
CNP_WEIGHTS="279146358279"

class ValidationError(Exception):
    pass

# Validări

def validate_id(item_id):
    if not isinstance(item_id,int) or isinstance(item_id,bool) or item_id<=0:
        raise ValidationError("ID-ul trebuie să fie un număr întreg pozitiv")

def validate_text(text,field,max_length):
    if not isinstance(text,str) or text.strip()=="":
        raise ValidationError(field+" nu poate fi vid")
    if len(text.strip())>max_length:
        raise ValidationError(field+" nu poate avea mai mult de "+str(max_length)+" caractere")

def validate_name(name):
    validate_text(name,"Numele",MAX_TEXT)
    if not name.strip().replace(" ","").replace("-","").isalpha():
        raise ValidationError("Numele poate conține doar litere, spații și cratime")

def validate_cnp(cnp):
    if not isinstance(cnp,str) or len(cnp)!=13 or not cnp.isascii() or not cnp.isdigit():
        raise ValidationError("CNP-ul trebuie să aibă exact 13 cifre")
    month=int(cnp[3:5])
    day=int(cnp[5:7])
    if cnp[0]=="0" or month<1 or month>12 or day<1 or day>31:
        raise ValidationError("CNP-ul conține o dată de naștere invalidă")
    total=0
    for i in range(12):
        total+=int(cnp[i])*int(CNP_WEIGHTS[i])
    control=total%11
    if control==10:
        control=1
    if control!=int(cnp[12]):
        raise ValidationError("CNP-ul are cifra de control greșită")

# Entități

class Book:
    def __init__(self,book_id,title,description,author):
        self._id=book_id
        self._title=title
        self._description=description
        self._author=author

    def get_id(self):
        return self._id

    def get_title(self):
        return self._title

    def get_description(self):
        return self._description

    def get_author(self):
        return self._author

class Client:
    def __init__(self,client_id,name,cnp):
        self._id=client_id
        self._name=name
        self._cnp=cnp

    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_cnp(self):
        return self._cnp

# Crearea unei cărți și a unui client

def create_book(book_id,title,description,author):
    validate_id(book_id)
    validate_text(title,"Titlul",MAX_TEXT)
    validate_text(description,"Descrierea",MAX_DESCRIPTION)
    validate_text(author,"Autorul",MAX_TEXT)
    return Book(book_id,title.strip(),description.strip(),author.strip())

def create_client(client_id,name,cnp):
    validate_id(client_id)
    validate_name(name)
    validate_cnp(cnp)
    return Client(client_id,name.strip(),cnp)