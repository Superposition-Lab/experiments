"""E-002: rotated surface-code memory threshold, PyMatching vs Fusion Blossom.

Generates stim rotated_memory_z circuits at d = 3/5/7 under uniform
circuit-level depolarizing noise, collects logical error rates with sinter,
and records wall-clock decoding time per decoder.

Run `python threshold.py --smoke` for a minutes-long sanity pass, or without
flags for the full sweep. Results append to results/stats.csv (sinter's
resume format: re-running continues rather than restarts).
"""

import argparse
import os
from pathlib import Path

import sinter
import stim

DISTANCES = (3, 5, 7)
# Uniform depolarizing sweep bracketing the expected crossing (~1e-2).
PROBABILITIES = (0.004, 0.006, 0.008, 0.010, 0.012, 0.014)
DECODERS = ("pymatching", "fusion_blossom")
RESULTS = Path(__file__).parent / "results" / "stats.csv"


def make_task(d: int, p: float) -> sinter.Task:
    circuit = stim.Circuit.generated(
        "surface_code:rotated_memory_z",
        distance=d,
        rounds=d,
        after_clifford_depolarization=p,
        after_reset_flip_probability=p,
        before_measure_flip_probability=p,
        before_round_data_depolarization=p,
    )
    return sinter.Task(circuit=circuit, json_metadata={"d": d, "p": p, "rounds": d})


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--smoke", action="store_true", help="tiny run to prove the stack")
    args = parser.parse_args()

    if args.smoke:
        distances, probabilities = (3, 5), (0.008, 0.012)
        max_shots, max_errors = 10_000, 100
    else:
        distances, probabilities = DISTANCES, PROBABILITIES
        max_shots, max_errors = 1_000_000, 1_000

    tasks = [make_task(d, p) for d in distances for p in probabilities]
    RESULTS.parent.mkdir(exist_ok=True)

    stats = sinter.collect(
        num_workers=max(1, (os.cpu_count() or 2) - 2),
        tasks=tasks,
        decoders=list(DECODERS),
        max_shots=max_shots,
        max_errors=max_errors,
        save_resume_filepath=str(RESULTS),
        print_progress=True,
    )

    print(f"\n{'decoder':<16}{'d':>3}{'p':>8}{'shots':>10}{'errors':>8}{'us/shot':>9}")
    for s in sorted(stats, key=lambda s: (s.decoder, s.json_metadata["d"], s.json_metadata["p"])):
        us = s.seconds / s.shots * 1e6 if s.shots else float("nan")
        print(
            f"{s.decoder:<16}{s.json_metadata['d']:>3}{s.json_metadata['p']:>8}"
            f"{s.shots:>10}{s.errors:>8}{us:>9.1f}"
        )
    print(f"\nstats: {RESULTS}")


if __name__ == "__main__":
    main()
