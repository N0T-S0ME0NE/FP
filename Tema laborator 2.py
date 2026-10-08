n = int(input("n = "))
v = [0] * 10
i = 0
while n > 0:
    v[n % 10] += 1
    n = n // 10
    i += 1
for j in range(1, 10):
    if v[j] > 0:
        mn = j
        v[j] -= 1
        break
x = mn
for j in range(10):
    for k in range(v[j]):
        x = x * 10 + j
print(x)
