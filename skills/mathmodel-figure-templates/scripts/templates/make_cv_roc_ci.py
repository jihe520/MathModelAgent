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
class ModelSpec:
    name: str
    auc_mean: float
    auc_std: float
    color: str
    ci_alpha: float
    noise: float


MODEL_SPECS = [
    ModelSpec("LR", 0.889, 0.026, "#2d214c", 0.16, 0.030),
    ModelSpec("RF", 0.906, 0.029, "#8f3032", 0.13, 0.026),
    ModelSpec("XGBoost", 0.895, 0.032, "#c47b4b", 0.14, 0.030),
    ModelSpec("LightGBM", 0.902, 0.039, "#3c8849", 0.15, 0.035),
    ModelSpec("SVM", 0.861, 0.043, "#242585", 0.16, 0.042),
]


def configure_matplotlib() -> None:
    mpl.rcParams.update(
        {
            "font.family": "sans-serif",
            "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
            "svg.fonttype": "none",
            "pdf.fonttype": 42,
            "font.size": 10,
            "axes.linewidth": 0.75,
            "axes.spines.right": True,
            "axes.spines.top": True,
            "legend.frameon": True,
        }
    )


def auc_to_curve_exponent(auc: float) -> float:
    auc = np.clip(auc, 0.60, 0.985)
    return auc / (1.0 - auc)


def base_roc_curve(fpr: np.ndarray, auc: float) -> np.ndarray:
    exponent = auc_to_curve_exponent(auc)
    tpr = 1.0 - (1.0 - fpr) ** exponent
    early_lift = 0.030 * np.exp(-((fpr - 0.055) / 0.055) ** 2)
    shoulder = -0.020 * np.exp(-((fpr - 0.34) / 0.20) ** 2)
    return np.clip(tpr + early_lift + shoulder, 0.0, 1.0)


def fold_auc_targets(mean_auc: float, std_auc: float, n_folds: int = 5) -> np.ndarray:
    offsets = np.array([-1.20, -0.45, 0.05, 0.55, 1.05])
    offsets = offsets[:n_folds]
    offsets = offsets - offsets.mean()
    offsets = offsets / offsets.std(ddof=1)
    return np.clip(mean_auc + offsets * std_auc, 0.72, 0.98)


def make_empirical_fold_curve(
    rng: np.random.Generator,
    target_auc: float,
    model_noise: float,
) -> tuple[np.ndarray, np.ndarray]:
    n_knots = 31
    low_fpr = np.sort(rng.beta(0.72, 4.6, size=22))
    high_fpr = np.sort(rng.uniform(0.22, 1.0, size=n_knots - low_fpr.size))
    fpr = np.unique(np.r_[0.0, low_fpr, high_fpr, 1.0])
    tpr_base = base_roc_curve(fpr, target_auc)
    hetero = model_noise * (1.15 - 0.55 * fpr)
    fold_noise = rng.normal(0.0, hetero, size=fpr.size)
    fold_noise[0] = 0.0
    fold_noise[-1] = 0.0
    tpr = np.clip(tpr_base + fold_noise, 0.0, 1.0)
    tpr = np.maximum.accumulate(tpr)
    tpr[0] = 0.0
    tpr[-1] = 1.0
    return fpr, tpr


def interpolate_fold(fpr: np.ndarray, tpr: np.ndarray, grid: np.ndarray) -> np.ndarray:
    interp = np.interp(grid, fpr, tpr)
    interp[0] = 0.0
    interp[-1] = 1.0
    return interp


def simulate_cv_rocs(
    spec: ModelSpec,
    grid: np.ndarray,
    seed: int,
    n_folds: int = 5,
) -> tuple[list[tuple[np.ndarray, np.ndarray]], np.ndarray, np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    fold_curves: list[tuple[np.ndarray, np.ndarray]] = []
    interpolated = []
    for target_auc in fold_auc_targets(spec.auc_mean, spec.auc_std, n_folds):
        fpr, tpr = make_empirical_fold_curve(rng, float(target_auc), spec.noise)
        fold_curves.append((fpr, tpr))
        interpolated.append(interpolate_fold(fpr, tpr, grid))

    tpr_matrix = np.vstack(interpolated)
    mean_tpr = tpr_matrix.mean(axis=0)
    std_tpr = tpr_matrix.std(axis=0, ddof=1)
    lower = np.clip(mean_tpr - std_tpr, 0.0, 1.0)
    upper = np.clip(mean_tpr + std_tpr, 0.0, 1.0)
    mean_tpr[0] = 0.0
    mean_tpr[-1] = 1.0
    return fold_curves, mean_tpr, lower, upper


def add_caption_and_table(fig: plt.Figure) -> None:
    caption_ax = fig.add_axes([0.06, 0.165, 0.88, 0.055])
    caption_ax.axis("off")
    caption_ax.text(
        0.00,
        0.70,
        "Fig. 2",
        fontsize=9,
        fontweight="bold",
        ha="left",
        va="center",
    )
    caption_ax.text(
        0.058,
        0.70,
        "The average AUC performance of five machine learning models subjected to fivefold external cross-validation",
        fontsize=8.5,
        color="#4b4b4b",
        ha="left",
        va="center",
    )

    table_ax = fig.add_axes([0.045, 0.035, 0.91, 0.095])
    table_ax.axis("off")
    table_ax.text(0.00, 0.88, "Table 3", fontsize=9, fontweight="bold", ha="left", va="center")
    table_ax.text(
        0.082,
        0.88,
        "Comparative analysis of the performance outcomes across various machine learning models",
        fontsize=8.5,
        color="#4b4b4b",
        ha="left",
        va="center",
    )

    columns = [
        "Model",
        "F1 score (%)",
        "Accuracy (%)",
        "Recall (%)",
        "Precision (%)",
        "AUC (%)",
        "Sensitivity (%)",
        "Specificity (%)",
    ]
    row = ["LR model", "80.8", "84.7", "80.0", "81.6", "89.6", "80.0", "87.8"]
    xs = np.array([0.00, 0.165, 0.285, 0.410, 0.535, 0.662, 0.792, 0.925])

    table_ax.plot([0, 1], [0.67, 0.67], color="#b8b8b8", linewidth=0.8)
    table_ax.plot([0, 1], [0.37, 0.37], color="#b8b8b8", linewidth=0.8)
    for x, label in zip(xs, columns):
        table_ax.text(x, 0.52, label, fontsize=7.5, fontweight="bold", ha="left", va="center")
    for x, value in zip(xs, row):
        table_ax.text(x, 0.18, value, fontsize=7.3, color="#555555", ha="left", va="center")
    table_ax.set_xlim(0, 1)
    table_ax.set_ylim(0, 1)


def make_figure(output_stem: Path) -> None:
    configure_matplotlib()
    grid = np.linspace(0.0, 1.0, 101)

    fig = plt.figure(figsize=(7.4, 7.8))
    ax = fig.add_axes([0.17, 0.255, 0.70, 0.70])

    legend_handles = []
    legend_labels = []
    for idx, spec in enumerate(MODEL_SPECS):
        fold_curves, mean_tpr, lower, upper = simulate_cv_rocs(spec, grid, seed=814 + idx * 17)
        for fpr, tpr in fold_curves:
            ax.step(
                fpr,
                tpr,
                where="post",
                color=spec.color,
                alpha=0.13,
                linewidth=0.65,
                zorder=1,
            )
        ax.fill_between(
            grid,
            lower,
            upper,
            step="post",
            color=spec.color,
            alpha=spec.ci_alpha,
            linewidth=0,
            zorder=2,
        )
        (line,) = ax.step(
            grid,
            mean_tpr,
            where="post",
            color=spec.color,
            linewidth=1.15,
            zorder=4,
        )
        legend_handles.append(line)
        legend_labels.append(f"{spec.name:<8}: {spec.auc_mean:.3f}±{spec.auc_std:.3f} (p<0.01)")

    ax.plot([0, 1], [0, 1], linestyle="--", color="#a34545", linewidth=0.8, alpha=0.78, zorder=0)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlabel("False Positive Rate", fontsize=10)
    ax.set_ylabel("True Positive Rate", fontsize=10)
    ax.set_xticks(np.arange(0.0, 1.01, 0.1))
    ax.set_yticks(np.arange(0.0, 1.01, 0.1))
    ax.tick_params(labelsize=8.5, length=3, width=0.7)
    ax.grid(True, color="#bcbcbc", alpha=0.28, linewidth=0.6)
    ax.legend(
        legend_handles,
        legend_labels,
        loc="lower right",
        fontsize=9,
        framealpha=0.72,
        facecolor="white",
        edgecolor="#d9d9d9",
        handlelength=2.1,
        labelspacing=0.65,
        borderpad=0.45,
    )

    add_caption_and_table(fig)

    output_stem.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_stem.with_suffix(".png"), dpi=300, bbox_inches="tight")
    fig.savefig(output_stem.with_suffix(".pdf"), bbox_inches="tight")
    fig.savefig(output_stem.with_suffix(".svg"), bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    make_figure(ROOT / "outputs" / "cv_roc_ci_replica")


if __name__ == "__main__":
    main()
