a = 1
def b():
    global a
    a += 1
    print(a)
    return a
print(b())