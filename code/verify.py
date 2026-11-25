"""Check whiskered Lefschetz ranks in the ORIGINAL x,y monomial basis.

Requires Python 3.10+ and NumPy. All elimination is exact, in prime fields.
The script enumerates every labelled simple graph through four vertices,
tests a non-flag simplicial complex, all labelled chordal graphs through five
vertices, several paired higher-power algebras, and the order-eight example.
Every comparison calls check(), which exits with status 1 on any mismatch, so
the script also fails correctly under python -O.  Usage:
    python3 verify.py [--output results/verification.json]
"""

import json
import sys
from itertools import combinations, product
from math import comb, factorial
import numpy as np


def check(condition, message):
    """Stop with exit status 1 if a verified statement fails."""
    if not condition:
        print("FAIL: " + message)
        sys.exit(1)


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


def face_basis(n, nonfaces):
    """Index the original squarefree monomials by two disjoint bitsets."""
    limit = 1 << n
    faces = [s for s in range(limit) if all(s & f != f for f in nonfaces)]
    by_degree = [[] for _ in range(n + 1)]
    for x in faces:
        for y in range(limit):
            if not x & y:
                by_degree[(x | y).bit_count()].append(x | (y << n))
    return faces, by_degree


def inclusion_power(source, target, d):
    """The coefficient of v in L^d u counts orders of the added variables."""
    return np.array([[factorial(d) if v & u == u else 0 for u in source]
                     for v in target], dtype=np.int64).reshape(len(target), len(source))


def rank_mod(matrix, p):
    work = matrix % p
    rank = 0
    for col in range(work.shape[1]):
        choices = np.flatnonzero(work[rank:, col])
        if not len(choices):
            continue
        pivot = rank + choices[0]
        work[[rank, pivot]] = work[[pivot, rank]]
        inv = pow(int(work[rank, col]), -1, p)
        factors = work[rank + 1:, col].copy() * inv % p
        work[rank + 1:] = (work[rank + 1:] - factors[:, None] * work[rank]) % p
        rank += 1
        if rank == work.shape[0]:
            break
    return rank


def boolean_power_rank(m, r, t, p):
    if not 0 <= r < t <= m:
        return 0
    d = t - r
    b = min(r, m - t)
    return sum(choose(m, h) - choose(m, h - 1) for h in range(b + 1)
               if factorial(d) * comb(b + d - h, d) % p)


def matrices(n, by_degree, i, j):
    """Matrices for A and its idealisation, with phi the all-leaves coefficient."""
    D = n + 1
    degrees = by_degree + [[]]
    d = j - i
    source = degrees[i]
    dual_target = degrees[D - j]
    base = inclusion_power(source, degrees[j], d)
    dual = inclusion_power(dual_target, degrees[D - i], d).T
    core_vertices = (1 << n) - 1
    # The cross term is d times phi(v L^(d-1) u).
    cross = np.array([[factorial(d) if not (u & v or (u | v) & core_vertices)
                       else 0 for u in source] for v in dual_target],
                     dtype=np.int64).reshape(len(dual_target), len(source))
    return base, np.block([[base, np.zeros((len(degrees[j]), len(degrees[D - i])),
                                           dtype=np.int64)], [cross, dual]])


def validate(n, nonfaces, primes=(2, 3, 5, 7)):
    faces, degrees = face_basis(n, nonfaces)
    sizes = [s.bit_count() for s in faces]
    D = n + 1
    outcomes = {p: [True] * 4 for p in primes}
    comparisons = 0
    for i, j in combinations(range(D + 1), 2):
        base, trivial = matrices(n, degrees, i, j)
        for p in primes:
            base_rank = rank_mod(base, p)
            ideal_rank = rank_mod(trivial, p)
            expected_base = sum(boolean_power_rank(n - s, i - s, j - s, p)
                                for s in sizes)
            expected_ideal = boolean_power_rank(D, i, j, p)
            for s in sizes:
                if s:
                    expected_ideal += boolean_power_rank(n - s, i - s, j - s, p)
                    expected_ideal += boolean_power_rank(n - s, D - j - s,
                                                         D - i - s, p)
            check((base_rank, ideal_rank) == (expected_base, expected_ideal),
                  f"rank mismatch n={n} i={i} j={j} p={p}")
            comparisons += 2
            base_full = base_rank == min(base.shape)
            ideal_full = ideal_rank == min(trivial.shape)
            outcomes[p][1] &= base_full
            outcomes[p][3] &= ideal_full
            if j == i + 1:
                outcomes[p][0] &= base_full
                outcomes[p][2] &= ideal_full
    a = max(sizes)
    for p in primes:
        threshold = 1 + (n % 2)
        check(outcomes[p] == [a <= threshold and p > (n + 1) // 2,
                               a <= 1 and p > n,
                               a <= threshold and p > (D + 1) // 2,
                               a <= 1 and p > D],
              f"WLP/SLP classification mismatch n={n} p={p}")
    return comparisons


def check_chordal(n, edges):
    """Compare all graded power ranks on a chordal graph with the recursion."""
    adj = [{v} for v in range(n)]
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)

    def simplicial(vertices):
        for v in sorted(vertices):
            neighbours = adj[v] & vertices
            if all(neighbours <= adj[w] for w in neighbours):
                return v
        return None

    vertices = set(range(n))
    while vertices:
        pivot = simplicial(vertices)
        if pivot is None:
            return 0
        vertices.remove(pivot)

    def blocks(vertices):
        if not vertices:
            return [(0, 0)]
        w = simplicial(vertices)
        result = [(m + 1, s) for m, s in blocks(vertices - adj[w])]
        for v in (adj[w] & vertices) - {w}:
            result += [(m, s + 1) for m, s in blocks(vertices - adj[v])]
        return result

    profile = blocks(set(range(n)))
    edge_masks = [(1 << i) | (1 << j) for i, j in edges]
    faces = [f for f in range(1 << n) if all(f & e != e for e in edge_masks)]
    maximal = [f for f in faces if all(f == h or f & h != f for h in faces)]
    check(len(profile) == len(maximal), "block count differs from maximal independent sets")
    levels = [[f for f in faces if f.bit_count() == j]
              for j in range(max(f.bit_count() for f in faces) + 1)]
    count = 0
    for i, j in combinations(range(len(levels)), 2):
        test = inclusion_power(levels[i], levels[j], j - i)
        for p in (2, 3, 5, 7):
            expected = sum(boolean_power_rank(m, i - s, j - s, p) for m, s in profile)
            check(rank_mod(test, p) == expected, f"chordal rank mismatch n={n} p={p}")
            count += 1
    return count


def check_higher(exponents, forbidden):
    n = len(exponents)
    E = sum(d - 1 for d in exponents)
    faces = [s for s in range(1 << n) if all(s & f != f for f in forbidden)]
    levels = [[] for _ in range(E + 1)]
    for v in product(*(range(1 - d, d) for d in exponents)):
        support = sum(1 << i for i, e in enumerate(v) if e > 0)
        if support in faces:
            levels[sum(abs(e) for e in v)].append(v)
    polynomials = []
    for s in faces:
        poly = [0] * s.bit_count() + [1]
        for i, d in enumerate(exponents):
            poly = np.convolve(poly, [1] * (d - ((s >> i) & 1)))
        polynomials.append(poly)

    def coefficient(u, v, power):
        increments = [abs(b) - abs(a) for a, b in zip(u, v)]
        if min(increments) < 0 or any(a * b < 0 for a, b in zip(u, v)):
            return 0
        result = factorial(power)
        for delta in increments:
            result //= factorial(delta)
        return result

    count = 0
    for i, j in combinations(range(E + 1), 2):
        matrix = np.array([[coefficient(u, v, j - i) for u in levels[i]]
                           for v in levels[j]], dtype=np.int64)
        rank = rank_mod(matrix, 1009)
        check(rank == sum(min(h[i], h[j]) for h in polynomials),
              f"higher-power rank mismatch {exponents}")
        if len(set(exponents)) == 1:
            a = max(s.bit_count() for s in faces)
            check((rank < min(matrix.shape)) == (E < i + j < E + a),
                  f"higher-power strip mismatch {exponents}")
        count += 1
    return count


def main():
    graphs = comparisons = 0
    for n in range(1, 5):
        edges = [(1 << i) | (1 << j) for i, j in combinations(range(n), 2)]
        for mask in range(1 << len(edges)):
            graph = [e for index, e in enumerate(edges) if mask & (1 << index)]
            comparisons += validate(n, graph)
            graphs += 1
    print(f"{graphs} labelled graphs, {comparisons} matrix ranks agreed.")
    other = validate(4, [0b0111, 0b1011])
    print(f"Non-flag complex with two minimal missing triples: {other} ranks agreed.")
    chordal = chordal_ranks = 0
    for n in range(1, 6):
        edges = list(combinations(range(n), 2))
        for mask in range(1 << len(edges)):
            present = [e for i, e in enumerate(edges) if mask & (1 << i)]
            count = check_chordal(n, present)
            if count:
                chordal += 1
                chordal_ranks += count
    print(f"{chordal} chordal graphs: {chordal_ranks} independent rank comparisons.")
    higher = sum(check_higher(exponents, forbidden)
                 for exponents in [(3,), (4, 4), (3, 3, 3), (2, 3, 5)]
                 for forbidden in ([[], [3]] if len(exponents) > 1 else [[]]))
    print(f"Higher paired powers: {higher} direct rank comparisons over F_1009.")
    n = 8
    edges = [(1 << i) | (1 << j) for i, j in combinations(range(n), 2)
             if j > 2]
    _, degrees = face_basis(n, edges)
    matrix = inclusion_power(degrees[4], degrees[5], 1)
    rank = rank_mod(matrix, 1009)
    check(matrix.shape == (406, 400) and rank == 386, "order-eight example")
    print(f"Published order-eight example over F_1009: rank {rank}, "
          f"kernel {matrix.shape[1] - rank}, cokernel {matrix.shape[0] - rank}.")
    summary = {
        "whiskered_labelled_graphs_orders_1_to_4": graphs,
        "whiskered_rank_comparisons_F2_F3_F5_F7": comparisons,
        "non_flag_complex_rank_comparisons": other,
        "chordal_labelled_graphs_orders_1_to_5": chordal,
        "chordal_rank_comparisons": chordal_ranks,
        "higher_power_rank_comparisons_F1009": higher,
        "order_eight_example": {"dim_A4": int(matrix.shape[1]),
                                "dim_A5": int(matrix.shape[0]), "rank": rank,
                                "kernel": int(matrix.shape[1] - rank),
                                "cokernel": int(matrix.shape[0] - rank)},
        "status": "PASS",
    }
    if "--output" in sys.argv:
        with open(sys.argv[sys.argv.index("--output") + 1], "w") as handle:
            json.dump(summary, handle, indent=2, sort_keys=True)
            handle.write("\n")
    print("PASS: all whiskered, idealisation, chordal and higher-power checks.")


if __name__ == "__main__":
    main()
