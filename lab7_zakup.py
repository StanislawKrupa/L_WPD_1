
n = 6
K = 10
x_a = 2

# ceny zakupu jednostki surowca w okresie j (indeks 1..n)
c = [None, 4, 3, 5, 3, 4, 2]
# zapotrzebowanie na surowiec w okresie j
v = [None, 6, 7, 4, 2, 4, 3]

# phi[j][x] = minimalny koszt od okresu j do n przy stanie magazynu x przed okresem j
phi   = [[float('inf')] * (K + 1) for _ in range(n + 2)]
u_opt = [[None]         * (K + 1) for _ in range(n + 2)]

# warunek końcowy
for x in range(K + 1):
    phi[n + 1][x] = 0

# iteracja wstecz: j = n, n-1, ..., 1
for j in range(n, 0, -1):
    for x_prev in range(K + 1):
        u_min = max(0, v[j] - x_prev)   # minimalne zakupy (zaspokojenie popytu)
        u_max = K - x_prev               # maksymalne zakupy (pojemność magazynu)

        for u in range(u_min, u_max + 1):
            x_j = x_prev + u - v[j]
            if 0 <= x_j <= K:
                cost = c[j] * u + phi[j + 1][x_j]
                if cost < phi[j][x_prev]:
                    phi[j][x_prev] = cost
                    u_opt[j][x_prev] = u

# odtwarzanie optymalnej strategii (iteracja w przód od x_a)
policy   = []
x_states = [x_a]
x_curr   = x_a

for j in range(1, n + 1):
    u_star = u_opt[j][x_curr]
    policy.append(u_star)
    x_curr = x_curr + u_star - v[j]
    x_states.append(x_curr)

# ─── wyniki ───────────────────────────────────────────────────────────────────
print("=" * 62)
print(f"  DANE: n={n}, K={K}, x_0={x_a}")
print(f"  Ceny:            c = {c[1:]}")
print(f"  Zapotrzebowanie: v = {v[1:]}")
print("=" * 62)
print(f"  Optymalny koszt:      phi_1(x_0) = phi_1({x_a}) = {phi[1][x_a]}")
print(f"  Optymalna strategia:  u* = {policy}")
print(f"  Stany magazynu:       x  = {x_states}")
cost_check = sum(c[j + 1] * policy[j] for j in range(n))
print(f"  Weryfikacja kosztu:   {' + '.join(f'{c[j+1]}·{policy[j]}' for j in range(n))} = {cost_check}")
print("=" * 62)

# ─── tabela phi_j (iteracja wstecz) ──────────────────────────────────────────
print("\nTabela wartości funkcji Bellmana  phi_j(x_{j-1}):")
header = f"{'j':>3} | " + "  ".join(f"x={x:<2}" for x in range(K + 1))
sep    = "-" * len(header)
print(header)
print(sep)
for j in range(1, n + 1):
    vals = "  ".join(
        f"{phi[j][x]:>4}" if phi[j][x] != float('inf') else " inf"
        for x in range(K + 1)
    )
    print(f"{j:>3} | {vals}")

# ─── tabela optymalnych decyzji u*_j ─────────────────────────────────────────
print("\nTabela optymalnych decyzji  u*_j(x_{j-1}):")
print(header)
print(sep)
for j in range(1, n + 1):
    vals = "  ".join(
        f"{u_opt[j][x]:>4}" if u_opt[j][x] is not None else "   -"
        for x in range(K + 1)
    )
    print(f"{j:>3} | {vals}")
