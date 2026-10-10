import random
from math import gcd as math_gcd
from sympy import isprime as sympy_isprime   #  dung de doi chieu

# ---------- 3. luy thua modulo (square-and-multiply) ----------
def mod_exp(a, x, p):
    result = 1
    a %= p
    while x > 0:
        if x & 1:                      # bit thap nhat cua x la 1
            result = (result * a) % p
        a = (a * a) % p                # binh phương
        x >>= 1                        # dich sang bit tiep theo
    return result

# ---------- 1. So nguyen to (Miller-Rabin) ----------
SMALL_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]

def is_prime(n, extra_rounds=20):
    if n < 2:
        return False
    for p in SMALL_PRIMES:
        if n % p == 0:
            return n == p
    d, s = n - 1, 0                    # n-1 = 2^s * d, d le
    while d % 2 == 0:
        d //= 2
        s += 1
    bases = SMALL_PRIMES + [random.randrange(2, n - 1) for _ in range(extra_rounds)]
    for a in bases:
        x = mod_exp(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False               # chac chan la hop so
    return True                        # rat co the la so nguyen to

def random_prime(bits):
    while True:
        n = random.getrandbits(bits) | (1 << (bits - 1)) | 1   # du so bit và la so le
        if is_prime(n):
            return n

def largest_primes_below(limit, count):
    primes, k = [], limit - 1
    while len(primes) < count:
        if is_prime(k):
            primes.append(k)
        k -= 1
    return primes

# ---------- 2. GCD (Euclid) ----------
def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


if __name__ == "__main__":
    print("===== 1a. so nguyen to ngau nhien =====")
    for b in (8, 16, 64):
        print(f"{b:>2} bit: {random_prime(b)}")

    print("\n===== 1b. 10 so nguyen to lon nhat < 2^89 - 1 =====")
    M10 = 2**89 - 1
    for i, p in enumerate(largest_primes_below(M10, 10), 1):
        print(f"{i:>2}. {p}")

    print("\n===== 1c. kiem tra so nguyen to (n < 2^89 - 1) =====")
    tests = [97, 1001, 2**31 - 1, 2**61 - 1, 2**67 - 1, 2**89 - 1 - 2]
    for n in tests:
        print(f"{n}: {is_prime(n)} (sympy: {sympy_isprime(n)})")
    n = int(input("Nhap mot so nguyen n < 2^89 - 1: "))
    if n >= M10:
        print("n phai nho hon 2^89 - 1")
    else:
        print(n, "la so nguyen to" if is_prime(n) else "khong phai so nguyen to")

    print("\n===== 2. GCD của hai so lon =====")
    a = random.getrandbits(4096)
    b = random.getrandbits(4096)
    g = gcd(a, b)
    print("a co", a.bit_length(), "bit, b co", b.bit_length(), "bit")
    print("GCD =", g)
    print("Khop math.gcd:", g == math_gcd(a, b))
    # Kiem tra bang so co uoc chung biet truoc
    k = random_prime(64)
    x, y = k * random.getrandbits(2000), k * random.getrandbits(2000)
    print("Uoc chung biet truoc chia het GCD:", gcd(x, y) % k == 0)

    print("\n===== 3. Luy thua modulo =====")
    print("7^40 mod 19 =", mod_exp(7, 40, 19), "| pow():", pow(7, 40, 19))
    big_a, big_x, big_p = random.getrandbits(512), random.getrandbits(512), random_prime(512)
    print("So mu 512 bit khop pow():", mod_exp(big_a, big_x, big_p) == pow(big_a, big_x, big_p))