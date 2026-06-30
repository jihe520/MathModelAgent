from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
os.environ.setdefault("MPLCONFIGDIR", str(ROOT / ".mplconfig"))

import matplotlib as mpl

mpl.use("Agg")

import matplotlib.pyplot as plt
import numpy as np


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["Times New Roman", "Times", "DejaVu Serif", "serif"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "font.size": 10,
            "axes.linewidth": 0.8,
        }
    )


def true_rmse_surface(max_depth: np.ndarray, n_estimators: np.ndarray) -> np.ndarray:
    x = np.asarray(max_depth, dtype=float)
    y = np.asarray(n_estimators, dtype=float)

    base = 0.505
    broad_slope = 0.018 * np.exp(-x / 9.0) + 0.010 * np.cos(y / 32.0)
    red_ridge = 0.165 * np.exp(-((x - 6.0) / 5.2) ** 2 - ((y - 162.0) / 34.0) ** 2)
    red_cap = 0.045 * np.exp(-((x - 3.0) / 3.5) ** 2 - ((y - 190.0) / 24.0) ** 2)
    warm_hump = 0.052 * np.exp(-((x - 22.0) / 5.5) ** 2 - ((y - 96.0) / 21.0) ** 2)
    cool_basin = -0.116 * np.exp(-((x - 30.0) / 8.5) ** 2 - ((y - 112.0) / 29.0) ** 2)
    narrow_trough = -0.047 * np.exp(-((x - 34.5) / 3.2) ** 2 - ((y - 124.0) / 9.5) ** 2)
    ripples = 0.011 * np.sin(x * 0.70 + y * 0.055) + 0.007 * np.cos(x * 1.50 - y * 0.035)
    return np.clip(base + broad_slope + red_ridge + red_cap + warm_hump + cool_basin + narrow_trough + ripples, 0.375, 0.655)


def simulate_tpe_trials(seed: int = 20260505, n_trials: int = 210) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    depth_trials = []
    estimator_trials = []
    rmse_trials = []

    for trial in range(n_trials):
        if trial < 65:
            depth = rng.uniform(1, 40)
            estimators = rng.uniform(5, 200)
        elif trial < 150:
            # TPE-like exploitation: sample more often near the low-RMSE basin.
            depth = rng.normal(30, 7.0)
            estimators = rng.normal(116, 28.0)
            if rng.random() < 0.24:
                depth = rng.uniform(8, 40)
                estimators = rng.uniform(70, 170)
        else:
            depth = rng.normal(34, 4.5)
            estimators = rng.normal(120, 17.0)
            if rng.random() < 0.15:
                depth = rng.uniform(1, 18)
                estimators = rng.uniform(130, 195)

        depth = float(np.clip(depth, 1, 40))
        estimators = float(np.clip(estimators, 5, 200))
        noise = rng.normal(0.0, 0.008 + 0.00003 * estimators)
        rmse = float(true_rmse_surface(depth, estimators) + noise)
        depth_trials.append(depth)
        estimator_trials.append(estimators)
        rmse_trials.append(rmse)

    return np.array(depth_trials), np.array(estimator_trials), np.array(rmse_trials)


def idw_response_surface(
    depth_trials: np.ndarray,
    estimator_trials: np.ndarray,
    rmse_trials: np.ndarray,
    depth_grid: np.ndarray,
    estimator_grid: np.ndarray,
) -> np.ndarray:
    depth_scale = 40.0
    estimator_scale = 200.0
    surface = np.empty_like(depth_grid, dtype=float)

    trial_x = depth_trials / depth_scale
    trial_y = estimator_trials / estimator_scale
    grid_x = depth_grid / depth_scale
    grid_y = estimator_grid / estimator_scale

    for row in range(depth_grid.shape[0]):
        dx = grid_x[row, :, None] - trial_x[None, :]
        dy = grid_y[row, :, None] - trial_y[None, :]
        dist2 = dx * dx + dy * dy + 0.0045
        weights = 1.0 / (dist2**2.15)
        local = (weights @ rmse_trials) / weights.sum(axis=1)
        surface[row, :] = local

    analytic = true_rmse_surface(depth_grid, estimator_grid)
    blended = 0.58 * surface + 0.42 * analytic
    return np.clip(blended, 0.375, 0.655)


def make_figure(output_stem: Path) -> None:
    configure_matplotlib()

    depth_trials, estimator_trials, rmse_trials = simulate_tpe_trials()
    max_depth = np.linspace(1, 40, 115)
    n_estimators = np.linspace(5, 200, 125)
    depth_grid, estimator_grid = np.meshgrid(max_depth, n_estimators)
    rmse_grid = idw_response_surface(depth_trials, estimator_trials, rmse_trials, depth_grid, estimator_grid)

    fig = plt.figure(figsize=(9.2, 7.2))
    ax = fig.add_axes([0.02, 0.05, 0.78, 0.88], projection="3d")
    norm = mpl.colors.Normalize(vmin=0.385, vmax=0.655)
    surf = ax.plot_surface(
        depth_grid,
        estimator_grid,
        rmse_grid,
        cmap="coolwarm",
        norm=norm,
        linewidth=0,
        antialiased=True,
        shade=True,
        rstride=1,
        cstride=1,
        alpha=0.96,
    )

    ax.set_title("Smooth 3D Surface Plot with RMSE", fontsize=14, pad=18)
    ax.set_xlabel("max_depth", fontsize=13, labelpad=10)
    ax.set_ylabel("n_estimators", fontsize=13, labelpad=10)
    ax.set_zlabel("RMSE", fontsize=12, labelpad=8)
    ax.set_xlim(0, 40)
    ax.set_ylim(205, 0)
    ax.set_zlim(0.37, 0.66)
    ax.set_xticks(np.arange(0, 41, 5))
    ax.set_yticks(np.arange(0, 201, 25))
    ax.set_zticks(np.arange(0.40, 0.66, 0.05))
    ax.tick_params(labelsize=8, pad=2)
    ax.view_init(elev=31, azim=42)
    ax.set_box_aspect((1.18, 1.45, 0.72))

    for axis in [ax.xaxis, ax.yaxis, ax.zaxis]:
        axis.pane.set_facecolor((1, 1, 1, 0))
        axis.pane.set_edgecolor("#d0d0d0")
        axis._axinfo["grid"]["color"] = (0.72, 0.72, 0.72, 0.65)
        axis._axinfo["grid"]["linewidth"] = 0.6

    cax = fig.add_axes([0.84, 0.23, 0.028, 0.48])
    cbar = fig.colorbar(surf, cax=cax)
    cbar.set_label("RMSE", fontsize=11, labelpad=10)
    cbar.set_ticks(np.arange(0.40, 0.66, 0.05))
    cbar.ax.tick_params(labelsize=8)
    cbar.outline.set_linewidth(0.75)

    output_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_stem.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(output_stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output_stem.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    make_figure(ROOT / "outputs" / "rf_tpe_surface_replica")


if __name__ == "__main__":
    main()
