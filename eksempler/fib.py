# coding=dansk

fra functools indfør lru_cache som mfb_cache


@mfb_cache()
lad fib(n):
    hvis n indeni (0, 1):
        aflever n
    ellers:
        aflever fib(n - 1) + fib(n - 2)


print(fib(20))
