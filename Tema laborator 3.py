def este_strict_crescator(secventa):
    if len(secventa) <= 1:
        return True
    
    for i in range(len(secventa) - 1):
        if secventa[i] >= secventa[i + 1]:
            return False
    return True

def toate_egale(secventa):
    if len(secventa) <= 1:
        return True
    
    for i in range(1, len(secventa)):
        if secventa[i] != secventa[0]:
            return False
    return True

def gaseste_secventa_maxima(lista, functie_verificare):
    if not lista:
        return []
    secventa_maxima = []
    for i in range(len(lista)):
        for j in range(i, len(lista)):
            sub_lista = lista[i : j + 1]
            if functie_verificare(sub_lista):
                if len(sub_lista) > len(secventa_maxima):
                    secventa_maxima = sub_lista
    return secventa_maxima

def citeste_lista():
    linie = input("Introduceți numerele separate prin spațiu: ")
    numere = [int(x) for x in linie.split()]
    return numere

def afiseaza_meniu():
    print("\n--- MENIU ---")
    print("1. Citirea unei liste de numere intregi")
    print("2. Gasirea secventei maxime de elemente strict crescatoare (Proprietatea 1)")
    print("3. Gasirea secventei maxime de elemente egale (Proprietatea 5)")
    print("4. Iesire din aplicatie")


def main():
    lista_curenta = []
    while True:
        afiseaza_meniu()
        optiune = input("Alegeți opțiunea (1-4): ")
        match optiune:
            case "1":
                lista_curenta = citeste_lista()
                print(f"Lista citită cu succes: {lista_curenta}")
            case "2":
                if not lista_curenta:
                    print("Eroare: Lista este goală! Citiți mai întâi lista (opțiunea 1).")
                else:
                    rezultat = gaseste_secventa_maxima(lista_curenta, este_strict_crescator)
                    print(f"Secvența maximă strict crescătoare este: {rezultat}")
            case "3":
                if not lista_curenta:
                    print("Eroare: Lista este goală! Citiți mai întâi lista (opțiunea 1).")
                else:
                    rezultat = gaseste_secventa_maxima(lista_curenta, toate_egale)
                    print(f"Secvența maximă de elemente egale este: {rezultat}")
            case "4":
                print("Aplicația se închide. La revedere!")
                break
            case _:
                print("Opțiune invalidă! Vă rugăm să alegeți un număr între 1 și 4.")
main()