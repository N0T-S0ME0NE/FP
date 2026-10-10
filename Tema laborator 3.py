def P1(V):
    if len(V)<2:
        return True
    for i in range(0,len(V)-1):
        if V[i]>=V[i+1]:
            return False
    return True

def P9(V):
    if len(V)==1:
        return True
    if len(V)==2:
        return V[0]==V[1]
    for i in range(0,len(V)-2):
        a=V[i]
        b=V[i+1]
        c=V[i+2]
        if a!=b and b!=c and a!=c:
            return False
    return True

def secv_max(V,Proprietate):
    if not V:
        return []
    secv_mx=[]
    for i in range(0,len(V)):
        for j in range(i,len(V)):
            sub_list=V[i:j+1]
            if Proprietate(sub_list):
                if len(sub_list)>len(secv_mx):
                    secv_mx=sub_list
    return secv_mx

def citeste_lista():
    nr=input("Introduceți numerele separate prin spațiu: ")
    W=[int(x) for x in nr.split()]
    return W

def meniu():
    print("\n--- MENIU ---")
    print("1. Citirea unei liste de numere intregi")
    print("2. Gasirea secventei maxime strict crescatoare")
    print("3. Gasirea secventei maxime unde 3 elemente consecutive au o valoare care se repeta)")
    print("4. Iesire din aplicatie")

def main():
    V=[]
    while True:
        meniu()
        n=input("Alegeți o opțiune (1-4): ")
        match n:
            case "1":
                V=citeste_lista()
                print(f"Numerele ce vor fi prelucrate sunt: {V}")
            case "2":
                if not V:
                    print("Eroare: Lista este goală! Citiți mai întâi lista de numere!")
                else:
                    x = secv_max(V, P1)
                    print(f"Secvența maximă de numere strict crescătoare este: {x}")
            case "3":
                if not V:
                    print("Eroare: Lista este goală! Citiți mai întâi lista de numere!")
                else:
                    y = secv_max(V, P9)
                    print(f"Secvența maximă pentru o valoare care se repeta într-un șir de 3 elemente consecutive este: {y}")
            case "4":
                print("Programul se va închide...")
                break
            case _:
                print("Opțiune invalidă! Vă rugăm să alegeți un număr între 1 și 4.")
main()