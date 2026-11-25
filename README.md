# Boolean blocks and the weak Lefschetz property of whiskered and chordal graph algebras

**Version 0.1.0-candidate. Unrefereed research candidate.** DOI [10.5281/zenodo.24540630](https://doi.org/10.5281/zenodo.24540630)
(all versions: [10.5281/zenodo.24540629](https://doi.org/10.5281/zenodo.24540629)). Creator: Anonymous. Text CC0-1.0;
code MIT. Release page: https://evidencepress.org/releases/whiskered-graph-weak-lefschetz-classification/

One change of variables splits the algebra into Boolean blocks. This settles the Holleben–Nicklasson conjecture over every
field and gives a Lefschetz criterion for all chordal graphs.

## What this is about

Many questions about counting can be turned into algebra. Take a network (a graph), make one variable per node, declare
that every variable squares to zero and that the product of two linked nodes is zero. The resulting algebra has one basis
element for each independent set of the network (a group of nodes with no links between them), so it records how many
independent sets there are of each size.

A classical question, named after the hard Lefschetz theorem of geometry, asks whether multiplying by one simple element,
the sum of all the variables, behaves as well as the dimensions allow at every step: it should lose nothing while the
spaces are growing and miss nothing once they shrink. When this holds (the **weak Lefschetz property**), the counting
sequence of the algebra is forced to rise and then fall smoothly. The **strong** version asks the same of every power of
that element.

**What was known.** *Whiskering* a network gives every node its own private leaf. Cooper, Faridi, Holleben, Nicklasson
and Van Tuyl, and then Holleben and Nicklasson (Journal of Pure and Applied Algebra, 2026), found that whiskered networks
rarely have the weak property. They settled several cases: the property holds for complete networks, and it fails for
networks with very large independent sets and for all bipartite networks (with computer checks for small orders). They
conjectured that it always fails once the original
network has three nodes with no links between them (independence number at least three). Computer checks covered networks
with up to seven nodes, and an eight-node check has been posted.

**What is new.**

1. The conjecture is true, over every field.
2. The exact answer. If the original network has n nodes and largest independent set of size α, the whiskered algebra has
   the weak property only if the network is complete (α = 1), or n is odd and α = 2; and then only if the field's
   characteristic is zero or larger than ⌈n/2⌉. The strong property holds only for complete networks, in characteristic
   zero or larger than n. The rank of every multiplication map is given by a formula in every characteristic.
3. The same answer, with thresholds shifted by one, for the Gorenstein algebras that Holleben and Nicklasson built from
   these networks.
4. For the much larger family of chordal networks (no unbridged cycles of length four or more), a simple test for both
   properties in every characteristic. It recovers two recent classifications, for paths and for "lollipop" networks, with
   short proofs and extends them to every characteristic. For example, a path network has the weak property for 1 to 7,
   9, 10 and 13 nodes, and never again; it has the strong property for 1 to 7 and 9 nodes.

**The idea of the proof.** Rename each leaf variable as "leaf plus its node". After this change, multiplying by the sum of
all the variables never alters which original nodes appear in a product, so the algebra breaks into independent pieces,
one for each independent set of the network. Each piece is a copy of the simplest algebra of this kind, the Boolean algebra
of subsets. Small pieces sit lower and large pieces higher. When one piece is shrinking while another is still growing at
the same step, the property fails, and that is exactly what three non-adjacent nodes cause. A classical description of
subset-inclusion matrices (Wilson; Ghorbani and coauthors) then gives every rank in every characteristic. Holleben and
Nicklasson's Lemma 3.1 already contains the complete-network case of this splitting in triangular form, and the argument
for the Gorenstein algebras follows the projection argument of their Theorem 4.6.

**Limits.** This is pure mathematics: a classification, not an algorithm for applications. The splitting needs a private
leaf at every node (or, for the chordal result, removable "simplicial" nodes), so cycles, tadpole networks and general
very well-covered networks are not covered. The path and lollipop results use a small exact computer check for short
lengths. The case of unequal higher exponents in prime characteristic is not settled. The work is an unrefereed
candidate; its assurance is internal AI-assisted review and computational checks only (see "Assurance" below).

## Contents

| Path | What it is |
|---|---|
| `manuscript.pdf`, `manuscript.tex` | The paper (13 pages). Section 1 is a plain introduction with a roadmap. |
| `code/verify.py` | Recomputes ranks in the original variables (no change of variables) by exact elimination over prime fields and compares them with the theorems. |
| `code/chordal_lefschetz.py` | Block profiles and the chordal criterion; paths and lollipops; exact integer arithmetic only. |
| `results/verification.json`, `results/chordal.json` | Recorded outputs of the two scripts (no timestamps). |
| `requirements.txt` | numpy 2.3.5 (for `verify.py`); `chordal_lefschetz.py` uses the standard library only. |
| `refs.bib` | The bibliography of the paper, from Crossref and arXiv records. |
| `AI_INDEX.md` | Machine-oriented map of claims, evidence and limits. |
| `RESEARCH_GATES.json` | Prior-art and limitation record. |
| `REVIEW_SUMMARY.md` | What the internal review raised and what was done. |
| `REPLAY_RECEIPT.md`, `ENVIRONMENT.txt` | Release replay and environment. |
| `.github/workflows/replay.yml` | CI: manifest, both scripts under `python -O`, byte comparison, negative controls. |
| `CITATION.cff`, `.zenodo.json`, `LICENSE.md`, `MANIFEST.sha256` | Citation, archive metadata, licences, hashes. |

## Replay

From the package root (seconds each; all arithmetic is exact, so outputs are platform-independent):

```sh
uv run --python 3.12 --with numpy==2.3.5 python3 -I -B -O code/verify.py --output results/verification.json
uv run --python 3.12 python3 -I -B -O code/chordal_lefschetz.py --output results/chordal.json
git diff --exit-code results/   # or: cmp against a pristine copy
```

Both scripts end with a line starting `PASS:` and exit 0; on any disagreement they print `FAIL: ...` and exit 1. Checks
are explicit (no `assert`), so they stay active under `python -O`. Both JSON outputs must be byte-identical to the files
in `results/`; no float tolerance is needed. Negative controls (run in CI): adding 8 to the Nguyen–Tran path list in
`chordal_lefschetz.py`, or forcing the WLP threshold in `verify.py` to 2, makes the script exit 1.

## Assurance

Written proofs with exact computational checks. Internal AI-assisted review only: a combined five-role Claude review
panel, a replay of the scripts with negative controls, one revision round with extensions, then a re-review and proof
audit of every new and rewritten proof (see `REVIEW_SUMMARY.md`). No Astra/Codex review took place. This is not peer
review, independent reproduction or formal verification. The scripts check the theorems on finite ranges; the proofs carry
the general claims.

## Citation

Anonymous (2026). *Boolean blocks and the weak Lefschetz property of whiskered and chordal graph algebras*. Version
0.1.0-candidate. Zenodo. https://doi.org/10.5281/zenodo.24540630
