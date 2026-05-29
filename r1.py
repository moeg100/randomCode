#Factorial in recursive

def factorial(a):
    if a == 1 or a == 0:
        return 1
    return a * factorial(a-1)
    
    
print(factorial(5))




#Fibonacci in recursive
def fibo(n):
    if n == 1:
        return 1
    if n == 0:
        return 0
        
    return fibo(n-1) + fibo(n-2)
    
    
    
for i in range(30):
    print(fibo(i))



def countString(s):
        count = 0
        for i in s:
                count += 1

        return count
        
        
print(countString("hello"))
