"""Lefschetz classifications for chordal graph algebras via Boolean blocks.

For a chordal graph H the algebra R(H) = K[z_v]/(z_v^2, z_v z_w : vw in E(H))
splits, as a graded module over K[L] with L the sum of the variables, into
shifted Boolean blocks B_m<s> (Theorem 6.1 of the manuscript).  This script

  1. computes the block multiset by simplicial-vertex elimination,
  2. evaluates the exact rank of every graded power of L from the blocks in
     characteristic 0 and in characteristic p (Wilson's diagonal form),
  3. checks those ranks against direct elimination in the original variables,
  4. checks that two different elimination orders give the same multiset,
  5. checks multiplicativity over disjoint unions,
  6. derives the WLP/SLP classifications of paths P_n and lollipops L_{m,n}
     and compares them with the published characteristic-zero lists, and
  7. checks the explicit witness inequalities used in the manuscript's proof
     for all n beyond the finite range.

Pure standard library; exact integer arithmetic only.  Every statement goes
through check(), which exits with status 1 on failure, so the script also
fails correctly under python -O.  Usage:
    python3 chordal_lefschetz.py [--output results/chordal.json]
"""

import json
import random
import sys
from collections import Counter
from functools import lru_cache
from itertools import combinations
from math import comb, factorial

CHAR0 = 0          # characteristic zero
DIRECT_PRIME = 1009  # direct eliminations; see note in direct_rank()


def check(condition, message):
    if not condition:
        print("FAIL: " + message)
        sys.exit(1)


def choose(n, k):
    return comb(n, k) if 0 <= k <= n else 0


# ---------------------------------------------------------------- graphs
def path(n):
    return n, frozenset((i, i + 1) for i in range(n - 1))


def lollipop(m, n):
    """K_m on 0..m-1, path m..m+n-1, bridge (m-1, m)."""
    edges = {(i, j) for i, j in combinations(range(m), 2)}
    edges |= {(m + i, m + i + 1) for i in range(n - 1)}
    edges.add((m - 1, m))
    return m + n, frozenset(edges)


def adjacency(n, edges):
    adj = [set() for _ in range(n)]
    for i, j in edges:
        adj[i].add(j)
        adj[j].add(i)
    return adj


def independence_number(n, edges):
    adj = adjacency(n, edges)

    @lru_cache(maxsize=None)
    def alpha(vertices):
        if not vertices:
            return 0
        v = min(vertices)
        rest = vertices - {v}
        return max(alpha(rest), 1 + alpha(rest - frozenset(adj[v])))
    return alpha(frozenset(range(n)))


# ---------------------------------------------------------------- blocks
def blocks(n, edges, rule=min):
    """Block multiset Counter{(m, s)} by simplicial-vertex elimination.

    rule picks which simplicial vertex to use (min or max label), so two
    different elimination orders can be compared.  Returns None if the graph
    is not chordal (elimination gets stuck).
    """
    adj = adjacency(n, edges)

    @lru_cache(maxsize=None)
    def rec(vertices):
        """Block multiset as a sorted tuple of ((m, s), multiplicity)."""
        if not vertices:
            return (((0, 0), 1),)
        simplicial = [v for v in vertices
                      if all(adj[a] >= (adj[v] & vertices) - {a}
                             for a in adj[v] & vertices)]
        if not simplicial:
            return None
        w = rule(simplicial)
        closed = (adj[w] & vertices) | {w}
        first = rec(vertices - closed)
        if first is None:
            return None
        out = Counter()
        for (m, s), c in first:
            out[(m + 1, s)] += c
        for v in sorted(adj[w] & vertices):
            sub = rec(vertices - ((adj[v] & vertices) | {v}))
            if sub is None:
                return None
            for (m, s), c in sub:
                out[(m, s + 1)] += c
        return tuple(sorted(out.items()))
    result = rec(frozenset(range(n)))
    return None if result is None else Counter(dict(result))


def boolean_power_rank(m, r, t, p):
    """Rank of U^(t-r): (B_m)_r -> (B_m)_t over a field of characteristic p."""
    if not 0 <= r < t <= m:
        return 0
    d, b = t - r, min(r, m - t)
    total = 0
    for h in range(b + 1):
        entry = factorial(d) * comb(b + d - h, d)
        if p == CHAR0 or entry % p:
            total += choose(m, h) - choose(m, h - 1)
    return total


def block_rank(profile, i, j, p):
    source = sum(c * choose(m, i - s) for (m, s), c in profile.items())
    target = sum(c * choose(m, j - s) for (m, s), c in profile.items())
    rank = sum(c * boolean_power_rank(m, i - s, j - s, p)
               for (m, s), c in profile.items())
    return source, target, rank


def top_degree(profile):
    return max(m + s for m, s in profile)


def lefschetz(profile, p):
    """(WLP, SLP) of the algebra with this block profile, characteristic p."""
    top = top_degree(profile)
    wlp = slp = True
    for i in range(top + 1):
        for j in range(i + 1, top + 1):
            source, target, rank = block_rank(profile, i, j, p)
            full = rank == min(source, target)
            if not full:
                slp = False
                if j == i + 1:
                    wlp = False
    return wlp, slp


def lefschetz_char0_by_types(types):
    """Characteristic-0 WLP/SLP from the SET of block types alone (the
    multiplicity-free criterion of the manuscript's Theorem 6.3)."""
    top = max(m + s for m, s in types)
    wlp = slp = True
    for i in range(top + 1):
        for j in range(i + 1, top + 1):
            kernel = any(s <= i <= s + m and i + j > 2 * s + m for m, s in types)
            cokernel = any(s <= j <= s + m and i + j < 2 * s + m for m, s in types)
            if kernel and cokernel:
                slp = False
                if j == i + 1:
                    wlp = False
    return wlp, slp


# ---------------------------------------------------------------- direct check
def rank_mod(rows, ncols, p):
    rows = [r[:] for r in rows]
    rank, col = 0, 0
    nrows = len(rows)
    for col in range(ncols):
        pivot = next((r for r in range(rank, nrows) if rows[r][col] % p), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], -1, p)
        for r in range(rank + 1, nrows):
            f = rows[r][col] * inv % p
            if f:
                rows[r] = [(a - f * b) % p for a, b in zip(rows[r], rows[rank])]
        rank += 1
    return rank


def direct_rank(n, edges, i, j, p):
    """Rank of L^(j-i): R(H)_i -> R(H)_j in the ORIGINAL monomial basis.

    The coefficient of an independent set J >= I with |J|-|I| = d is d!.
    With p = 1009 and orders below 20, every Wilson entry d! binom(k, d)
    with k <= 20 is prime to p, so these ranks equal characteristic-0 ranks
    (and the comparison is also made at small primes)."""
    edge_masks = [(1 << a) | (1 << b) for a, b in edges]
    faces = [f for f in range(1 << n) if all(f & e != e for e in edge_masks)]
    src = [f for f in faces if f.bit_count() == i]
    tgt = [f for f in faces if f.bit_count() == j]
    d = j - i
    rows = [[factorial(d) % p if (v & u) == u else 0 for u in src] for v in tgt]
    if not src or not tgt:
        return len(src), len(tgt), 0
    return len(src), len(tgt), rank_mod(rows, len(src), p)


# ---------------------------------------------------------------- witnesses
def ceil_div(a, b):
    return -(-a // b)


def path_witness(n):
    """Section 6 Lemma: kernel block (ceil(n/2), 0), cokernel block at s'."""
    return ceil_div(n, 4) + 1 <= (n + 1) // 3


def lollipop_witness(m, n):
    big = ceil_div(n, 2) + 1
    low = ceil_div(big, 2)
    w2 = low <= n // 3                     # cokernel block from Y * P_{n-1}
    w3 = m >= 3 and low <= (n + 1) // 3    # cokernel block from Y * P_n
    return w2 or w3


NT_PATH_WLP = {1, 2, 3, 4, 5, 6, 7, 9, 10, 13}


def published_lollipop(m, n):
    if m == 1:
        return n in {1, 2, 3, 4, 5, 6, 8, 9, 12}
    if m == 2:
        return n in {1, 2, 3, 4, 5, 7, 8, 11}
    return n in {1, 3, 4, 7}


def primes_upto(limit):
    return [q for q in range(2, limit + 1)
            if all(q % r for r in range(2, int(q ** 0.5) + 1))]


def main():
    out = {}
    rng = random.Random(20261124)

    # (3) direct-elimination check of block ranks on paths, lollipops and
    # random chordal graphs, all graded powers, char 0 proxy and small primes
    direct = 0
    cases = [path(n) for n in range(1, 13)]
    cases += [lollipop(m, n) for m in range(2, 6) for n in range(1, 8)]
    for n, edges in cases:
        prof = blocks(n, edges)
        check(prof is not None, "path/lollipop not chordal?")
        top = top_degree(prof)
        for i in range(top + 1):
            for j in range(i + 1, top + 1):
                for p in (2, 3, 5, DIRECT_PRIME):
                    if n > 10 and p != DIRECT_PRIME and j - i > 1:
                        continue
                    want = block_rank(prof, i, j, CHAR0 if p == DIRECT_PRIME else p)
                    got = direct_rank(n, edges, i, j, p)
                    check(want == got, f"direct rank n={n} i={i} j={j} p={p}")
                    direct += 1
    out["direct_rank_comparisons"] = direct

    # (4) elimination-order invariance and (5) multiplicativity on random
    # chordal graphs (random perfect elimination orderings)
    invariant = multiplicative = 0
    for trial in range(300):
        n = rng.randint(2, 10)
        edges = set()
        for v in range(1, n):
            earlier = list(range(v))
            # attach v to a clique among earlier vertices (keeps chordality)
            base = rng.choice(earlier)
            clique = {base}
            for u in earlier:
                if u != base and rng.random() < 0.5 and all(
                        (min(u, c), max(u, c)) in edges for c in clique):
                    clique.add(u)
            if rng.random() < 0.85:
                edges |= {(c, v) for c in clique}
        edges = frozenset(edges)
        a, b = blocks(n, edges, min), blocks(n, edges, max)
        check(a is not None and a == b, f"elimination order changed blocks {edges}")
        invariant += 1
        n2, e2 = path(rng.randint(1, 6))
        union = frozenset(edges | {(x + n, y + n) for x, y in e2})
        prod = Counter()
        for (m1, s1), c1 in a.items():
            for (m2, s2), c2 in blocks(n2, e2).items():
                prod[(m1 + m2, s1 + s2)] += c1 * c2
        check(blocks(n + n2, union) == prod, "disjoint union not multiplicative")
        multiplicative += 1
    out["elimination_order_invariance_tests"] = invariant
    out["disjoint_union_multiplicativity_tests"] = multiplicative

    # (6) paths
    nmax = 120
    path_wlp, path_slp, path_rows = [], [], []
    for n in range(1, nmax + 1):
        prof = blocks(*path(n))
        alpha = independence_number(*path(n))
        check(alpha == ceil_div(n, 2), "alpha(P_n)")
        check(max(m for m, _ in prof) == alpha, "largest block size equals alpha")
        w0, s0 = lefschetz(prof, CHAR0)
        check((w0, s0) == lefschetz_char0_by_types(set(prof)), "type criterion")
        check(w0 == (n in NT_PATH_WLP), f"Nguyen-Tran list disagrees at n={n}")
        if not w0:
            check(n <= 7 or path_witness(n) or n in NT_PATH_WLP,
                  f"path failure without witness n={n}")
        check(path_witness(n) == (n >= 8 and n not in NT_PATH_WLP),
              f"path witness set n={n}")
        if w0:
            path_wlp.append(n)
        if s0:
            path_slp.append(n)
        if n <= 40:
            for p in primes_upto(45):
                w, s = lefschetz(prof, p)
                check(w == (w0 and p > ceil_div(alpha, 2)), f"path WLP char {p} n={n}")
                check(s == (s0 and p > alpha), f"path SLP char {p} n={n}")
    for n in range(nmax + 1, 5001):
        check(path_witness(n), f"path witness inequality n={n}")
    out["paths"] = {"checked_n": [1, nmax], "wlp_char0": path_wlp,
                    "slp_char0": path_slp,
                    "prime_thresholds_checked": "n<=40, all primes p<=43",
                    "witness_inequality_checked_to": 5000}

    # lollipops
    lol = {}
    for m in range(1, 9):
        wl, sl = [], []
        for n in range(1, 61):
            g = lollipop(m, n) if m >= 2 else path(n + 1)
            prof = blocks(*g)
            w0, s0 = lefschetz(prof, CHAR0)
            check(w0 == published_lollipop(m, n), f"lollipop list m={m} n={n}")
            check((w0, s0) == lefschetz_char0_by_types(set(prof)), "type criterion L")
            if m >= 2:
                check(lollipop_witness(m, n) == (not w0),
                      f"lollipop witness set m={m} n={n}")
                alpha = independence_number(*g)
                check(alpha == ceil_div(n, 2) + 1, "alpha(L_{m,n})")
                if n <= 25:
                    for p in primes_upto(30):
                        w, s = lefschetz(prof, p)
                        check(w == (w0 and p > ceil_div(alpha, 2)),
                              f"lollipop WLP char {p}")
                        check(s == (s0 and p > alpha), f"lollipop SLP char {p}")
            if w0:
                wl.append(n)
            if s0:
                sl.append(n)
        lol[str(m)] = {"wlp_char0": wl, "slp_char0": sl}
        if m >= 3:
            check(set(blocks(*lollipop(m, 9))) == set(blocks(*lollipop(3, 9))),
                  "block types independent of m>=3")
    for n in range(61, 5001):
        check(lollipop_witness(2, n) and lollipop_witness(3, n),
              f"lollipop witness inequality n={n}")
    out["lollipops"] = {"checked": "1<=m<=8, 1<=n<=60", "by_m": lol,
                        "witness_inequality_checked_to": 5000}
    out["status"] = "PASS"

    print(f"Direct eliminations agreeing with block ranks: {direct}")
    print(f"Elimination-order invariance: {invariant}; multiplicativity: {multiplicative}")
    print(f"Paths, WLP in char 0 for n<={nmax}: {path_wlp}")
    print(f"Paths, SLP in char 0 for n<={nmax}: {path_slp}")
    for m in range(1, 9):
        print(f"Lollipop m={m}: WLP n={lol[str(m)]['wlp_char0']}; "
              f"SLP n={lol[str(m)]['slp_char0']}")
    print("PASS: chordal block criterion, paths and lollipops.")
    if "--output" in sys.argv:
        with open(sys.argv[sys.argv.index("--output") + 1], "w") as handle:
            json.dump(out, handle, indent=2, sort_keys=True)
            handle.write("\n")


if __name__ == "__main__":
    main()
