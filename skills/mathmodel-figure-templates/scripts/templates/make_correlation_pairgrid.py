from __future__ import annotations

import math
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mplconfig"))

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


VARIABLES = [f"Variable_{idx}" for idx in range(1, 10)]


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "axes.linewidth": 0.6,
            "xtick.major.width": 0.45,
            "ytick.major.width": 0.45,
            "xtick.major.size": 1.8,
            "ytick.major.size": 1.8,
        }
    )


def simulate_data(seed: int = 20260629, n_samples: int = 130) -> np.ndarray:
    rng = np.random.default_rng(seed)
    f1 = rng.normal(size=n_samples)
    f2 = rng.normal(size=n_samples)
    f3 = rng.normal(size=n_samples)
    noise = lambda scale=1.0: rng.normal(scale=scale, size=n_samples)

    data = np.column_stack(
        [
            1.00 * f1 + 0.25 * f2 + noise(0.55),
            0.20 * f1 + 0.85 * f2 + noise(0.88),
            0.95 * f1 + noise(0.55),
            0.12 * f1 + 0.18 * f3 + noise(0.95),
            0.82 * f1 + 0.12 * f2 + noise(0.50),
            -0.20 * f1 + 0.20 * f3 + noise(0.92),
            0.78 * f1 + 0.20 * f2 + noise(0.48),
            -0.24 * f1 + 0.10 * f2 + noise(0.95),
            0.84 * f1 + 0.08 * f2 + noise(0.48),
        ]
    )
    data = (data - data.mean(axis=0)) / data.std(axis=0, ddof=1)
    return data


def kde_1d(values: np.ndarray, grid: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    std = max(np.std(values, ddof=1), 1e-4)
    bandwidth = max(1.06 * std * values.size ** (-1 / 5), 0.10)
    z = (grid[:, None] - values[None, :]) / bandwidth
    density = np.exp(-0.5 * z**2).mean(axis=1) / (bandwidth * np.sqrt(2 * np.pi))
    return density


def fit_line_with_ci(x: np.ndarray, y: np.ndarray, x_grid: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    slope, intercept = np.polyfit(x, y, deg=1)
    y_hat = slope * x_grid + intercept

    fitted = slope * x + intercept
    residuals = y - fitted
    n = x.size
    s_err = math.sqrt(np.sum(residuals**2) / max(n - 2, 1))
    x_mean = x.mean()
    ssx = np.sum((x - x_mean) ** 2)
    se_mean = s_err * np.sqrt(1.0 / n + (x_grid - x_mean) ** 2 / max(ssx, 1e-12))
    ci = 1.96 * se_mean
    return y_hat, y_hat - ci, y_hat + ci


def fisher_p_value(r: float, n: int) -> float:
    clipped = float(np.clip(r, -0.999999, 0.999999))
    z = 0.5 * math.log((1 + clipped) / (1 - clipped)) * math.sqrt(max(n - 3, 1))
    return math.erfc(abs(z) / math.sqrt(2.0))


def stars_for_p(p_value: float) -> str:
    if p_value < 0.001:
        return "***"
    if p_value < 0.01:
        return "**"
    if p_value < 0.05:
        return "*"
    return ""


def style_small_axes(ax: plt.Axes, row: int, col: int, n_vars: int) -> None:
    for spine in ax.spines.values():
        spine.set_color("#737373")
        spine.set_linewidth(0.45)
    ax.tick_params(labelsize=4.0, pad=0.5)
    if row < n_vars - 1:
        ax.set_xticklabels([])
    if col > 0:
        ax.set_yticklabels([])


def draw_scatter_cell(ax: plt.Axes, x: np.ndarray, y: np.ndarray, xlabel: str, ylabel: str) -> None:
    ax.scatter(x, y, s=8, color="#11779c", alpha=0.78, edgecolors="none", zorder=2)
    x_grid = np.linspace(x.min(), x.max(), 120)
    y_fit, y_low, y_high = fit_line_with_ci(x, y, x_grid)
    ax.fill_between(x_grid, y_low, y_high, color="#e8a8d1", alpha=0.36, linewidth=0, zorder=1)
    ax.plot(x_grid, y_fit, color="#9a4bb3", lw=1.0, zorder=3)
    ax.set_xlim(-3.1, 3.1)
    ax.set_ylim(-3.1, 3.1)
    ax.set_xlabel(xlabel, fontsize=4.7, labelpad=1)
    ax.set_ylabel(ylabel, fontsize=4.7, labelpad=1)


def draw_hist_cell(ax: plt.Axes, values: np.ndarray, xlabel: str) -> None:
    counts, bins, _ = ax.hist(values, bins=12, color="#9ecae1", edgecolor="#2b5d73", linewidth=0.55, alpha=0.90)
    grid = np.linspace(values.min() - 0.25, values.max() + 0.25, 180)
    density = kde_1d(values, grid)
    scaled = density / density.max() * max(counts) if density.max() > 0 else density
    ax.plot(grid, scaled, color="#225d78", lw=1.0)
    ax.set_xlabel(xlabel, fontsize=4.7, labelpad=1)
    ax.set_ylabel("Count", fontsize=4.7, labelpad=1)


def draw_corr_cell(
    ax: plt.Axes,
    r: float,
    p_value: float,
    cmap: mpl.colors.Colormap,
    norm: mpl.colors.Normalize,
) -> None:
    ax.set_facecolor(cmap(norm(r)))
    for spine in ax.spines.values():
        spine.set_color("white")
        spine.set_linewidth(1.6)
    ax.set_xticks([])
    ax.set_yticks([])
    text_color = "white" if abs(r) >= 0.55 else "#1f1f1f"
    ax.text(0.5, 0.46, f"{r:.2f}", ha="center", va="center", fontsize=6.7, color=text_color, transform=ax.transAxes)
    star_text = stars_for_p(p_value)
    if star_text:
        ax.text(0.5, 0.68, star_text, ha="center", va="center", fontsize=6.4, fontweight="bold", color=text_color, transform=ax.transAxes)


def make_figure(output_stem: Path) -> None:
    configure_matplotlib()
    data = simulate_data()
    corr = np.corrcoef(data, rowvar=False)
    n_vars = data.shape[1]
    n_samples = data.shape[0]

    cmap = mpl.colormaps["RdBu_r"]
    norm = mpl.colors.Normalize(vmin=-1.0, vmax=1.0)

    fig = plt.figure(figsize=(9.2, 8.6))
    grid = fig.add_gridspec(
        n_vars,
        n_vars,
        left=0.055,
        right=0.905,
        bottom=0.055,
        top=0.965,
        wspace=0.08,
        hspace=0.08,
    )

    for row in range(n_vars):
        for col in range(n_vars):
            ax = fig.add_subplot(grid[row, col])
            if row > col:
                draw_scatter_cell(ax, data[:, col], data[:, row], VARIABLES[col], VARIABLES[row])
                style_small_axes(ax, row, col, n_vars)
            elif row == col:
                draw_hist_cell(ax, data[:, col], VARIABLES[col])
                style_small_axes(ax, row, col, n_vars)
            else:
                r = corr[row, col]
                p = fisher_p_value(r, n_samples)
                draw_corr_cell(ax, r, p, cmap, norm)

    cax = fig.add_axes([0.925, 0.145, 0.028, 0.79])
    sm = mpl.cm.ScalarMappable(norm=norm, cmap=cmap)
    cbar = fig.colorbar(sm, cax=cax)
    ticks = np.linspace(-1.0, 1.0, 9)
    cbar.set_ticks(ticks)
    cbar.set_ticklabels([f"{tick:.2f}" for tick in ticks])
    cbar.ax.tick_params(labelsize=6, width=0.45, length=2)
    cbar.outline.set_linewidth(0.45)

    output_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_stem.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(output_stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output_stem.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    make_figure(ROOT / "outputs" / "correlation_pairgrid_replica")


if __name__ == "__main__":
    main()
