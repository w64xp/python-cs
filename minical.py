def line () :
    return "........................................"
def add(a, b):
    c = a+b
    return c
def sub(a, b):
    c = a-b
    return c
def mul(a, b):
    c = a*b
    return c
def div(a, b):
    c = a/b
    return c
def exp(a, b):
    c = a**b
    return c

print("Calculator")
print(line())
a = int(input("input a: "))
b = int(input("input b: "))
choice = input("input math symbol(+,-,*,/,**) : ")
print(line())
if choice =="+" :
    s = add(a,b)
elif choice =="-":
    s = sub(a,b)
elif choice =="*":
    s = mul(a,b)
elif choice =="/":
    s = div(a,b)
elif choice =="**":
    s = exp(a,b)
else :
    print("Error")
print("result: ",s)