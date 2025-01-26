
import fractions
from math import log10, floor
from time import sleep

def WriteDigits(File, Number):
    digit = Number
    Scale = 10 ** floor(log10(Number))
    while Scale >= 1:
        File.write(str(digit // Scale))
        digit %= Scale
        Scale //= 10
    File.write("\n")

def ReadDigits(File):
    Number = 0
    digit = File.read(1)
    while digit != "\n":
        Number = Number * 10 + int(digit)
        digit = File.read(1)
    #print(f"Read {Number} from the file")
    return Number

File = open("PI Approximation/Data.txt", "r")
n = ReadDigits(File)
numerator = ReadDigits(File)
denominator = ReadDigits(File)
yn = ReadDigits(File)
xn = ReadDigits(File)
Sum = fractions.Fraction(numerator, denominator)
File.close()

def calculate_pi(goal = float("inf"), wait = 5000):
    global n, yn, xn, Sum
    File = open("PI Approximation/Digits.txt", "r")
    AlreadyKnown = len(File.read())
    File.close()
    digits = AlreadyKnown
    while digits <= goal:
        #print(f"Calculating {n}th term...")
        n += 1
        yn *= 2 * n ** 2
        xn *= (2 * n + 1) * 2 * n
        tn = fractions.Fraction(yn, xn)
        Sum += tn
        digits = - floor(log10(yn) - log10(xn))
        Digits = Sum.numerator * 10 ** (digits-1) // Sum.denominator
        if n % wait == 0:    
            File = open("PI Approximation/Data.txt", "w")
            WriteDigits(File, n)
            WriteDigits(File, Sum.numerator)
            WriteDigits(File, Sum.denominator)
            WriteDigits(File, yn)
            WriteDigits(File, xn)
            File.close()
            File = open("PI Approximation/Digits.txt", "w")
            WriteDigits(File, Digits)
            File.close()
            print("Waiting for 5 seconds...")
            sleep(5)