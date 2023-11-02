def c_nk(n, k):
    """Calculate the binomial coefficient of n and k"""
    if 0 <= k <= n:
        num = 1
        den = 1
        for i in range(1, min(k, n - k) + 1):
            num *= n
            den *= i
            n -= 1
        return num // den
    else:
        return 0