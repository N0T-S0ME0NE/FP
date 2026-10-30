def cmmdc(a,b):
    while b>0:
        r=a%b
        a=b
        b=r
    return a

def P1(V):
    if len(V)<2:
        return True
    for i in range(0,len(V)-1):
        if V[i]>=V[i+1]:
            return False
    return True

def P3(V):
    if len(V)<2:
        return True
    for i in range(0,len(V)-1):
        if cmmdc(V[i],V[i+1])!=1:
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
    secv_mx=[V[0]]
    for i in range(0,len(V)):
        for j in range(i,len(V)):
            sub_list=V[i:j+1]
            if Proprietate(sub_list):
                if len(sub_list)>len(secv_mx):
                    secv_mx=sub_list
    return secv_mx

def teste():
    assert secv_max([2,4,6,3,5,7,9,1],P1)==[3,5,7,9]
    assert secv_max([5,4,3,2],P1)==[5]
    assert secv_max([1,3,2,4,6,8],P1)==[2,4,6,8]
    assert secv_max([7,7,7,7],P1)==[7]
    assert secv_max([1,2,3,4],P1)==[1,2,3,4]
    assert secv_max([9],P1)==[9]
    
    assert secv_max([1,1,2,3,3],P9)==[1,1,2]
    assert secv_max([1,2,3],P9)==[1]
    assert secv_max([5,12,9],P9)==[5]
    assert secv_max([4,4,4,4],P9)==[4,4,4,4]
    assert secv_max([8,8],P9)==[8,8]
    assert secv_max([8,9],P9)==[8]
    assert secv_max([1,2,1,3,3,4,3],P9)==[1,3,3,4,3]
    assert secv_max([1,2,3,4],P9)==[1]

    assert secv_max([2,3,5,7],P3)==[2,3,5,7]
    assert secv_max([2,4,3,5],P3)==[4,3,5]
    assert secv_max([6,9,4],P3)==[9,4]
    assert secv_max([10,15],P3)==[10]
    assert secv_max([7],P3)==[7]
    assert secv_max([2,15,4,10],P3)==[2,15,4]
    print("Toate testele automate au trecut cu succes!\n")
teste()

def citeste_lista():
    nr=input("Introduceți numerele separate prin spațiu: ")
    W=[int(x) for x in nr.split()]
    return W

def meniu():
    print("\n--- MENIU ---")
    print("1. Citirea unei liste de numere întregi")
    print("2. Găsirea secvenței maxime strict crescatoare")
    print("3. Găsirea secvenței maxime unde 3 elemente consecutive au o valoare care se repetă")
    print("4. Găsirea secvenței maxime unde 2 numere consecutive sunt relativ prime")
    print("5. Ieșire din aplicație")

def main():
    V=[]
    while True:
        meniu()
        n=input("Alegeți o opțiune (1-5): ")
        match n:
            case "1":
                V=citeste_lista()
                print(f"Numerele ce vor fi prelucrate sunt: {V}")
            case "2":
                if not V:
                    print("Eroare: Lista este goală! Citiți mai întâi lista de numere!")
                else:
                    x=secv_max(V,P1)
                    print(f"Secvența maximă de numere strict crescătoare este: {x}")
            case "3":
                if not V:
                    print("Eroare: Lista este goală! Citiți mai întâi lista de numere!")
                else:
                    y=secv_max(V,P9)
                    print(f"Secvența maximă pentru o valoare care se repetă într-un șir de 3 elemente consecutive este: {y}")
            case "4":
                if not V:
                    print("Eroare: Lista este goală! Citiți mai întâi lista de numere!")
                else:
                    z=secv_max(V,P3)
                    print(f"Secvența maximă pentru oricare două numere consecutive relativ prime este: {z}")
            case "5":
                print("Programul se va închide...")
                break
            case _:
                print("Opțiune invalidă! Vă rugăm să alegeți un număr între 1 și 5.")
main()