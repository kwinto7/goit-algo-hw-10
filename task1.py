from typing import Dict, List
import math
import time

COINS_DEFAULT = [50, 25, 10, 5, 2, 1] 

def find_coins_greedy(amount: int, coins: List[int] = COINS_DEFAULT) -> Dict[int, int]:
    """
    Жадібний алгоритм: на кожному кроці беремо максимально можливу монету.
    Повертає словник {номінал: кількість}.
    """
    if amount < 0:
        raise ValueError("Сума має бути невід’ємною")

    change: Dict[int, int] = {}
    remaining = amount
    for c in coins:
        if remaining == 0:
            break
        cnt = remaining // c
        if cnt:
            change[c] = cnt
            remaining -= cnt * c

    if remaining != 0:
        # Таке можливо, якщо набір монет не покриває всі суми
        raise ValueError(f"Неможливо видати суму {amount} з монет {coins}")
    return change


def find_min_coins(amount: int, coins: List[int] = COINS_DEFAULT) -> Dict[int, int]:
    """
    Динамічне програмування (мінімальна кількість монет).
    dp[s] = мін. к-сть монет для суми s
    prev[s] = монета, якою найкраще доходимо до s
    Повертає словник {номінал: кількість}.
    """
    if amount < 0:
        raise ValueError("Сума має бути невід’ємною")
    if amount == 0:
        return {}

    # Ініціалізація
    dp = [math.inf] * (amount + 1)
    prev = [-1] * (amount + 1)
    dp[0] = 0

    # Заповнюємо dp
    for s in range(1, amount + 1):
        for c in coins:
            if c <= s and dp[s - c] + 1 < dp[s]:
                dp[s] = dp[s - c] + 1
                prev[s] = c

    if dp[amount] is math.inf:
        raise ValueError(f"Неможливо видати суму {amount} з монет {coins}")

    # Реконструкція відповіді
    res: Dict[int, int] = {}
    s = amount
    while s > 0:
        c = prev[s]
        res[c] = res.get(c, 0) + 1
        s -= c

    return dict(sorted(res.items()))  


if __name__ == "__main__":
    amt = 113

    g = find_coins_greedy(amt)
    d = find_min_coins(amt)

    print("Жадібний:", g)   
    print("DP      :", d)   

    # Мікро-бенчмарк
    def bench(fn, repeats=5, *, amount=100_000, coins=COINS_DEFAULT):
        best = math.inf
        for _ in range(repeats):
            t0 = time.perf_counter()
            fn(amount, coins)
            best = min(best, time.perf_counter() - t0)
        return best

    big_amount = 1_000_000  # велика сума для демонстрації
    t_greedy = bench(find_coins_greedy, amount=big_amount)
    t_dp = bench(find_min_coins, amount=50_000)  # обмежуємо, щоб не чекати довго

    print(f"\nGreedy {big_amount=:,}: {t_greedy*1e3:.3f} ms")
    print(f"DP     50,000:        {t_dp*1e3:.3f} ms (для 1,000,000 буде набагато повільніше)")
