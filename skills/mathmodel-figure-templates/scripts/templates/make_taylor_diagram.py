from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mplconfig"))

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


@dataclass(frozen=True)
class TaylorPoint:
    model: str
    std: float
    corr: float


MODELS = [
    ("XGBoost", "#f2a51a"),
    ("ANN", "#d7191c"),
    ("GPR", "#2222a0"),
    ("NGBoost(normal)", "#36a852"),
    ("NGBoost(Log-normal)", "#0b6b20"),
    ("Observed", "#000000"),
]

PANELS: dict[str, list[TaylorPoint]] = {
    "training": [
        TaylorPoint("XGBoost", 1.020, 0.985),
        TaylorPoint("ANN", 0.930, 0.970),
        TaylorPoint("GPR", 1.080, 0.955),
        TaylorPoint("NGBoost(normal)", 0.980, 0.982),
        TaylorPoint("NGBoost(Log-normal)", 0.950, 0.974),
    ],
    "testing": [
        TaylorPoint("XGBoost", 1.000, 0.975),
        TaylorPoint("ANN", 0.960, 0.965),
        TaylorPoint("GPR", 1.060, 0.960),
        TaylorPoint("NGBoost(normal)", 1.020, 0.972),
        TaylorPoint("NGBoost(Log-normal)", 0.975, 0.968),
    ],
    "full dataset": [
        TaylorPoint("XGBoost", 1.010, 0.984),
        TaylorPoint("ANN", 0.940, 0.966),
        TaylorPoint("GPR", 1.085, 0.952),
        TaylorPoint("NGBoost(normal)", 0.990, 0.980),
        TaylorPoint("NGBoost(Log-normal)", 0.960, 0.972),
    ],
}


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif", "serif"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "font.size": 8,
            "axes.linewidth": 0.7,
            "legend.frameon": True,
        }
    )


def polar_to_xy(std: float | np.ndarray, corr: float | np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    corr_arr = np.asarray(corr)
    std_arr = np.asarray(std)
    theta = np.arccos(np.clip(corr_arr, 0.0, 1.0))
    return std_arr * np.cos(theta), std_arr * np.sin(theta)


def draw_taylor_grid(ax: plt.Axes, ref_std: float = 1.0, rmax: float = 1.75) -> None:
    theta = np.linspace(0, np.pi / 2, 300)
    grid_color = "#cfcfcf"
    light_color = "#dedede"

    for radius in np.arange(0.25, rmax + 0.001, 0.25):
        ax.plot(radius * np.cos(theta), radius * np.sin(theta), color=grid_color, lw=0.45, zorder=0)

    corr_ticks = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]
    for corr in corr_ticks:
        x, y = polar_to_xy(rmax, corr)
        ax.plot([0, x], [0, y], color=light_color, lw=0.45, zorder=0)

    # Centered RMS-difference contours around the observed reference point.
    phi = np.linspace(0, np.pi, 400)
    for rms in [0.25, 0.50, 0.75, 1.00, 1.25]:
        x = ref_std + rms * np.cos(phi)
        y = rms * np.sin(phi)
        mask = (x >= 0) & (y >= 0) & (x**2 + y**2 <= rmax**2)
        ax.plot(x[mask], y[mask], ls="--", color="#bdbdbd", lw=0.45, alpha=0.85, zorder=0)

    ax.plot(ref_std * np.cos(theta), ref_std * np.sin(theta), ls="--", color="#cc7c8f", lw=0.65, alpha=0.75)
    ax.plot(rmax * np.cos(theta), rmax * np.sin(theta), color="#999999", lw=0.75)

    ax.set_xlim(0, rmax)
    ax.set_ylim(0, rmax)
    ax.set_aspect("equal", adjustable="box")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color("#777777")
    ax.spines["left"].set_color("#777777")
    ax.set_xlabel("Standard Deviation", fontsize=8, labelpad=8)
    ax.set_ylabel("Standard Deviation", fontsize=8, labelpad=2)
    ticks = np.arange(0.0, rmax + 0.001, 0.25)
    ax.set_xticks(ticks)
    ax.set_yticks(ticks)
    ax.set_xticklabels([f"{t:.2f}" if t else "0" for t in ticks], fontsize=6.2)
    ax.set_yticklabels([f"{t:.2f}" if t else "0" for t in ticks], fontsize=6.2)
    ax.tick_params(length=2.0, width=0.55, pad=1)

    for corr in corr_ticks:
        x, y = polar_to_xy(rmax * 1.02, corr)
        angle = np.degrees(np.arccos(corr)) - 90
        label = f"{corr:.2f}" if corr >= 0.95 else f"{corr:.1f}"
        ax.text(x, y, label, fontsize=6.2, ha="center", va="center", rotation=angle, rotation_mode="anchor")

    label_x, label_y = polar_to_xy(rmax * 0.94, 0.68)
    ax.text(
        label_x,
        label_y,
        "Correlation",
        fontsize=7.2,
        rotation=-43,
        rotation_mode="anchor",
        ha="center",
        va="center",
    )
    ax.text(ref_std, -0.060, "Observed", fontsize=6.4, ha="center", va="top")


def draw_panel(ax: plt.Axes, points: list[TaylorPoint], letter: str) -> None:
    color_map = dict(MODELS)
    draw_taylor_grid(ax)

    handles = []
    for model, color in MODELS:
        if model == "Observed":
            x, y = polar_to_xy(1.0, 1.0)
            handle = ax.scatter(x, y, s=18, marker="o", facecolor=color, edgecolor="black", lw=0.35, zorder=5)
        else:
            point = next(item for item in points if item.model == model)
            x, y = polar_to_xy(point.std, point.corr)
            handle = ax.scatter(x, y, s=18, marker="o", facecolor=color, edgecolor="black", lw=0.35, zorder=5)
        handles.append(handle)

    ax.legend(
        handles,
        [model for model, _ in MODELS],
        loc="upper right",
        bbox_to_anchor=(1.02, 1.10),
        fontsize=5.4,
        labelspacing=0.12,
        handlelength=0.9,
        handletextpad=0.25,
        borderpad=0.25,
        framealpha=0.86,
        edgecolor="#999999",
        facecolor="white",
        fancybox=False,
    )
    ax.text(0.50, -0.22, f"({letter})", transform=ax.transAxes, fontsize=9, ha="center", va="center")


def add_header_and_caption(fig: plt.Figure) -> None:
    fig.text(0.035, 0.925, "D. Lai et al.", fontsize=8.5, fontstyle="italic", ha="left")
    fig.text(
        0.965,
        0.925,
        "Engineering Applications of Artificial Intelligence 135 (2024) 108704",
        fontsize=8.5,
        fontstyle="italic",
        ha="right",
    )
    fig.text(
        0.035,
        0.105,
        "Fig. 7.",
        fontsize=9,
        fontweight="bold",
        ha="left",
        va="baseline",
    )
    fig.text(
        0.090,
        0.105,
        (
            "Taylor diagram of the training (a), testing (b), and full dataset (c) of the ML models. "
            "The “Observed” point represents actual measured data from experiments or real-world"
        ),
        fontsize=8.4,
        ha="left",
        va="baseline",
    )
    fig.text(
        0.035,
        0.077,
        "observations, which the models (XGBoost, ANN, GPR, NGBoost) are being compared against.",
        fontsize=8.4,
        ha="left",
        va="baseline",
    )


def make_figure(output_stem: Path) -> None:
    configure_matplotlib()
    fig = plt.figure(figsize=(10.8, 5.7))

    lefts = [0.115, 0.405, 0.695]
    labels = ["a", "b", "c"]
    panel_keys = ["training", "testing", "full dataset"]
    for left, letter, key in zip(lefts, labels, panel_keys):
        ax = fig.add_axes([left, 0.285, 0.215, 0.465])
        draw_panel(ax, PANELS[key], letter)

    add_header_and_caption(fig)

    output_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_stem.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(output_stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output_stem.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    make_figure(ROOT / "outputs" / "taylor_diagram_replica")


if __name__ == "__main__":
    main()
