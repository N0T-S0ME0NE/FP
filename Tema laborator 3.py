def este_strict_crescator(secventa):
    """Verifică dacă o secvență este strict crescătoare (Proprietatea 1)"""
    if len(secventa) <= 1:
        return True
    
    for i in range(len(secventa) - 1):
        if secventa[i] >= secventa[i + 1]:
            return False
    return True


def toate_egale(secventa):
    """Verifică dacă toate elementele din secvență sunt egale (Proprietatea 5)"""
    if len(secventa) <= 1:
        return True
    
    for i in range(1, len(secventa)):
        if secventa[i] != secventa[0]:
            return False
    return True


def gaseste_secventa_maxima(lista, functie_verificare):
    """
    Găsește secvența contiguă de lungime maximă din listă
    care respectă o anumită proprietate dată prin functie_verificare.
    """
    if not lista:
        return []

    secventa_maxima = []

    # Generăm toate subsecvențele posibile (de la i la j)
    for i in range(len(lista)):
        for j in range(i, len(lista)):
            sub_lista = lista[i : j + 1]
            
            # Verificăm dacă respectă proprietatea
            if functie_verificare(sub_lista):
                # Dacă este mai lungă decât ce am găsit până acum, o salvăm
                if len(sub_lista) > len(secventa_maxima):
                    secventa_maxima = sub_lista

    return secventa_maxima



def citeste_lista():
    """Citește de la tastatură o listă de numere întregi introduse pe o singură linie."""
    linie = input("Introduceți numerele separate prin spațiu: ")
    # Convertim fiecare element din text în număr întreg (int)
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

        if optiune == "1":
            lista_curenta = citeste_lista()
            print(f"Lista citită cu succes: {lista_curenta}")

        elif optiune == "2":
            if not lista_curenta:
                print("Eroare: Lista este goală! Citiți mai întâi lista (opțiunea 1).")
            else:
                rezultat = gaseste_secventa_maxima(lista_curenta, este_strict_crescator)
                print(f"Secvența maximă strict crescătoare este: {rezultat}")

        elif optiune == "3":
            if not lista_curenta:
                print("Eroare: Lista este goală! Citiți mai întâi lista (opțiunea 1).")
            else:
                rezultat = gaseste_secventa_maxima(lista_curenta, toate_egale)
                print(f"Secvența maximă de elemente egale este: {rezultat}")

        elif optiune == "4":
            print("Aplicatia se inchide. La revedere!")
            break

        else:
            print("Opțiune invalidă! Vă rugăm să alegeți un număr între 1 și 4.")


# Punctul de intrare în program
if __name__ == "__main__":
    main()