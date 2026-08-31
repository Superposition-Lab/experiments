# Experiments

The runnable experiments behind [Superposition](https://splabs.sh) posts. Anything a post links to must be re-runnable months later, so each experiment is a folder with a `README.md` (question · date · exact commands · result), a `justfile` (`setup` / `run` / `plot` / `test`) and pinned dependencies (`pyproject.toml` + `uv.lock`, or `Cargo.lock`). The table below records the **commit hash each post was written against**.

Early experiments that predate this repository keep their own repo; their rows link out. Ids are `E-NNN`, sequential, never reused.

| Id | Slug | Kind | Question | Thread | Repo @ commit | Status | Backs |
| -- | ---- | ---- | -------- | ------ | ------------- | ------ | ----- |
| E-001 | ecc_vs_pqc_zkp | own repo | Do Google's ZK proofs of secp256k1 point-addition circuits verify — with the shipped key, with a recomputed key, and against a from-source rebuild? | T1 | [`github.com/MCarlomagno/ecc_vs_pqc_zkp`](https://github.com/MCarlomagno/ecc_vs_pqc_zkp) @ `9e5e5ce` (the repo's sole commit, dated 2026-08-04 — pushed three days after № 001; earliest public state) | done | [№ 001](https://splabs.sh/writings/google-zkp-quantum-attack-bitcoin/) |
| E-002 | surface-code-threshold | in this repo | Reproduce a rotated-surface-code memory threshold plot at d = 3/5/7, and time PyMatching vs Fusion Blossom on the same syndromes | T2 | [`./surface-code-threshold`](./surface-code-threshold/) @ *(record hash at first push)* | data collected 2026-08-27 (threshold ≈ 0.7%; PyMatching 30–90× faster in-harness at d=7 — integration, not algorithm; see its README) | [№ 004](https://splabs.sh/writings/where-quantum-error-correction-starts-to-work/) (2026-09-01) |

## Conventions for a re-runnable experiment

- README answers: what question, when, exact commands, expected output, actual result, tool versions (`uv tree` / `cargo --version` / `sp1up --version` / Docker image tags).
- Data that came from outside is immutable under `data/raw/`; derived artifacts under `results/` with hashes.
- Notebooks, if any, are marimo (`.py`) — no hidden state, diffs cleanly.
- Large or vendored inputs (e.g. Google's Zenodo release, Docker images) are **not** committed; record URL + hash instead.
