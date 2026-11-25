# Replay receipt (0.1.0-candidate, 25 November 2026)

Fresh copy of the approved candidate (hashes verified), cwd = package root, macOS 27.2.1 arm64, every command with
`python3 -I -B -O` and `PYTHONDONTWRITEBYTECODE=1`. Interpreters were printed inside the run.

| Command | Interpreter | Exit | Time | Output |
|---|---|---|---|---|
| `uv run --python 3.12 --with numpy==2.3.5 python3 -I -B -O code/verify.py --output results/verification.json` | CPython 3.12.11, numpy 2.3.5 | 0 | about 1 s | ends `PASS: all whiskered, idealisation, chordal and higher-power checks.`; JSON byte-identical to `results/verification.json` |
| `uv run --python 3.12 python3 -I -B -O code/chordal_lefschetz.py --output results/chordal.json` | CPython 3.14.7 (the `python3` shim; standard library only) | 0 | about 6 s | ends `PASS: chordal block criterion, paths and lollipops.`; JSON byte-identical to `results/chordal.json` |

Negative controls (fresh copies, `python3 -I -B -O`):

- `chordal_lefschetz.py` with `NT_PATH_WLP` changed to include 8: exit 1, `FAIL: Nguyen-Tran list disagrees at n=8`.
- `verify.py` with `threshold = 1 + (n % 2)` changed to `threshold = 2`: exit 1, `FAIL: WLP/SLP classification mismatch n=2 p=2`.

Comparison policy: exact (byte-identical JSON). All arithmetic is exact and the outputs contain no timestamps, floats or
version strings, so the same comparison is used on Linux CI (`.github/workflows/replay.yml`), which also reruns both
negative controls.

Changes after the replay: the DOI line on the title page of `manuscript.tex`, the rebuilt `manuscript.pdf` (three pdflatex
passes; 13 pages; word-level text comparison against the approved PDF shows only the DOI line), and the release records
(README, AI index, review summary, research gates, bibliography, citation, licences, CI workflow, manifest). No script,
recorded output or mathematical statement changed.
