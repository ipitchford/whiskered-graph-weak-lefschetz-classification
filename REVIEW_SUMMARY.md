# Review summary (public, 0.1.0-candidate)

This records the internal review of the candidate: who looked, what they raised, and what was done. It is
AI-assisted internal review, not peer review or independent reproduction.

## What ran

1. **Panel (round 1).** Five Claude reviewer roles (editor, methodology, domain specialist, perspective and devil's
   advocate) in one combined review pass. The methodology role checked every proof line by line against the definitions
   of Holleben and Nicklasson; the domain role checked the literature, attribution and novelty against the cited sources,
   which were read. The panel also recomputed the whiskered classification with its own script, independent of the
   package code, and reran the original verifier. No critical issue and no mathematical error was found.
2. **Replay.** A clean replay of the original verifier reproduced every printed count; it used bare `assert`, which is
   skipped under `python -O`, so the checks were rewritten to fail explicitly. Negative controls were added.
3. **Revision round.** One round addressed every item (table below) and added extensions: the chordal Lefschetz
   criterion (Theorem 7.3), the block profile and its invariance (Proposition 7.2), the path and lollipop corollaries in
   every characteristic with the strong-property lists (Lemma 7.4, Corollaries 7.5 and 7.6), the characterisation of the
   Holleben–Nicklasson Perazzo algebras with the weak property (Remark after Corollary 5.2), and the script
   `code/chordal_lefschetz.py`.
4. **Verification.** A re-review checked every first-round item against the revised text, and a proof audit checked
   every new and rewritten proof, with an independent recomputation of the relabelling behind equation (2), the
   whiskered classification, the chordal block profiles, the path and lollipop lists, the prime thresholds and the
   witness inequalities. Every audited proof was found correct. Two attribution and scope items were raised and fixed
   (V1 and V2 below).

No Astra/Codex review took place: the second-model route was unsupported for the account during this batch.

## Objections and dispositions

| Item | Raised by | Disposition |
|---|---|---|
| Holleben–Nicklasson Lemma 3.1 (and Proposition 3.2) already split the complete-graph case, in triangular form | domain, devil's advocate | Credited in Section 1 (key idea) and in the Remark after Theorem 3.1 |
| The necessity argument for the Gorenstein algebras is Holleben–Nicklasson's Theorem 4.6 projection argument | domain, devil's advocate | Credited in the proof of Corollary 5.2 |
| Position the splitting against Gasanova–Lundqvist–Nicklasson Theorem 1; cite the path, lollipop and tadpole papers | domain | Paragraph after Theorem 7.1; Nguyen–Tran, lollipop and tadpole papers cited |
| The abstract promised more on chordal graphs than was proved | devil's advocate | Resolved by extension: Theorem 7.3 proves a criterion for all chordal graphs |
| The posted eight-vertex check needed its author; a process-style "literature check" paragraph | editor | Cited by its Crossref author (Z. Zeng); paragraph removed |
| "Applies to arbitrary complexes" needed qualifying | editor, domain | Qualified: a private leaf at every vertex is needed (Remark after Theorem 3.1; Section 8) |
| The diagonal form of inclusion matrices should cite Wilson directly | domain | Wilson (1990) Theorem 2 read and cited (Theorem 1 for ranks mod p); Ghorbani et al. Corollary 3 as a second proof |
| Dirac's theorem citation | domain | Cited through Fulkerson and Gross (1965), p. 851, which states it |
| V1: the reduction to the sum of the variables over an arbitrary field is already recorded by Cooper et al. | re-review | Credited to Cooper et al., Lemma 2.2 and the remark after it; Lemma 2.1 is kept because it covers all powers |
| V2: Holleben–Nicklasson Lemma 4.5 applies only to Perazzo forms | re-review | The Remark after Corollary 5.2 now proves that F(w(G)) is a Perazzo form for every non-complete G before applying it |
| Minor rigour items (strip inequalities, Theorem 6.1 for unequal exponents, prime ranges, definitions of level, G-quadratic, Perazzo and simplicial form) | methodology, re-review | Written out; for unequal exponents only the rank formula is claimed, and prime-characteristic thresholds are stated as not determined |
| Readability: the first version had no motivation, no roadmap and undefined notation | editor, perspective | New Section 1 (problem, what was known, Theorems A–C, key idea, roadmap); every section opens with a sentence saying what it does; notation defined before use |
| Checks used `assert` | replay | Explicit checks that print FAIL and exit 1; negative controls under `python -O` |

## Open after review

Cycles and tadpole graphs with a cycle of length at least four, very well-covered graphs in general, partially
whiskered graphs, and prime-characteristic thresholds for unequal higher exponents (Section 8). Prior-art searches were of
limited scope (see `RESEARCH_GATES.json`).
