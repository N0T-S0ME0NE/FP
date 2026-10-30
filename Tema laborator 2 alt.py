def prim(n):
    if n < 2:
        return False
    d = 2
    while d * d <= n:
        if n % d == 0:
            return False
        d += 1
    return True

def main():
    n = int(input("n = "))
    m = n - 1
    ok = 0
    while m > 1:
        if prim(m):
            print(f"Cel mai mare numar prim mai mic decat n este: {m}")
            ok = 1
            break
        m -= 1
    if ok == 0:
        print(f"Nu exista numar prim mai mic decat n.")
main()