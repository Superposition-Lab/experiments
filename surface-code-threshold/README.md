# surface-code-threshold

**Question.** Reproduce the rotated surface-code memory threshold plot at d = 3/5/7 under uniform circuit-level depolarizing noise, and time two MWPM decoders (PyMatching, Fusion Blossom) on the same syndrome data.

**Data collected:** 2026-08-27 (36 tasks, ≥1000 errors each, 1.52M shots total).

Companion post: [Where quantum error correction starts to work](https://splabs.sh/writings/where-quantum-error-correction-starts-to-work/) — a Superposition experiment (E-002).

## Run

```
just setup   # uv sync
just smoke   # minutes: d=3/5, two noise points — proves the stack
just run     # full sweep: d=3/5/7 × p=0.004…0.014, resumable (results/stats.csv)
just plot    # plots/threshold.png
```

`sinter.collect` appends to `results/stats.csv` and resumes: re-running `just run` continues where it stopped.

## Versions (pinned in `uv.lock`; recorded 2026-08-25)

stim 1.16.0 · sinter 1.16.0 · PyMatching 2.4.0 · fusion-blossom 0.2.13 · Python via uv · Apple Silicon.

sinter's built-in decoders here: `pymatching`, `pymatching-correlated`, `fusion_blossom`, `hypergraph_union_find`, `mw_parity_factor`, `vacuous` — the last three are candidates for widening the harness later.

## Knobs (state them in the post)

- Circuit family: `surface_code:rotated_memory_z`, rounds = d.
- Noise: the same p applied as after-Clifford depolarization, before-round data depolarization, measurement flip, and reset flip (stim's uniform circuit-level model).
- Stopping: `max_shots` = 1M, `max_errors` = 1000 per task.

## Result (2026-08-27, full sweep; `plots/threshold.png`)

- **Threshold:** the d = 3/5/7 curves cross between p = 0.006 and 0.008, at ≈ 0.7% for this uniform depolarizing model with rounds = d. Below the crossing, larger distance wins (at p = 0.004: 1.15% → 0.73% → 0.45% logical error per shot for d = 3/5/7); above it, larger distance loses.
- **Accuracy:** PyMatching and Fusion Blossom agree within statistical error at every point (both panels of the plot are visually identical) — expected, both are exact MWPM.
- **Speed (sinter wall clock, harness caveat below):** PyMatching 0.4–1.3 µs/shot at d=3, 3.0–9.9 at d=5, 8.3–31 at d=7. Fusion Blossom 15–45, 59–269, 271–2047 µs/shot respectively — 30–90× slower in this harness at d=7. The gap is implementation and Python-binding overhead, not the blossom algorithm — found 2026-08-27: sinter's fusion-blossom integration decodes per shot in Python (a `SyndromePattern` object per shot, two FFI crossings, `np.binary_repr` string formatting in the loop; `sinter/_decoding/_decoding_fusion_blossom.py`), while PyMatching gets one batched C++ call. Fusion-blossom's own Rust-side benchmarks are the fair comparison and belong to a later, dedicated latency harness. Any published timing table must be labeled "decoder as integrated in sinter".

## Caveats

- `sinter`'s `seconds` includes worker/harness overhead and amortizes setup over few shots in small runs — it ranks decoders coarsely; a real latency benchmark (per-shot distributions, tails, streaming) is a separate harness and a later experiment.
- Threshold read off the crossing of d-curves is an estimate; quote it with the noise model attached, never as "the" surface-code threshold.
