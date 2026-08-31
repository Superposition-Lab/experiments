"""Threshold plot from results/stats.csv: logical error rate vs physical noise,
one curve per (decoder, distance). The crossing of the distance curves is the
threshold estimate. Writes plots/threshold.png.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import sinter

HERE = Path(__file__).parent
STATS = HERE / "results" / "stats.csv"
OUT = HERE / "plots" / "threshold.png"


def main() -> None:
    stats = sinter.read_stats_from_csv_files(STATS)
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    for ax, decoder in zip(axes, ("pymatching", "fusion_blossom")):
        sinter.plot_error_rate(
            ax=ax,
            stats=[s for s in stats if s.decoder == decoder],
            x_func=lambda s: s.json_metadata["p"],
            group_func=lambda s: f"d={s.json_metadata['d']}",
        )
        ax.loglog()
        ax.set_title(decoder)
        ax.set_xlabel("physical error rate p")
        ax.grid(which="both", alpha=0.3)
        ax.legend()
    axes[0].set_ylabel("logical error rate per shot")
    OUT.parent.mkdir(exist_ok=True)
    fig.savefig(OUT, dpi=160, bbox_inches="tight")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
