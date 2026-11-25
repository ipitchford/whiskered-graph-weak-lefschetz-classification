# AI index: Boolean blocks and the weak Lefschetz property of whiskered and chordal graph algebras (v0.1.0-candidate)

Machine-oriented map of claims, evidence and limits. Human readers should start with [README.md](README.md) ("What
this is about") and the paper [manuscript.pdf](manuscript.pdf) (source [manuscript.tex](manuscript.tex); Section 1 is
a plain introduction with a roadmap). DOI 10.5281/zenodo.24540630 (concept 10.5281/zenodo.24540629). Status:
unrefereed candidate; internal AI-assisted review only.

## Normalisation

K a field of characteristic p ≥ 0. G a graph on n vertices with independence number α; w(G) its whiskering (a leaf
y_i at each vertex x_i). A_G = K[x, y]/(x_i², y_i², x_i y_i, x_i x_j for ij ∈ E(G)) = R(w(G)); more generally A_Δ for a
simplicial complex Δ with face numbers f_s and largest face size a. R(H) = K[z_v]/(z_v², z_v z_w for vw ∈ E(H)).
L = sum of all variables. WLP: some linear form gives maximal rank (injective or surjective) between all adjacent
degrees; SLP: the same for all powers. B_m = Boolean algebra Z[u_1..u_m]/(u_j²) with U = Σ u_j; B_m⟨s⟩ shifted to start
in degree s. b_n = 1 if n even, 2 if n odd. T = Nagata idealisation of A_Δ by its graded dual (socle degree D = n + 1).
HN = Holleben–Nicklasson, J. Pure Appl. Algebra 230 (2026) 108238, doi:10.1016/j.jpaa.2026.108238. Statement numbers
follow the manuscript.

## Claims and where they are proved

| ID | Claim | Location | Status / credit |
|---|---|---|---|
| 1 | Generic forms: over any field (finite included), rank(h^{j−i}) ≤ rank(L^{j−i}) for every linear form h on a monomial Artinian algebra | Lemma 2.1 | written proof; the WLP case over an arbitrary field is recorded by Cooper et al. (Lemma 2.2) |
| 2 | Boolean ranks: diagonal form of U^d: (B_m)_r → (B_m)_t with entries d!·C(b+d−h, d), multiplicity C(m,h) − C(m,h−1) | equation (2), Section 2 | from Wilson (1990) Theorem 2 (and Theorem 1 for ranks mod p); second proof Ghorbani et al. (2008) Cor. 3 |
| 3 | Integral splitting: after y_i ↦ u_i = x_i + y_i, A_Δ = ⊕_{S∈Δ} x_S B_{[n]∖S} as graded Z[L]-modules | Theorem 3.1 | written proof; complete-graph case in triangular form is HN Lemma 3.1 |
| 4 | Rank of every power of L in every characteristic; rank formula (3) for p = 0 or p > n | Section 3 | written proof |
| 5 (Theorem A) | For p = 0 or p > n, L^{j−i}: A_i → A_j fails maximal rank iff n < i + j < n + a. A_Δ has the WLP iff a ≤ b_n and (p = 0 or p > ⌈n/2⌉); the SLP iff a ≤ 1 and (p = 0 or p > n). Hence the HN conjecture (WLP fails for α(G) ≥ 3) holds over every field | Theorem 4.1 | written proof; checked in the original variables on all graphs of order ≤ 4 over F_2, F_3, F_5, F_7 |
| 5a | Eight-vertex example (K_8 minus a triangle, HN Ex. 3.17): dim A_4 = 400, dim A_5 = 406, rank 386, kernel 14, cokernel 20 | Example 4.2 | exact (verify.py, direct elimination over F_1009); block table by formula (3) |
| 6 (Theorem B) | Gorenstein idealisation T: ζ = (L, φ) attains every generic rank (p = 0 or p > D); WLP iff a ≤ b_n and (p = 0 or p > ⌈(n+1)/2⌉); SLP iff a ≤ 1 and (p = 0 or p > n + 1). For non-complete G, T is HN's G-quadratic Perazzo algebra in characteristic zero | Theorem 5.1, Corollary 5.2, Remark after it | written proof; necessity follows HN Theorem 4.6's projection argument; identification via HN Lemmas 4.3, 4.5 and Theorem 4.4 |
| 7 | Higher truncation exponents: integral splitting into monomial complete intersections; characteristic-zero rank formula; strip, WLP and SLP for equal exponents | Theorem 6.1 | written proof; prime-characteristic thresholds for unequal exponents not determined |
| 8 | Chordal splitting at a simplicial vertex; for chordal H, R(H) splits into one Boolean block per maximal independent set | Theorem 7.1 | written proof |
| 9 | Block profile P_H: independent of elimination order, multiplicative over disjoint unions, largest block size α(H) | Proposition 7.2 | written proof; tested on 300 random chordal graphs each |
| 10 (Theorem C) | Chordal criterion: in characteristic zero, maximal rank fails iff one block type blocks injectivity and one blocks surjectivity; WLP in characteristic p iff WLP in characteristic zero and p > ⌈α/2⌉; SLP iff SLP in characteristic zero and p > α | Theorem 7.3 | written proof |
| 11 | Paths: WLP iff n ∈ {1..7, 9, 10, 13} and (p = 0 or p > ⌈⌈n/2⌉/2⌉); SLP iff n ∈ {1..7, 9} and (p = 0 or p > ⌈n/2⌉) | Lemma 7.4, Corollary 7.5 | written proof for n ≥ 25 (witness inequality); exact finite check for n ≤ 24 (chordal_lefschetz.py); characteristic-zero WLP list is Nguyen–Tran Theorem 1.2(1) |
| 12 | Lollipops L_{m,n}, m ≥ 2: WLP lists {1..5, 7, 8, 11} (m = 2), {1, 3, 4, 7} (m ≥ 3); SLP lists {1..5, 7} (m = 2), {1, 3} (m ≥ 3); thresholds p > ⌈α/2⌉ (WLP), p > α (SLP), α = ⌈n/2⌉ + 1 | Corollary 7.6 | written proof for n ≥ 23; exact finite check for n ≤ 22; characteristic-zero WLP lists are Tran Quang Hoa, Nguyen Duy Phuoc and Tran Nguyen Thanh Son, arXiv:2510.21569, Theorem 1.3 |
| 13 | Outside the method: partially whiskered and very well-covered graphs in general (HN Ex. 3.18), cycles and tadpoles with a cycle of length ≥ 4, the classification of Perazzo algebras with the WLP | Section 8 | stated as open |

## Evidence

| Check | Script | Output | Scope |
|---|---|---|---|
| All labelled graphs of order 1–4: ranks of all powers of L on A_G and of ζ on T against Theorems 3.1 and 5.1; WLP/SLP thresholds of Theorem 4.1 and Corollary 5.2 | [code/verify.py](code/verify.py) | [results/verification.json](results/verification.json) | 75 graphs, 8,440 comparisons over F_2, F_3, F_5, F_7; exact elimination in the original variables |
| Non-flag complex on four vertices | code/verify.py | results/verification.json | 120 comparisons |
| All 894 labelled chordal graphs of order 1–5 against Theorem 7.1 | code/verify.py | results/verification.json | 18,680 comparisons |
| Higher exponents (3), (4,4), (3,3,3), (2,3,5) with and without a nonface against Theorem 6.1 | code/verify.py | results/verification.json | 143 comparisons over F_1009 |
| Example 4.2 by direct elimination | code/verify.py | results/verification.json `order_eight_example` | rank 386, kernel 14, cokernel 20 |
| Block profiles against direct elimination (paths n ≤ 12; lollipops 2 ≤ m ≤ 5, n ≤ 7) | [code/chordal_lefschetz.py](code/chordal_lefschetz.py) | [results/chordal.json](results/chordal.json) | 1,128 direct eliminations; exact integers |
| Elimination-order invariance and multiplicativity | code/chordal_lefschetz.py | results/chordal.json | 300 random chordal graphs each |
| Chordal criterion for paths (n ≤ 120) and lollipops (m ≤ 8, n ≤ 60); prime thresholds (paths n ≤ 40, p ≤ 43; lollipops n ≤ 25, p ≤ 29); witness inequalities to n = 5000; agreement with the published Nguyen–Tran and lollipop lists | code/chordal_lefschetz.py | results/chordal.json | exact |

Numbers quoted on the release page and in the audio: three pairwise non-adjacent vertices; seven-vertex computer checks
by Holleben and Nicklasson and a posted eight-vertex check; path lists 1–7, 9, 10, 13 (weak) and 1–7, 9 (strong);
lollipop lists; characteristic thresholds about n/2 (weak) and n (strong); the eight-vertex example 400, 406, 386, 14, 20.
All are proved or in the recorded output.

## Limits

The splitting needs a private leaf at every vertex (or a simplicial vertex at each elimination step). The path and
lollipop corollaries use an exact finite check for n ≤ 24 and n ≤ 22. Prime-characteristic thresholds for unequal higher
exponents are not determined. The scripts check the theorems on finite ranges; the proofs carry the general claims.
Prior-art searches were of limited scope.

## Replay and records

Replay commands: [README.md](README.md), [ENVIRONMENT.txt](ENVIRONMENT.txt), [REPLAY_RECEIPT.md](REPLAY_RECEIPT.md),
CI [.github/workflows/replay.yml](.github/workflows/replay.yml). Review: [REVIEW_SUMMARY.md](REVIEW_SUMMARY.md). Prior
art and limitation triage: [RESEARCH_GATES.json](RESEARCH_GATES.json). Bibliography: [refs.bib](refs.bib). Dependencies:
[requirements.txt](requirements.txt). Licences: [LICENSE.md](LICENSE.md). Citation: [CITATION.cff](CITATION.cff).
Hashes: [MANIFEST.sha256](MANIFEST.sha256).
