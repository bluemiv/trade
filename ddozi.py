symbol = ":bounce:"
n = 3
indent = 6
print("--")

for i in range(n-1):
    print(" " * indent*(n-i-1) + symbol * (2*i+1))

for i in range(n):
    print(" " * (indent*i) + symbol * (2*(n-i-1)+1))