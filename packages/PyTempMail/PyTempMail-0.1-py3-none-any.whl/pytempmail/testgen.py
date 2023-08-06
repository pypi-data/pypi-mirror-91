def count(i):
    for k in range(i):
        yield k

for c in count(5):
    print(c)

print("END")